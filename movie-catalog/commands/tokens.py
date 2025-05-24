from typing import Annotated

import typer
from rich import print
from rich.box import MARKDOWN
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens as tokens

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
) -> None:
    """
    Check of the passed token is valid - exists or not.
    """
    print(
        f"Token: [bold]{token}[/bold]",
        (
            "[green]exists[/green]."
            if tokens.token_exists(token)
            else "[red]doesn't exist[/red]."
        ),
    )


@app.command(name="list")
def list_tokens() -> None:
    """
    Get list of all tokens.
    """
    print(Markdown("# List of all available tokens."))
    for idx, token in enumerate(tokens.get_tokens(), start=1):
        print(f"{idx}. [bold]{token}[/bold]")


@app.command()
def create() -> None:
    """
    Create a new token and save it to db.
    """
    token = tokens.generate_and_save_token()
    print(f"Token: [bold green]{token}[/bold green] created and saved to db.")


@app.command()
def add(token: str) -> None:
    """
    Add a new token to db.
    """
    tokens.add_token(token)
    print(f"Token: [bold green]{token}[/bold green] saved to db.")


@app.command(name="rm")
def delete(token: str) -> None:
    """
    Delete a token from db.
    """
    if not tokens.token_exists(token):
        print(f"Token: [bold red]{token}[/bold red] not found.")
        return

    tokens.delete_token(token)
    print(f"Token: [bold red]{token}[/bold red] deleted from db.")
