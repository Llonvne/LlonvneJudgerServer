import abc
import subprocess

import docker


class DockerBased(abc.ABC):
    def __init__(self, imageName: str, dockerfile: str):
        self.imageName = imageName
        self.dockerfile = dockerfile
        self.resolve_image_dependency(imageName, dockerfile)

    def run_docker(self, command):
        self.resolve_image_dependency(self.imageName, self.dockerfile)
        compile_command = f"docker run -i --rm -v $(pwd):/src -w /src {self.imageName} {command}"
        program = subprocess.Popen(compile_command, shell=True, text=True, stderr=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        return program

    @staticmethod
    def resolve_image_dependency(imageName: str, file: str):
        client = docker.from_env()
        # 检查镜像是否存在
        if client.images.list(name=imageName):
            print(f"检测到所需到 {imageName} 镜像")
        else:
            print(f"未检测到所需到 {imageName} 镜像，开始构建")
            dockerfile = f"""docker build -t {imageName} - <<EOF \n{file}\nEOF"""
            subprocess.run(dockerfile, shell=True, text=True, stderr=subprocess.PIPE)
            if not client.images.list(name=f"{imageName}"):
                print("构建镜像失败")
            else:
                print("构建镜像成功")
