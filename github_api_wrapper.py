# github_api_wrapper.py

import requests

class GitHubAPIWrapper:
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.github.com"

    def _make_request(self, url: str) -> dict:
        headers = {"Authorization": f"token {self.api_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(
                f"GitHub API request failed: {response.status_code} {response.text}\n"
                f"URL: {url}\n"
                f"Headers: {headers}"
            )

    return response.json()


    def get_repo_info(self, owner: str, repo: str, subdir: str = None) -> dict:
        if subdir:
            url = f"{self.base_url}/repos/{owner}/{repo}/contents/{subdir}"
        else:
            url = f"{self.base_url}/repos/{owner}/{repo}"

        return self._make_request(url)
