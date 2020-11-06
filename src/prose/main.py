"""Define main function."""
from typing import Optional

import click

from .env import ModernPythonEnviroment
from .exceptions import ToolNotFoundError
from .template import PackageTemplate


@click.command()
@click.option("--project_name")
@click.option("--project_type")
@click.option("--template_name")
@click.option("--python_version", default="3.8.2")
def main(
    project_name: str,
    project_type: str,
    template_name: str,
    python_version: Optional[str] = "3.8.2",
) -> None:
    """Initialize new Python project.

    Args:
        project_name (str): define project name.
        project_type (str): define project typ. Available types are:
            ``package`` and ``model``. ``package`` type is dedicated
            for new Python packages, while ``model`` should be used
            for development of machine learning models.
        template_name (str): define template name.
        python_version (str): Python version.

    Raises:
        NotImplementedError: raises when project_type is not
            available at the moment.
        ToolNotFoundError: raises when required tool is not
            available in an environment.

    """
    template_params = {"project_name": project_name, "template_name": template_name}
    if project_type == "package":
        template = PackageTemplate(**template_params)
        template.start_project()
        if template_name == "modern_python":
            env = ModernPythonEnviroment(
                project_name=project_name, python_version=python_version
            )
            tools_availability = env.check_environment()
            if not tools_availability:
                raise ToolNotFoundError("Please install required tools.")
            env.setup_environment()
    if project_type == "model":
        raise NotImplementedError(
            "At this moment templates dedicated for ML models " "are not implemented."
        )


if __name__ == "__main__":
    main()
