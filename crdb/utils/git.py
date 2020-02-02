from django.conf import settings
from django.utils.timezone import localtime, now
from django.core.exceptions import ImproperlyConfigured

from github import Github
from github.GithubException import UnknownObjectException


class GitHubFile:

    def __init__(self, data_file: str) -> None:
        self.data_file = data_file

        self.github_token = getattr(settings, 'GITHUB_TOKEN', None)
        if not self.github_token:
            raise ImproperlyConfigured("Missing GITHUB_TOKEN setting.")

        self.github_repo = getattr(settings, 'GITHUB_REPO', None)
        if not self.github_repo:
            raise ImproperlyConfigured("Missing GITHUB_REPO setting.")

        self._api = Github(self.github_token)
        self._repo = self._api.get_repo(self.github_repo)

    def get_sha(self) -> str:
        try:
            contents = self._repo.get_contents(self.data_file)
            return contents.sha
        except UnknownObjectException:
            pass
        return ""

    def update(self, new_content) -> bool:
        ts = str(localtime(now()))
        commit_msg = f"Data export {ts}"
        sha = self.get_sha()
        commit = self._repo.update_file(self.data_file, commit_msg, new_content, sha)
        return True
