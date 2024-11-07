from urllib import request
from project import Project
import toml


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        data = toml.loads(content)

        poetry_data = data.get("tool", {}).get("poetry", {})

        name = poetry_data.get("name", "Unknown Project Name")
        description = poetry_data.get("description", "No description provided.")
        license = poetry_data.get("license", "No license provided")
        authors = poetry_data.get("authors", [])

        dependencies = list(poetry_data.get("dependencies", {}).keys())
        dev_dependencies = list(
            poetry_data.get("group", {}).get("dev", {}).get("dependencies", {}).keys()
        )

        return Project(name, description, license, authors, dependencies, dev_dependencies)

