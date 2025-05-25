import requests
import base64
import json
import os
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import quote
import time


@dataclass
class Repository:
    """Data class to represent a GitHub repository."""
    name: str
    full_name: str
    description: Optional[str]
    default_branch: str
    html_url: str
    language: Optional[str]
    stars: int
    forks: int


@dataclass
class ReadmeContent:
    """Data class to represent README content from a repository."""
    repository_name: str
    repository_url: str
    content: str
    encoding: str
    file_path: str


class GitHubAnalyzer:
    """
    A tool to analyze GitHub repositories and extract README files.
    """
    
    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize the GitHub analyzer.
        
        Args:
            github_token: Optional GitHub personal access token for higher rate limits.
                         If not provided, will try to get from GITHUB_TOKEN environment variable.
        """
        # If no token provided, try to get from environment
        if github_token is None:
            github_token = os.getenv('GITHUB_TOKEN')
        
        self.base_url = "https://api.github.com"
        self.session = requests.Session()
        
        if github_token:
            self.session.headers.update({
                "Authorization": f"token {github_token}",
                "Accept": "application/vnd.github.v3+json"
            })
        else:
            self.session.headers.update({
                "Accept": "application/vnd.github.v3+json"
            })
    
    def get_user_repositories(self, username: str) -> List[Repository]:
        """
        Fetch all public repositories for a given username.
        
        Args:
            username: GitHub username
            
        Returns:
            List of Repository objects
            
        Raises:
            requests.RequestException: If API request fails
        """
        repositories = []
        page = 1
        per_page = 100
        
        while True:
            url = f"{self.base_url}/users/{quote(username)}/repos"
            params = {
                "type": "public",
                "sort": "updated",
                "direction": "desc",
                "page": page,
                "per_page": per_page
            }
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                repos_data = response.json()
                
                # If no more repositories, break the loop
                if not repos_data:
                    break
                
                for repo_data in repos_data:
                    repository = Repository(
                        name=repo_data["name"],
                        full_name=repo_data["full_name"],
                        description=repo_data.get("description"),
                        default_branch=repo_data["default_branch"],
                        html_url=repo_data["html_url"],
                        language=repo_data.get("language"),
                        stars=repo_data["stargazers_count"],
                        forks=repo_data["forks_count"]
                    )
                    repositories.append(repository)
                
                # If we got less than per_page results, we're on the last page
                if len(repos_data) < per_page:
                    break
                
                page += 1
                
                # Add a small delay to respect rate limits
                time.sleep(0.1)
                
            except requests.RequestException as e:
                print(f"Error fetching repositories for user {username}: {e}")
                raise
        
        return repositories
    
    def get_readme_content(self, repository: Repository) -> Optional[ReadmeContent]:
        """
        Fetch README content from a repository.
        
        Args:
            repository: Repository object
            
        Returns:
            ReadmeContent object if README found, None otherwise
        """
        # Common README file names to try
        readme_names = [
            "README.md",
            "readme.md",
            "README.MD",
            "README",
            "readme",
            "README.txt",
            "readme.txt",
            "README.rst",
            "readme.rst"
        ]
        
        for readme_name in readme_names:
            try:
                url = f"{self.base_url}/repos/{repository.full_name}/contents/{readme_name}"
                params = {"ref": repository.default_branch}
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    file_data = response.json()
                    
                    # Decode the content from base64
                    if file_data.get("encoding") == "base64":
                        content = base64.b64decode(file_data["content"]).decode("utf-8", errors="ignore")
                    else:
                        content = file_data.get("content", "")
                    
                    return ReadmeContent(
                        repository_name=repository.name,
                        repository_url=repository.html_url,
                        content=content,
                        encoding=file_data.get("encoding", ""),
                        file_path=file_data.get("path", readme_name)
                    )
                
                # Add a small delay between requests
                time.sleep(0.05)
                
            except requests.RequestException as e:
                print(f"Error fetching README for {repository.name}: {e}")
                continue
        
        return None
    
    def analyze_user(self, username: str) -> Tuple[List[Repository], List[ReadmeContent]]:
        """
        Analyze a GitHub user by fetching all repositories and their README files.
        
        Args:
            username: GitHub username
            
        Returns:
            Tuple of (repositories, readme_contents)
        """
        print(f"Fetching repositories for user: {username}")
        repositories = self.get_user_repositories(username)
        print(f"Found {len(repositories)} repositories")
        
        readme_contents = []
        
        for i, repo in enumerate(repositories, 1):
            print(f"Processing repository {i}/{len(repositories)}: {repo.name}")
            readme = self.get_readme_content(repo)
            
            if readme:
                readme_contents.append(readme)
                print(f"  ✓ README found ({len(readme.content)} characters)")
            else:
                print(f"  ✗ No README found")
        
        print(f"\nAnalysis complete!")
        print(f"Total repositories: {len(repositories)}")
        print(f"Repositories with README: {len(readme_contents)}")
        
        return repositories, readme_contents
    
    def save_results(self, username: str, repositories: List[Repository], 
                    readme_contents: List[ReadmeContent], output_dir: str = "output") -> None:
        """
        Save analysis results to files.
        
        Args:
            username: GitHub username
            repositories: List of repositories
            readme_contents: List of README contents
            output_dir: Directory to save results
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save repository metadata
        repos_file = os.path.join(output_dir, f"{username}_repositories.json")
        repos_data = [
            {
                "name": repo.name,
                "full_name": repo.full_name,
                "description": repo.description,
                "default_branch": repo.default_branch,
                "html_url": repo.html_url,
                "language": repo.language,
                "stars": repo.stars,
                "forks": repo.forks
            }
            for repo in repositories
        ]
        
        with open(repos_file, "w", encoding="utf-8") as f:
            json.dump(repos_data, f, indent=2, ensure_ascii=False)
        
        # Save README contents
        for readme in readme_contents:
            safe_name = "".join(c for c in readme.repository_name if c.isalnum() or c in ('-', '_'))
            readme_file = os.path.join(output_dir, f"{username}_{safe_name}_README.md")
            
            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(f"# {readme.repository_name}\n")
                f.write(f"Repository: {readme.repository_url}\n")
                f.write(f"File: {readme.file_path}\n\n")
                f.write("---\n\n")
                f.write(readme.content)
        
        print(f"Results saved to {output_dir}/")
        print(f"  - Repository metadata: {repos_file}")
        print(f"  - README files: {len(readme_contents)} files")


