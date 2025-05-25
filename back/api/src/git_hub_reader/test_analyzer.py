#!/usr/bin/env python3
"""
Test script for the GitHub Analyzer tool.

This script runs basic tests to ensure the analyzer is working correctly.
"""

import sys
import os
from main import GitHubAnalyzer, Repository, ReadmeContent


def test_analyzer_initialization():
    """Test that the analyzer can be initialized properly."""
    print("Testing analyzer initialization...")
    
    # Test without token
    analyzer = GitHubAnalyzer()
    assert analyzer.base_url == "https://api.github.com"
    assert "Accept" in analyzer.session.headers
    print("✓ Analyzer initialization without token works")
    
    # Test with token
    test_token = "test_token_123"
    analyzer_with_token = GitHubAnalyzer(github_token=test_token)
    assert "Authorization" in analyzer_with_token.session.headers
    print("✓ Analyzer initialization with token works")


def test_data_classes():
    """Test that the data classes work correctly."""
    print("\nTesting data classes...")
    
    # Test Repository class
    repo = Repository(
        name="test-repo",
        full_name="user/test-repo",
        description="A test repository",
        default_branch="main",
        html_url="https://github.com/user/test-repo",
        language="Python",
        stars=42,
        forks=7
    )
    assert repo.name == "test-repo"
    assert repo.stars == 42
    print("✓ Repository data class works")
    
    # Test ReadmeContent class
    readme = ReadmeContent(
        repository_name="test-repo",
        repository_url="https://github.com/user/test-repo",
        content="# Test README\n\nThis is a test.",
        encoding="base64",
        file_path="README.md"
    )
    assert readme.repository_name == "test-repo"
    assert "Test README" in readme.content
    print("✓ ReadmeContent data class works")


def test_github_api_connection():
    """Test that we can connect to the GitHub API."""
    print("\nTesting GitHub API connection...")
    
    analyzer = GitHubAnalyzer()
    
    try:
        # Test with a known user that should exist
        repositories = analyzer.get_user_repositories("octocat")
        
        if repositories:
            print(f"✓ Successfully fetched {len(repositories)} repositories for octocat")
            
            # Test README fetching on the first repository
            first_repo = repositories[0]
            readme = analyzer.get_readme_content(first_repo)
            
            if readme:
                print(f"✓ Successfully fetched README from {first_repo.name} ({len(readme.content)} characters)")
            else:
                print(f"⚠ No README found in {first_repo.name} (this is normal)")
        else:
            print("⚠ No repositories found for octocat (this might indicate API issues)")
            
    except Exception as e:
        print(f"❌ GitHub API connection test failed: {e}")
        print("This might be due to rate limiting or network issues.")
        return False
    
    return True


def test_file_operations():
    """Test file saving operations."""
    print("\nTesting file operations...")
    
    # Create test data
    test_repo = Repository(
        name="test-repo",
        full_name="testuser/test-repo",
        description="A test repository",
        default_branch="main",
        html_url="https://github.com/testuser/test-repo",
        language="Python",
        stars=1,
        forks=0
    )
    
    test_readme = ReadmeContent(
        repository_name="test-repo",
        repository_url="https://github.com/testuser/test-repo",
        content="# Test Repository\n\nThis is a test README file.",
        encoding="base64",
        file_path="README.md"
    )
    
    analyzer = GitHubAnalyzer()
    test_output_dir = "test_output"
    
    try:
        # Test saving results
        analyzer.save_results("testuser", [test_repo], [test_readme], test_output_dir)
        
        # Check if files were created
        import json
        
        # Check JSON file
        json_file = os.path.join(test_output_dir, "testuser_repositories.json")
        if os.path.exists(json_file):
            with open(json_file, 'r') as f:
                data = json.load(f)
                assert len(data) == 1
                assert data[0]["name"] == "test-repo"
            print("✓ Repository JSON file created successfully")
        else:
            print("❌ Repository JSON file not created")
            return False
        
        # Check README file
        readme_file = os.path.join(test_output_dir, "testuser_test-repo_README.md")
        if os.path.exists(readme_file):
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert "Test Repository" in content
            print("✓ README file created successfully")
        else:
            print("❌ README file not created")
            return False
        
        # Clean up test files
        import shutil
        if os.path.exists(test_output_dir):
            shutil.rmtree(test_output_dir)
        print("✓ Test files cleaned up")
        
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False
    
    return True


def main():
    """Run all tests."""
    print("🧪 Running GitHub Analyzer Tests")
    print("=" * 50)
    
    tests = [
        test_analyzer_initialization,
        test_data_classes,
        test_file_operations,
        test_github_api_connection,  # This one last as it requires internet
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            result = test()
            if result is not False:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"🧪 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The GitHub Analyzer is ready to use.")
        return 0
    else:
        print("⚠ Some tests failed. Please check the output above.")
        return 1


if __name__ == "__main__":
    exit(main()) 