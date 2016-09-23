# -*- coding: utf-8 -*-

import click

from glogcli.graylog_api import GraylogAPIFactory
from glogcli.utils import get_config
from glogadmincli.graylog_api import GraylogAPI

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

    source_api = GraylogAPIFactory.get_graylog_api(cfg, None, source_host, source_password, source_port, None, False, source_username)
    target_api = GraylogAPIFactory.get_graylog_api(cfg, None, target_host, target_password, target_port, None, False, target_username)

    source_api = GraylogAPI(source_api)
    target_api = GraylogAPI(target_api)

    source_roles = source_api.get_roles().get("roles")
    target_roles = target_api.get_roles().get("roles")

    roles_to_create = get_unique_roles_to_create(source_roles, target_roles)
    print(roles_to_create)

    for role in roles_to_create:
        result = target_api.post_role(role)
        print(result)

def get_unique_roles_to_create(source_roles, target_roles):
    for target_role in target_roles:
        for source_role in source_roles:
            if(source_role.get("name").lower() == target_role.get("name").lower()):
                source_roles.remove(source_role)
    return source_roles

    #source_streams = source_api.get_streams()
    #print(source_streams)
    #target_api.post_streams(source_streams)


if __name__ == "__main__":
    main()
