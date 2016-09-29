# -*- coding: utf-8 -*-

import click
import json

from glogcli.graylog_api import GraylogAPIFactory
from glogcli.utils import get_config
from glogadmincli.graylog_api import GraylogAPI
from glogadmincli.utils import format_stream_to_create, format_input_to_create, format_extractor_to_create


@click.command()
@click.option("-se", "--source-environment", default=None, help="The Graylog source environment")
@click.option("-te", "--target-environment", default=None, help="The Graylog target environment")
@click.option("-sh", "--source-host", default=None, help="The Graylog node's source host")
@click.option("-th", "--target-host", default=None,  help="The Graylog node's target host")
@click.option("-su", "--source-username", default=None,  help="The source Graylog username")
@click.option("-tu", "--target-username", default=None,  help="The target Graylog username")
@click.option("-sp", "--source-password", default=None,  help="The source Graylog user password")
@click.option("-tp", "--target-password", default=None,  help="The target Graylog user password")
@click.option("--source-port", default=80,  help="The source Graylog port (default: 80)")
@click.option("--target-port", default=80,  help="The target Graylog port (default: 80)")
@click.option("--import-roles", default=False, is_flag=True, help="Imports the Roles and its Streams from the source to the target")
@click.option("--import-inputs", default=False, is_flag=True, help="Imports the Inputs and its Extractors from the source to the target")


def main(source_environment,
         target_environment,
         source_host,
         target_host,
         source_username,
         target_username,
         source_password,
         target_password,
         source_port,
         target_port,
         import_roles,
         import_inputs):

    cfg = get_config()

    source_api = GraylogAPIFactory.get_graylog_api(cfg, source_environment, source_host, source_password, source_port, None, False, source_username)
    target_api = GraylogAPIFactory.get_graylog_api(cfg, target_environment, target_host, target_password, target_port, None, False, target_username)

    source_api = GraylogAPI(source_api)
    target_api = GraylogAPI(target_api)

    if import_roles:
        source_roles = source_api.get_roles().get("roles")
        target_roles = target_api.get_roles().get("roles")

        roles_to_create = get_unique_roles_to_create(source_roles, target_roles)
        target_streams = target_api.get_streams()

        for role in roles_to_create:
            target_role_permissions = []
            for permission in role.get("permissions"):
                if("streams:" in permission):
                    resource_tag, permission, source_stream_id = permission.split(":")
                    stream = source_api.get_stream(source_stream_id)
                    if stream is not None:
                        is_stream_already_in_target = False
                        for target_stream in target_streams.get("streams"):
                            if target_stream.get("title") == stream.get("title"):
                                is_stream_already_in_target = True
                        if is_stream_already_in_target:
                            click.echo("Ignoring Stream {} from {}, it's already created in {}.".format(
                                stream.get("title"), source_api.get_host(), target_api.get_host()))
                        else:
                            result = target_api.post_stream(format_stream_to_create(stream))
                            target_role_permissions.append("{}:{}:{}".format(resource_tag, permission, result.get("stream_id")))

            role["permissions"] = target_role_permissions
            target_api.post_role(role)

    if import_inputs:
        source_inputs = source_api.get_inputs().get("inputs")
        target_inputs = target_api.get_inputs().get("inputs")

        inputs_to_create = []
        for source_input in source_inputs:
            is_source_input_already_in_target = False
            for target_input in target_inputs:
                if source_input.get("title") == target_input.get("title"):
                    is_source_input_already_in_target = True
            if is_source_input_already_in_target:
                click.echo("Ignoring Input {} from {}, it's already created in {}.".format(source_input.get("title"), source_api.get_host(), target_api.get_host()))
            else:

                inputs_to_create.append(source_input)

        for source_input in inputs_to_create:
            source_input_id = source_input.get("id")
            result = target_api.post_input(format_input_to_create(source_input))
            source_extractors = source_api.get_extractors(source_input_id).get("extractors")
            for source_extractor in source_extractors:
                formatted = format_extractor_to_create(source_extractor)
                target_api.post_extractor(formatted, result.get("id"))


def get_unique_roles_to_create(source_roles, target_roles):
    for target_role in target_roles:
        for source_role in source_roles:
            if(source_role.get("name").lower() == target_role.get("name").lower()):
                source_roles.remove(source_role)
    return source_roles

if __name__ == "__main__":
    main()
