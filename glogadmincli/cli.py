# -*- coding: utf-8 -*-

import click

from glogcli.graylog_api import GraylogAPIFactory
from glogcli.utils import get_config
from glogadmincli.graylog_api import GraylogAPI
from glogadmincli.utils import format_stream_to_create, format_input_to_create


@click.command()
@click.option("-sh", "--source-host", default=None, help="")
@click.option("-th", "--target-host", default=None,  help="")
@click.option("-su", "--source-username", default=None,  help="")
@click.option("-tu", "--target-username", default=None,  help="")
@click.option("-sp", "--source-password", default=None,  help="")
@click.option("-tp", "--target-password", default=None,  help="")
@click.option("--source-port", default=80,  help="")
@click.option("--target-port", default=80,  help="")
@click.option("--import-roles", default=False, is_flag=True, help="")
@click.option("--import-inputs", default=False, is_flag=True, help="")
@click.option("--import-extractors", default=False, is_flag=True, help="")


def main(source_host,
         target_host,
         source_username,
         target_username,
         source_password,
         target_password,
         source_port,
         target_port,
         import_roles,
         import_inputs,
         import_extractors):

    cfg = get_config()

    source_api = GraylogAPIFactory.get_graylog_api(cfg, None, source_host, source_password, source_port, None, False, source_username)
    target_api = GraylogAPIFactory.get_graylog_api(cfg, None, target_host, target_password, target_port, None, False, target_username)

    source_api = GraylogAPI(source_api)
    target_api = GraylogAPI(target_api)

    if import_roles:
        source_roles = source_api.get_roles().get("roles")
        target_roles = target_api.get_roles().get("roles")

        roles_to_create = get_unique_roles_to_create(source_roles, target_roles)

        for role in roles_to_create:
            target_role_permissions = []
            for permission in role.get("permissions"):
                if("streams:" in permission):
                    resource_tag, permission, source_stream_id = permission.split(":")
                    stream = source_api.get_stream(source_stream_id)
                    result = target_api.post_stream(format_stream_to_create(stream))
                    target_role_permissions.append("{}:{}:{}".format(resource_tag, permission, result.get("stream_id")))

            role["permissions"] = target_role_permissions
            target_api.post_role(role)

    if import_inputs:
        source_inputs = source_api.get_inputs().get("inputs")
        for source_input in source_inputs:
            source_input_id = source_input.get("id")
            result = target_api.post_input(format_input_to_create(source_input))

def get_unique_roles_to_create(source_roles, target_roles):
    for target_role in target_roles:
        for source_role in source_roles:
            if(source_role.get("name").lower() == target_role.get("name").lower()):
                source_roles.remove(source_role)
    return source_roles

if __name__ == "__main__":
    main()
