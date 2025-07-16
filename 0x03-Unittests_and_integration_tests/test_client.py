#!/usr/bin/env python3
"""
Unit and Integration tests for client.py
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Task 4: Test that GithubOrgClient.org returns the correct value.
        """
        # Set a dummy return value for the mocked get_json
        mock_get_json.return_value = {"name": org_name}

        # Instantiate the client
        client = GithubOrgClient(org_name)

        # Call the org property
        result = client.org

        # Assert get_json was called once with the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert the result is correct
        self.assertEqual(result, {"name": org_name})

    def test_public_repos_url(self):
        """
        Task 5: Test the _public_repos_url property.
        """
        # The known payload for the org
        known_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch GithubOrgClient.org to return the known payload
        with patch.object(GithubOrgClient,
                          'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url

            # Assert the result is the expected repos_url
            self.assertEqual(result, known_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Task 6: Test the public_repos method.
        """
        # Define a payload for get_json to return
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": None}
        ]
        mock_get_json.return_value = repos_payload

        # Mock the _public_repos_url property
        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/test/repos"

            client = GithubOrgClient("test")
            result = client.public_repos()

            # Expected list of repo names
            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)

            # Assert the mocked property and get_json were called once
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("https://api.github.com/orgs/test/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Task 7: Test the has_license static method.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class using fixtures.
    """

    @classmethod
    def setUpClass(cls):

        # This side_effect function will return a different mock response
        # based on the URL it receives.
        def side_effect(url):
            mock_response = Mock()
            if url == f"https://api.github.com/orgs/google":
                mock_response.json.return_value = cls.org_payload
            elif url == "https://api.github.com/orgs/google/repos":
                mock_response.json.return_value = cls.repos_payload
            else:
                # Return a 404 for any other URL
                mock_response.status_code = 404
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):

        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Task 8: Test public_repos method in an integration-like manner.
        """
        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Task 8: Test public_repos with a license filter.
        """
        client = GithubOrgClient("google")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()