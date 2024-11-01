from dotenv import load_dotenv
load_dotenv(override=True)
#from workflow import run

#run()

from docker_folder.docker_utils import DockerUtils

container_name = "test_name"
DockerUtils.bash(container_name, "touch file1")

DockerUtils.stop(container_name)