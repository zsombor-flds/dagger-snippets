import anyio
import sys
from dagger import Connection, Config, Container, Socket
from datetime import datetime

async def main():
    ''' Build a docker container'''
    cfg = Config(log_output=sys.stderr)
    
    async with Connection(cfg) as dagger_client:
        docker_host: Socket = dagger_client.host().unix_socket("/var/run/docker.sock")
        src = dagger_client.host().directory("./docker_demo")

        # example server container
        server: Container = (
                dagger_client.container()
                .from_("docker:dind")
                    .with_unix_socket("/var/run/docker.sock", docker_host)
                    .with_env_variable("CACHEBUSTER", datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
                     .with_mounted_directory("/docker_demo", src)
                    .with_workdir("/docker_demo/")
                    .with_exec(["ls"])
                    .with_exec(["docker", "build", "-t", "test", "."]) #TODO param

                )
        # execute
        await server.stdout()
    

if __name__ == "__main__":
    anyio.run(main)