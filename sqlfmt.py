import sys
import anyio
import dagger


async def test():
    """
    Run sqlfmt on a given dbt project
    """
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        src = client.host().directory("./dbt_project_demo")

        python = (
            client.container()
            .from_("python:3.10-slim-buster")
            .with_mounted_directory("/dbt_project_demo", src)
            .with_workdir("/dbt_project_demo")
            .with_exec(["pip", "install", "shandy-sqlfmt[jinjafmt]"])
            .with_exec(["sqlfmt", "./models", "--diff"])
        )
        # execute
        # await python.stdout()
        await python.exit_code()


if __name__ == "__main__":
    anyio.run(test)
