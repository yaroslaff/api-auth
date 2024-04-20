import typer
import click
from rich.console import Console
from typing_extensions import Annotated

from ..models import User, Code
from ..db import SessionLocal
from ..cron import cron

err_console = Console(stderr=True)

panel_local="Local commands"

app = typer.Typer(pretty_exceptions_show_locals=False, 
    # rich_markup_mode="rich"
    no_args_is_help=True,                
    rich_markup_mode="markdown"
    )
err_console = Console(stderr=True)



@app.callback(
        context_settings={"help_option_names": ["-h", "--help"]})
def callback(ctx: typer.Context,
    ):
    """
    Client for FastAPI Simple Auth
    """
    global db
    
    db = SessionLocal()


@app.command(rich_help_panel=panel_local,
             help='List all users')
def users():
    for user in db.query(User).all():
        print(user)

@app.command(rich_help_panel=panel_local,
             help='List all codes')
def codes():
    for code in db.query(Code).all():
        print(code)

@app.command("cron", rich_help_panel=panel_local,
             help='Run cron job once')
def clicron():
    cron(force=True)

def main():
    global exact
    command = typer.main.get_command(app)

    try:
        rc = command(standalone_mode=False)

    except click.ClickException as e:
        err_console.print(e)

    except Exception as e:
        err_console.print(type(e))
        err_console.print(f"Got unexpected exception: {e}")

