from typing import Annotated

import typer
from rich import print
from rich.box import MARKDOWN
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="token",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Tokens management.",
)


@app.command()
def check(
    token: Annotated[
        str,
        typer.Argument(help="The token to check"),
    ],
):
    """
    Check of the passed token is valid - exists or not.
    """
    print(
        f"Token: [bold]{token}[/bold]",
        (
            "[green]exists[/green]."
            if redis_tokens.token_exists(token)
            else "[red]doesn't exist[/red]."
        ),
    )


@app.command(name="list")
def list_tokens():
    """
    Get list of all tokens.
    """
    print(Markdown("# List of all available tokens."))
    for idx, token in enumerate(redis_tokens.get_tokens(), start=1):
        print(f"{idx}. [bold]{token}[/bold]")