def main():
    """
    Main function to demonstrate the GitHub analyzer.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze GitHub repositories and extract README files")
    parser.add_argument("username", help="GitHub username to analyze")
    parser.add_argument("--token", help="GitHub personal access token (optional, for higher rate limits)")
    parser.add_argument("--output", default="output", help="Output directory (default: output)")
    
    args = parser.parse_args()
    
    # Initialize analyzer
    analyzer = GitHubAnalyzer(github_token=args.token)
    
    try:
        # Analyze user
        repositories, readme_contents = analyzer.analyze_user(args.username)
        
        # Save results
        analyzer.save_results(args.username, repositories, readme_contents, args.output)
        
        # Print summary
        print(f"\n📊 Summary for {args.username}:")
        print(f"Total repositories: {len(repositories)}")
        print(f"Repositories with README: {len(readme_contents)}")
        
        if repositories:
            languages = [repo.language for repo in repositories if repo.language]
            if languages:
                from collections import Counter
                lang_counts = Counter(languages)
                print(f"Top languages: {', '.join([f'{lang} ({count})' for lang, count in lang_counts.most_common(3)])}")
            
            total_stars = sum(repo.stars for repo in repositories)
            total_forks = sum(repo.forks for repo in repositories)
            print(f"Total stars: {total_stars}")
            print(f"Total forks: {total_forks}")
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
