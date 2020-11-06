"""Define classes which control the environment of a project."""
from abc import ABC, abstractmethod
import logging
import os
import subprocess
from typing import Optional


# naive configuration of logging module
logging.basicConfig(level=logging.INFO)


class Environment(ABC):
    """Abstract class for environments management."""

    @abstractmethod
    def check_environment(self) -> bool:
        """Check environment.

        Check if all required tools are available.

        Returns:
            bool: verification result.

        """
        return True

    @abstractmethod
    def setup_environment(self) -> None:
        """Setup environment."""
        pass

    def _is_tool_available(self, tool: str) -> bool:
        """Check if a single tool is available as a shell command.

        Args:
            tool (str): tool command.

        Returns:
            bool: verification result.

        """
        tool_availability = subprocess.check_output(["command", "-v", tool])
        if tool_availability:
            msg = f"{tool} available."
            logging.info(msg)
            return True
        else:
            msg = f"Please install: {tool}."
            logging.info(msg)
            return False


class ModernPythonEnviroment(Environment):
    """Manage environment of a project using ``modern_python`` template."""

    required_tools = [
        "git",
        "nox",
        "poetry",
        "pyenv",
    ]
    required_dev_packages = [
        "pytest",
        "coverage",
        "pytest-cov",
        "pytest-mock",
        "flake8",
        "black",
        "flake8-black",
        "flake8-import-order",
        "flake8-bugbear",
        "flake8-bandit",
        "safety",
        "mypy",
        "flake8-annotations",
        "typeguard",
        "flake8-docstrings",
        "darglint",
        "xdoctest",
        "sphinx",
        "sphinx-autodoc-typehints",
        "codecov",
    ]

    def __init__(
        self, project_name: str, python_version: Optional[str] = "3.8.2"
    ) -> None:
        """Initialize class.

        Args:
            project_name (str): project name.
            python_version (str, optional): python version.
                Defaults to "3.8.2".

        """
        self.project_name = project_name
        self.python_version = python_version

    def check_environment(self) -> bool:
        """Check if an environment can be created.

        It requires all tools listed in ``self.required_tools`` to be
        available in a current evironment.

        Returns:
            bool: status.

        """
        tools_availability = []
        for tool in self.required_tools:
            status = self._is_tool_available(tool)
            tools_availability.append(status)
        return all(tools_availability)

    def setup_environment(self) -> None:
        """Setup project environment.

        Raises:
            FileNotFoundError: if project directory does not exists.

        """
        if not os.path.exists(os.path.join("./", self.project_name)):
            raise FileNotFoundError("Project directory doesn't exist.")
        os.chdir(os.path.join("./", self.project_name))
        subprocess.call(["pyenv", "local", self.python_version])
        subprocess.call(["git", "init"])
        subprocess.call(["pre-commit", "install"])
        for dev_package in self.required_dev_packages:
            subprocess.call(["poetry", "add", "--dev", dev_package])
        subprocess.call(["poetry", "install"])
        subprocess.call(["poetry", "run", self.project_name])
