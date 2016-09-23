# -*- coding: utf-8 -*-

import click

from glogcli.graylog_api import GraylogAPIFactory
from glogcli.utils import get_config

@click.command()
@click.option("-sh", "--source-host", default=None, help="")
@click.option("-th", "--target-host", default=None,  help="")
@click.option("-su", "--source-username", default=None,  help="")
@click.option("-tu", "--target-username", default=None,  help="")
@click.option("-sp", "--source-password", default=None,  help="")
@click.option("-tp", "--target-password", default=None,  help="")
@click.option("--source-port", default=80,  help="")
@click.option("--target-port", default=80,  help="")
def main(source_host,
         target_host,
         source_username,
         target_username,
         source_password,
         target_password,
         source_port,
         target_port):
    print(source_host, target_host, source_username, target_username, source_password, target_password)
    click.echo("Replace this message by putting your code into "
                "glogadmin-cli.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    cfg = get_config()
    environment = None
    source_api = GraylogAPIFactory.get_graylog_api(cfg, environment, source_host, source_password, source_port, None, False, source_username)
    target_api = GraylogAPIFactory.get_graylog_api(cfg, environment, target_host, target_password, target_port, None, False, target_username)

    print(source_api.get_saved_queries())
    print(target_api.get_saved_queries())

if __name__ == "__main__":
    main()
