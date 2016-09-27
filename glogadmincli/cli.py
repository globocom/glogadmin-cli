# -*- coding: utf-8 -*-

import click
import json

from glogcli.graylog_api import GraylogAPIFactory
from glogcli.utils import get_config
from glogadmincli.graylog_api import GraylogAPI
from glogadmincli.utils import mult_dict_del, format_stream_to_create, format_streams_to_create


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
@click.option("--import-streams", default=False, is_flag=True, help="")
def main(source_host,
         target_host,
         source_username,
         target_username,
         source_password,
         target_password,
         source_port,
         target_port,
         import_roles,
         import_streams):

    cfg = get_config()

    source_api = GraylogAPIFactory.get_graylog_api(cfg, None, source_host, source_password, source_port, None, False, source_username)
    target_api = GraylogAPIFactory.get_graylog_api(cfg, None, target_host, target_password, target_port, None, False, target_username)

    source_api = GraylogAPI(source_api)
    target_api = GraylogAPI(target_api)

    if(import_roles):
        source_roles = source_api.get_roles().get("roles")
        target_roles = target_api.get_roles().get("roles")

        roles_to_create = get_unique_roles_to_create(source_roles, target_roles)

        for role in roles_to_create:
            print(role)
            target_role_permissions = []
            for permission in role.get("permissions"):
                if("streams:" in permission):
                    resource_tag, permission, source_stream_id = permission.split(":")
                    stream = source_api.get_stream(source_stream_id)
                    result = target_api.post_stream(format_stream_to_create(stream))
                    target_role_permissions.append("{}:{}:{}".format(resource_tag, permission, result.get("stream_id")))

            role["permissions"] = target_role_permissions
            target_api.post_role(role)


    if(import_streams):
        source_streams = source_api.get_streams().get("streams")
        i = 0
        for stream in source_streams:
            stream_rules = stream.get("rules")
            for rule in stream_rules:
                del rule["stream_id"]
                del rule["id"]
            click.echo("{}: {} , rules: {}".format(i, stream.get("description"), stream_rules))
            i += 1
        selected_streams_indexes = raw_input("Select a list of streams passing IDs splitted by space, like '1 4 7 18': ").split(' ')

        created_streams = []
        for selected_index in selected_streams_indexes:
            stream_to_create = source_streams[int(selected_index)]
            result = target_api.post_stream(stream_to_create)
            created_streams.append(result)
        click.echo("Streams created in the target: {}".format(created_streams))
        click.echo("")

        target_roles = target_api.get_roles().get("roles")
        i = 0
        for role in target_roles:
            click.echo("{}: {} ".format(i, role.get("name")))
            i += 1

        selected_roles_indexes = raw_input("Select a list of roles to access the streams passing IDs splitted by space, like '1 4 7 18': ").split(' ')
        for selected_index in selected_roles_indexes:
            role_to_update = target_roles[int(selected_index)]
            target_api.put_streams_in_role(role_to_update, created_streams)

def get_unique_roles_to_create(source_roles, target_roles):
    for target_role in target_roles:
        for source_role in source_roles:
            if(source_role.get("name").lower() == target_role.get("name").lower()):
                source_roles.remove(source_role)
    return source_roles

if __name__ == "__main__":
    main()
