#!/usr/bin/env python3
"""
Example usage of the GitHub Analyzer tool.

This script demonstrates how to use the GitHubAnalyzer class to:
1. Fetch all public repositories for a user
2. Extract README files from each repository
3. Save the results to files
"""

from main import GitHubAnalyzer
import os


def analyze_github_user(username: str, github_token: str = None, output_dir: str = "output"):
    """
    Analyze a GitHub user and extract all README files from their repositories.
    
    Args:
        username: GitHub username to analyze
        github_token: Optional GitHub personal access token for higher rate limits
        output_dir: Directory to save results
    """
    print(f"🔍 Analyzing GitHub user: {username}")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = GitHubAnalyzer(github_token=github_token)
    
    try:
        # Analyze the user
        repositories, readme_contents = analyzer.analyze_user(username)
        
        # Save results to files
        analyzer.save_results(username, repositories, readme_contents, output_dir)
        
        # Print detailed summary
        print("\n" + "=" * 50)
        print(f"📊 Analysis Summary for {username}")
        print("=" * 50)
        
        print(f"Total repositories found: {len(repositories)}")
        print(f"Repositories with README: {len(readme_contents)}")
        print(f"Success rate: {len(readme_contents)/len(repositories)*100:.1f}%" if repositories else "N/A")
        
        if repositories:
            # Language statistics
            languages = [repo.language for repo in repositories if repo.language]
            if languages:
                from collections import Counter
                lang_counts = Counter(languages)
                print(f"\n📈 Top Programming Languages:")
                for lang, count in lang_counts.most_common(5):
                    print(f"  {lang}: {count} repositories")
            
            # Repository statistics
            total_stars = sum(repo.stars for repo in repositories)
            total_forks = sum(repo.forks for repo in repositories)
            print(f"\n⭐ Total stars across all repositories: {total_stars}")
            print(f"🍴 Total forks across all repositories: {total_forks}")
            
            # Top repositories by stars
            top_repos = sorted(repositories, key=lambda r: r.stars, reverse=True)[:5]
            print(f"\n🏆 Top repositories by stars:")
            for repo in top_repos:
                print(f"  {repo.name}: {repo.stars} ⭐ ({repo.language or 'Unknown'})")
        
        # README statistics
        if readme_contents:
            total_chars = sum(len(readme.content) for readme in readme_contents)
            avg_chars = total_chars / len(readme_contents)
            print(f"\n📄 README Statistics:")
            print(f"  Total characters: {total_chars:,}")
            print(f"  Average README length: {avg_chars:.0f} characters")
            
            # Longest READMEs
            longest_readmes = sorted(readme_contents, key=lambda r: len(r.content), reverse=True)[:3]
            print(f"  Longest READMEs:")
            for readme in longest_readmes:
                print(f"    {readme.repository_name}: {len(readme.content):,} characters")
        
        print(f"\n💾 Results saved to: {output_dir}/")
        print(f"  - Repository metadata: {username}_repositories.json")
        print(f"  - Individual README files: {len(readme_contents)} files")
        
        return repositories, readme_contents
        
    except Exception as e:
        print(f"❌ Error analyzing user {username}: {e}")
        return None, None


def main():
    """
    Main function with example usage.
    """
    # Example 1: Analyze a popular GitHub user (without token)
    print("Example 1: Analyzing without GitHub token (rate limited)")
    username = "octocat"  # GitHub's mascot account
    repositories, readme_contents = analyze_github_user(username)
    
    if repositories:
        print(f"\n✅ Successfully analyzed {username}!")
    else:
        print(f"\n❌ Failed to analyze {username}")
    
    print("\n" + "="*70)
    
    # Example 2: Show how to use with a GitHub token (commented out)
    print("Example 2: Using with GitHub token (uncomment to use)")
    print("""
    # To use with a GitHub token for higher rate limits:
    # 1. Create a personal access token at: https://github.com/settings/tokens
    # 2. Set it as an environment variable: export GITHUB_TOKEN=your_token_here
    # 3. Uncomment the following lines:
    
    # github_token = os.getenv('GITHUB_TOKEN')
    # if github_token:
    #     username = "torvalds"  # Example: Linus Torvalds
    #     repositories, readme_contents = analyze_github_user(username, github_token)
    # else:
    #     print("No GitHub token found in environment variable GITHUB_TOKEN")
    """)
    
    # Example 3: Programmatic usage
    print("\nExample 3: Programmatic usage")
    print("""
    # You can also use the analyzer programmatically:
    
    from main import GitHubAnalyzer
    
    analyzer = GitHubAnalyzer()
    repositories = analyzer.get_user_repositories("username")
    
    for repo in repositories:
        readme = analyzer.get_readme_content(repo)
        if readme:
            print(f"README from {repo.name}: {len(readme.content)} characters")
    """)


if __name__ == "__main__":
    main() 