import logging

# import click
import requests
import rich_click as click
from notifiers import get_notifier
from rich.console import Console
from rich.table import Table

from .lib.notify import slack_notify

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter(style="{", fmt="[{name}:{filename}] {levelname} - {message}")
)

log = logging.getLogger("cvet")
log.setLevel(logging.INFO)
log.addHandler(handler)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help", "help"])
click.rich_click.SHOW_ARGUMENTS = True


@click.command(no_args_is_help=True, context_settings=CONTEXT_SETTINGS)
@click.argument(
    "time_frame",
    type=click.Choice(["day", "week"]),
    default="day",
)
@click.option("-n", "--notify", help="Slack webhook to notify on run")
@click.option(
    "-rt",
    "--repo-threshold",
    type=int,
    default=1,
    help="Number of repos needed to show CVE.",
    show_default=True,
)
def main(time_frame, notify, repo_threshold) -> None:
    """cvetrends.com CLI"""

    if time_frame == "day":
        time_frame = "24hrs"
    elif time_frame == "week":
        time_frame = "7days"

    # Issuing request to cvetracker.com
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }
    response = requests.get(
        f"https://cvetrends.com/api/cves/{time_frame}", headers=headers, timeout=15
    )

    table = Table()
    table.add_column("CVE")
    table.add_column("Description")
    table.add_column("GitHub Repos")

    # Checking if request was successful
    try:
        # Parsing response and constructing table
        for i in response.json()["data"]:
            if len(i["github_repos"]) >= repo_threshold:
                table.add_row(i["cve"], i["description"], f"{len(i['github_repos'])}")
    except Exception as a:
        print(f"Something went wrong: {a}")
        exit(1)

    # Constructing table
    console = Console()

    # Only print table if notify isn't set
    if not notify:
        console.print(table)

    # Notify if notify is set
    if notify:
        slack_notify(response.json()["data"], notify, repo_threshold)


if __name__ == "__main__":
    main(prog_name="cvetrends")  # pragma: no cover
