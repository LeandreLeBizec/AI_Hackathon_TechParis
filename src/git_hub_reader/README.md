# GitHub Analyzer Tool 🔍

A powerful Python tool to analyze GitHub repositories and extract README files from all public repositories of a given user.

## 🚀 Features

- **Repository Discovery**: Automatically fetches all public repositories for any GitHub user
- **README Extraction**: Intelligently finds and extracts README files from multiple formats (`.md`, `.txt`, `.rst`, etc.)
- **Branch Detection**: Automatically uses the default branch (main, master, or custom)
- **Rate Limiting**: Built-in respect for GitHub API rate limits with automatic delays
- **Token Support**: Optional GitHub token support for higher rate limits (5000 vs 60 requests/hour)
- **Data Export**: Saves results in both JSON (metadata) and individual markdown files
- **Comprehensive Analytics**: Provides detailed statistics about repositories and README content

## 📋 Requirements

- Python 3.7+
- `requests` library
- GitHub account (optional, for personal access token)

## 🛠️ Installation

1. Install the required dependencies:
```bash
pip install requests
```

2. Clone or download the files:
   - `main.py` - Main analyzer class
   - `example.py` - Example usage script

## 🎯 Quick Start

### Command Line Usage

```bash
# Basic usage (rate limited to 60 requests/hour)
python main.py octocat

# With GitHub token for higher rate limits
python main.py octocat --token YOUR_GITHUB_TOKEN

# Custom output directory
python main.py octocat --output my_analysis
```

### Programmatic Usage

```python
from main import GitHubAnalyzer

# Initialize analyzer
analyzer = GitHubAnalyzer()

# Analyze a user
repositories, readme_contents = analyzer.analyze_user("octocat")

# Save results
analyzer.save_results("octocat", repositories, readme_contents)
```

## 🔧 Configuration

### GitHub Personal Access Token (Recommended)

For better rate limits (5000 requests/hour vs 60), create a GitHub personal access token:

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Select scopes: `public_repo` (for public repositories)
4. Copy the generated token

Use the token in one of these ways:

```bash
# Method 1: Command line argument
python main.py username --token YOUR_TOKEN

# Method 2: Environment variable
export GITHUB_TOKEN=YOUR_TOKEN
python main.py username

# Method 3: Programmatically
analyzer = GitHubAnalyzer(github_token="YOUR_TOKEN")
```

## 📊 Output Structure

The tool generates the following outputs:

```
output/
├── username_repositories.json          # Repository metadata
├── username_repo1_README.md           # Individual README files
├── username_repo2_README.md
└── ...
```

### Repository Metadata (JSON)
```json
[
  {
    "name": "repository-name",
    "full_name": "username/repository-name",
    "description": "Repository description",
    "default_branch": "main",
    "html_url": "https://github.com/username/repository-name",
    "language": "Python",
    "stars": 42,
    "forks": 7
  }
]
```

### README Files
Each README file includes:
- Repository name and URL
- Original file path
- Complete README content

## 🔍 How It Works

1. **Extract GitHub Username**: Takes a username as input
2. **List Public Repositories**: Uses GitHub API to fetch all public repos
3. **For Each Repository**:
   - Attempts to find README files in various formats
   - Tries common names: `README.md`, `readme.md`, `README`, etc.
   - Uses the repository's default branch
   - Decodes base64 content from GitHub API
4. **Save Results**: Exports data in structured formats

## 📈 Analytics Provided

- Total repository count
- README success rate
- Programming language distribution
- Star and fork statistics
- README content statistics (length, etc.)
- Top repositories by popularity

## ⚡ Performance Features

- **Pagination**: Handles users with many repositories
- **Rate Limiting**: Automatic delays to respect API limits
- **Error Handling**: Graceful handling of missing files or API errors
- **Efficient Requests**: Minimal API calls with session reuse

## 🎨 Example Output

```
🔍 Analyzing GitHub user: octocat
==================================================
Fetching repositories for user: octocat
Found 8 repositories
Processing repository 1/8: Hello-World
  ✓ README found (1337 characters)
Processing repository 2/8: Spoon-Knife
  ✓ README found (856 characters)
...

Analysis complete!
Total repositories: 8
Repositories with README: 6

📊 Summary for octocat:
Total repositories: 8
Repositories with README: 6
Top languages: JavaScript (3), HTML (2), C (1)
Total stars: 2847
Total forks: 1234
```

## 🚨 Rate Limits

| Authentication | Rate Limit | Recommended For |
|---------------|------------|-----------------|
| No Token | 60 requests/hour | Small analyses (<50 repos) |
| Personal Token | 5000 requests/hour | Large analyses, production use |

## 🛡️ Error Handling

The tool handles various scenarios gracefully:
- Non-existent users
- Private repositories (skipped)
- Missing README files
- API rate limit exceeded
- Network connectivity issues
- Malformed repository data

## 🔄 Supported README Formats

- `README.md` / `readme.md`
- `README.MD`
- `README` / `readme`
- `README.txt` / `readme.txt`
- `README.rst` / `readme.rst`

## 🤝 Contributing

Feel free to contribute by:
- Adding support for more file formats
- Improving error handling
- Adding new analytics features
- Optimizing performance

## 📄 License

This tool is provided as-is for educational and analysis purposes. Please respect GitHub's Terms of Service and API usage guidelines.

## 🔗 Related Resources

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [GitHub API Rate Limiting](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting) 