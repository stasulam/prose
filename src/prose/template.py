"""Define classes to convert predefined templates into Python projects."""
from abc import ABC, abstractmethod
import os
import shutil
import string
from typing import List, Optional

import prose


class Template(ABC):
    """Define abstract class for templates."""

    def __init__(
        self,
        project_name: str,
        template_name: str,
        template_type: str,
        overwrite: Optional[bool] = False,
    ) -> None:
        """Abstract template of a project initialized with ``prose``.

        Args:
            project_name (str): project name. It will define Python package
                name or name of a Machine Learning project.
            template_name (str): template name. It will define one of the
                templates available in ``prose``.
            template_type (str): template type. Chose between a pattern
                for a package or a model.
            overwrite (bool, optional): replace if directory already exists.
                Defaults to False.

        """
        template_dir = os.path.join(prose.__path__[0], "templates/")
        self.project_name = project_name
        self.source = os.path.join(template_dir, template_type, template_name)
        self.destination = project_name
        self.overwrite = overwrite

    @abstractmethod
    def start_project(self) -> None:
        """Start project."""
        pass

    def _extract_template_files(self) -> None:
        """Extract template's resources.

        Template's resources will be extracted in a directory
        defined in ``self.destination``. In this case, it will
        be a directory with the same name as a project.

        Raises:
            FileNotFoundError: if directory does not exist.

        """
        if os.path.exists(self.destination):
            if self.overwrite:
                shutil.rmtree(self.destination)
            else:
                raise FileNotFoundError(
                    "Project was already initialized. "
                    "In order to overwrite existing project "
                    "use ``--overwrite`` option."
                )
        shutil.copytree(src=self.source, dst=self.destination)

    def _list_template_files(self) -> List[str]:
        """List template's resources.

        List all of the files that was extracted from template's resources.
        This will will be modified with user provided arguments.

        Returns:
            List[str]: list consisting all of the template's resources.

        """
        template_files = []
        for dirname, dirnames, filenames in os.walk(self.destination):
            if "__pycache__" in dirnames:
                dirnames.remove("__pycache__")
            for filename in filenames:
                template_files.append(os.path.join(dirname, filename))
        return template_files

    @staticmethod
    def _modify_template_file(path: str, **kwargs: dict) -> None:
        """Modify single template file.

        Fill a single template file with user-defined arguments.

        Args:
            path (str): path to file.
            **kwargs (dict): pass arguments as a dictionary.
                It will fill a given template file.

        Raises:
            ValueError: if filling template with a given argument
                was impossible.

        """
        with open(path, "rb") as file:
            raw = file.read().decode("utf-8")
        try:
            content = string.Template(raw).substitute(**kwargs)
        except ValueError:
            raise ValueError(f"Filling template: {path} failed.")
        render_path = path[: -len(".tmpl")] if path.endswith(".tmpl") else path
        if path.endswith(".tmpl"):
            os.rename(path, render_path)
        with open(render_path, "wb") as file:
            file.write(content.encode("utf-8"))


class PackageTemplate(Template):
    """Define template for a Python package."""

    def __init__(
        self, project_name: str, template_name: str, overwrite: Optional[bool] = False
    ) -> None:
        """Python package template.

        Args:
            project_name (str): project name. This will be the package name.
            template_name (str): template_name. The available patterns are
                available in: ``templates/packages/``.
            overwrite (bool, optional): replace if directory already exists.
                Defaults to False.

        """
        super().__init__(
            project_name=project_name,
            template_name=template_name,
            template_type="packages",
            template_dir=os.path.join(prose.__path__[0], "templates"),
            overwrite=overwrite,
        )

    def start_project(self, **kwargs: dict) -> None:
        """Start Python package project."""
        self._extract_template_files()
        template_files = self._list_template_files()
        for template_file in template_files:
            self._modify_template_file(
                template_file, project_name=self.project_name, **kwargs
            )
        # rename main package directory
        os.rename(
            src=os.path.join(self.destination, "src/project_name"),
            dst=os.path.join(self.destination, f"src/{self.project_name}"),
        )


class ModelTemplate(Template):
    """Machine learning model template."""

    pass
