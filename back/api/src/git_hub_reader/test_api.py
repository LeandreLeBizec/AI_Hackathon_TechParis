from dotenv import load_dotenv
import requests
import os
load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

from main import GitHubAnalyzer

analyzer = GitHubAnalyzer(github_token)
repositories, readme_contents = analyzer.analyze_user("ThomasTaylor14")
analyzer.save_results("ThomasTaylor14", repositories, readme_contents)

print(repositories)
print(readme_contents)
    