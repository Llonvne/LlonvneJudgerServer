from Entities import RunnerRequest
from abstract.DockerBasedStandardRunner import DockerBasedStandardRunner


class GenericPython3Runner(DockerBasedStandardRunner):
    def __init__(self, python_version: str):
        self.version = python_version
        super().__init__(f"python{python_version}_runner", f"FROM python:{python_version}")

    def get_command(self, request: RunnerRequest):
        return f" python ./target/{request.submission_id}/{request.submission_id}.py"

    def get_version(self) -> str:
        return self.version
