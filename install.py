import pip
from data_processing_stack.dependencies import GITHUB_PERSONAL_ACCESS_TOKEN, private_dependency, DEPENDENCIES


if __name__ == '__main__':

    for dependency in DEPENDENCIES:
        uri = private_dependency(
            personal_access_token=GITHUB_PERSONAL_ACCESS_TOKEN,
            repo_user='reloc8', repo_name=dependency.project_name,
            package_name=dependency.package_name, package_version=dependency.release_version
        )
        location = f'stack/lambda/{dependency.package_name}/{dependency.release_version}/python'
        args = ['install', uri, '-t', location]
        pip.main(args=args)
