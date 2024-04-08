import git
from datetime import datetime, timezone
import requests
from datetime import datetime
import re
from packaging import version


def get_commit_timestamp(repo_path, commit_hash):
    try:
        repo = git.Repo(repo_path)
        commit = repo.commit(commit_hash)
        timestamp = commit.committed_date
        return timestamp
    except git.InvalidGitRepositoryError:
        print("Invalid Git repository.")
    except git.BadName:
        print("Invalid commit hash.")



def get_package_version(package_name, date):
    date = datetime.strptime(date, '%Y-%m-%d')
    url = f'https://pypi.org/pypi/{package_name}/json'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        releases = data['releases']
        new_releases = dict(sorted(releases.items(), key=lambda item: version.parse(item[0]), reverse=True))
        for version_, release_info in new_releases.items():
            for file_info in release_info:
                upload_time = file_info['upload_time']
                upload_time = datetime.strptime(upload_time, '%Y-%m-%dT%H:%M:%S')
                if upload_time <= date:
                    return version_

        return None
    else:
        raise Exception(f'Failed to fetch package information for {package_name}')
    

def get_dependencies_from_requirements(file_path):
    dependencies = []
    with open(file_path, 'r') as file:
        for line in file:
            # Use regex to match lines containing package names in requirements.txt format
            match = re.match(r'^\s*([a-zA-Z0-9_-]+)\s*(?:==.*|\n)?$', line)
            if match:
                dependencies.append(match.group(1))
    return dependencies
