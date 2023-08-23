import os
import sys

import setuptools

workspace_directory = os.path.abspath(os.path.join("..", ".."))
automation_setup_directory = os.path.join(workspace_directory, "Automation", "Setup")

sys.path.insert(0, automation_setup_directory)

import automation_helpers # pylint: disable = wrong-import-position


def run_setup() -> None:
    project_configuration = automation_helpers.load_project_configuration(workspace_directory)

    resource_patterns = [
        'static/**/*.css',
        'static/**/*.jpeg',
        'templates/**/*.html',
    ]

    setuptools.setup(
		name = "benjaminhamon-portal-website",
		description = "Website for www.benjaminhamon.com",
        version = project_configuration["ProjectVersionFull"],
        author = project_configuration["Author"],
        author_email = project_configuration["AuthorEmail"],
        url = project_configuration["ProjectUrl"],
        packages = setuptools.find_packages(include = [ "benjaminhamon_portal_website", "benjaminhamon_portal_website.*" ]),
        python_requires = "~= 3.9",

        install_requires = [
            "Flask ~= 2.3.2",
        ],

        package_data = {
            "benjaminhamon_portal_website": automation_helpers.list_package_data("benjaminhamon_portal_website", resource_patterns),
        },
    )


run_setup()
