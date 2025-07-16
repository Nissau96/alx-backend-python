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
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = {"name": org_name}
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, {"name": org_name})
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """
        Test the _public_repos_url property.
        """
        known_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }
        with patch.object(GithubOrgClient,
                          'org',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = known_payload
            client = GithubOrgClient("google")
            expected_url = known_payload["repos_url"]
            self.assertEqual(client._public_repos_url, expected_url)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test the public_repos method.
        """
        repos_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = repos_payload

        with patch.object(GithubOrgClient,
                          '_public_repos_url',
                          new_callable=PropertyMock) as mock_public_repos_url:
            test_url = "https://api.github.com/orgs/test/repos"
            mock_public_repos_url.return_value = test_url
            client = GithubOrgClient("test")
            self.assertEqual(client.public_repos(), ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test the has_license static method.
        """
        has_license_result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(has_license_result, expected)


@parameterized_class([
    "org_payload", "repos_payload", "expected_repos", "apache2_repos"
], TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the GithubOrgClient class using fixtures.
    """

    @classmethod
    def setUpClass(cls):
        """Set up the class fixture by patching requests.get."""
        def side_effect(url):
            mock_response = Mock()
            org_url = "https://api.github.com/orgs/google"
            repos_url = "https://api.github.com/orgs/google/repos"
            if url == org_url:
                mock_response.json.return_value = cls.org_payload
            elif url == repos_url:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.status_code = 404
            return mock_response

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class fixture by stopping the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos method against fixtures.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos method with license filter against fixtures.
        """
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
