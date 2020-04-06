import click


def success(message):
    click.echo(click.style(str(message), fg='green', bold=True))


def error(message):
    click.echo(click.style(str(message), fg='red', bold=True))


def bar():
    click.echo(click.style("--------------------", fg=d, ))
