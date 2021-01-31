import os
from dataclasses import dataclass
from typing import AnyStr


GITHUB_PERSONAL_ACCESS_TOKEN = os.getenv('GITHUB_PERSONAL_ACCESS_TOKEN')


def private_dependency(personal_access_token: AnyStr,
                       repo_user: AnyStr, repo_name: AnyStr,
                       package_name: AnyStr, package_version: AnyStr):
    """Defines a dependency from a private Github repository

    :param personal_access_token:   Github Personal Access Token
    :param repo_user:               Dependency repository user
    :param repo_name:               Dependency repository name
    :param package_name:            Dependency package name
    :param package_version:         Dependency repository release (tag)
    :return:                        The dependency specification for the install_requires field
    """

    return f'{package_name} @ ' \
           f'git+https://{personal_access_token}@github.com/' \
           f'{repo_user}/{repo_name}.git/@{package_version}#egg={package_name}-0'


@dataclass
class Dependency:

    project_name: AnyStr
    package_name: AnyStr
    release_version: AnyStr


DEPENDENCIES = [
    Dependency(project_name='lambda-dispatch-stream', package_name='dispatch_stream', release_version='1.0.0'),
    Dependency(project_name='lambda-geocode-property', package_name='geocode_property', release_version='1.1.0'),
    Dependency(project_name='lambda-fetch-properties', package_name='fetch_properties', release_version='1.1.0')
]
