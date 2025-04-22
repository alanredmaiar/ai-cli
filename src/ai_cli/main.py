import asyncio
import warnings

from ai_cli.asyn import async_click as click
from ai_cli.commands.log import log
from ai_cli.settings import settings as st


def main():
    """Entry point for the application."""
    warnings.filterwarnings("ignore", message="coroutine '.*' was never awaited")

    @click.group(name=st.PYPROJECT["project"]["name"])
    @click.version_option(st.PYPROJECT["project"]["version"])
    @click.pass_context
    async def app(ctx):
        pass

    app.add_command(log)
    asyncio.run(app())


if __name__ == "__main__":
    main()
