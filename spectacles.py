import sys
import anyio
import dagger
import os


async def test():
    """
    Run spectacles
    """
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
    
        base_url = os.getenv("LOOKER_BASE_URL")
        client_id = os.getenv("LOOKER_CLIENT_ID")
        client_secret = os.getenv("LOOKER_CLIENT_SECRET")
        project = os.getenv("LOOKER_PROJECT_NAME")
        branch = os.getenv("LOOKER_BRANCH_NAME")

        python = (
            client.container()
            .from_("python:3.10-slim-buster")
            .with_new_file('./config.yaml', f'base_url: {base_url}\nclient_id: {client_id}\nclient_secret: {client_secret}')
            .with_exec(["pip", "install", "spectacles"])
            .with_exec(["spectacles", "connect", "--config-file", "config.yaml"])
            # .with_exec(["spectacles", "sql", "--config-file", "config.yaml", "--project", project, "--branch", branch, "--incremental"])

        )
        # execute
        await python.stdout()

if __name__ == "__main__":
    anyio.run(test)
