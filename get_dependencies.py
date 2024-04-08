from datetime import datetime, timezone
from gitread import get_dependencies_from_requirements, get_commit_timestamp, get_package_version

requirements_file = 'requirements.txt'
dependency_names = get_dependencies_from_requirements(requirements_file)

repo_path = "Path To cloned Repo"
commit_hash = "Commit Hash of which dependencies you want to find out" 
timestamp = get_commit_timestamp(repo_path, commit_hash)

if timestamp:
    timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc)
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')
    date_str = formatted_timestamp.split(' ')[0]
    print(f"Timestamp of commit {commit_hash}: {formatted_timestamp}")
    
    for package_name in dependency_names:
        version_ = get_package_version(package_name, date_str)
        if version_:
            print(f'The version of {package_name} at {date_str} was {version_}')
        else:
            print(f'No suitable version of {package_name} was found before {date_str}')