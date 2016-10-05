# -*- coding: utf-8 -*-

import click

from glogcli.graylog_api import GraylogAPIFactory
from glogcli.utils import get_config
from glogadmincli.graylog_api import GraylogAPI
from glogadmincli.utils import format_stream_to_create, format_input_to_create, format_extractor_to_create, format_rule_to_create


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
@click.option("--update", default=False, is_flag=True, help="Force update of resources like Streams and Extractors")


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
         import_inputs,
         update):

    cfg = get_config()

    source_api = GraylogAPIFactory.get_graylog_api(cfg, source_environment, source_host, source_password,
                                                   source_port, None, False, source_username, False)
    target_api = GraylogAPIFactory.get_graylog_api(cfg, target_environment, target_host, target_password,
                                                   target_port, None, False, target_username, False)
    source_api = GraylogAPI(source_api)
    target_api = GraylogAPI(target_api)

    if import_roles:
        source_roles = source_api.get_roles().get("roles")
        target_roles = target_api.get_roles().get("roles")

        roles_to_create = get_unique_roles_to_create(source_roles, target_roles, update)
        target_streams = target_api.get_streams()

        for role in roles_to_create:
            target_role_permissions = []

            stream_by_permission_map_source = get_permission_map_by_stream_id(role.get("permissions"))
            stream_by_permission_map_source.keys().reverse()
            for stream_id in stream_by_permission_map_source.keys():
                resource_tag = "streams"

                stream = source_api.get_stream(stream_id)
                if stream is None:
                    continue

                stream_was_not_updated = True
                for target_stream in target_streams.get("streams"):
                    source_stream_title = stream.get("title")
                    target_stream_title = target_stream.get("title")
                    if source_stream_title == target_stream_title:
                        target_api.put_stream(target_stream.get("id"), format_stream_to_create(stream))

                        source_rules = source_api.get_rules(stream_id).get("stream_rules")
                        target_rules = target_api.get_rules(target_stream.get("id")).get("stream_rules")

                        for target_rule in target_rules:
                            target_api.delete_rule(target_rule.get("stream_id"), target_rule.get("id"))
                        for source_rule in source_rules:
                            formatted_rule = format_rule_to_create(source_rule)
                            target_api.post_rule(target_stream.get("id"), formatted_rule)
                        stream_was_not_updated = False

                if stream_was_not_updated:
                    post_stream_response = target_api.post_stream(format_stream_to_create(stream))
                    if post_stream_response is not None:
                        click.echo("Stream {} successfully imported from {} to {}.".format(
                            stream.get("title"), source_api.get_host(), target_api.get_host()))

                        for permission_level in stream_by_permission_map_source.get(stream_id):
                            target_role_permissions.append(
                                "{}:{}:{}".format(resource_tag, permission_level, post_stream_response.get("stream_id")))

            role["permissions"] = target_role_permissions
            target_role = target_api.get_role(role)
            if target_role is None:
                response = target_api.post_role(role)
                if response.status_code in [200, 201]:
                    click.echo("Role {} successfully imported from {} to {}.".format(
                        role.get("name"), source_api.get_host(), target_api.get_host()))
                else:
                    click.echo("Role {} could not be created. Status: {} Message: {}".format(
                        role.get("name"), response.status_code, response.content))
            else:
                for permission in target_role_permissions:
                    target_role["permissions"].append(permission)

                if target_role.get("read_only") is False:
                    target_api.put_streams_in_role(target_role)

    if import_inputs:
        source_inputs = source_api.get_inputs().get("inputs")
        target_inputs = target_api.get_inputs().get("inputs")

        inputs_to_create = []
        for source_input in source_inputs:
            is_source_input_already_in_target = False
            source_input_id = source_input.get("id")

            for target_input in target_inputs:
                both_inputs_titles_are_equal = source_input.get("title") == target_input.get("title")
                both_inputs_types_are_equal = source_input.get("type") == target_input.get("type")
                if both_inputs_titles_are_equal and both_inputs_types_are_equal:
                    is_source_input_already_in_target = True
                    if update:
                        response = target_api.put_input(target_input.get("id"), format_input_to_create(source_input))
                        #update extractors comparing by title
                        click.echo("Updating Target Input '{}:{}' in {}, based on Source Input '{}:{}'".format(
                            target_input.get("title"), response.get("id"), target_api.get_host(),
                            source_input.get("title"), source_input_id)
                        )
                    else:
                        click.echo("Ignoring Input {}:{} from {}, it's already created in {}".format(
                            source_input.get("title"), source_input.get("id"), source_api.get_host(),
                            target_api.get_host())
                        )

            if not is_source_input_already_in_target:
                inputs_to_create.append(source_input)

        for source_input in inputs_to_create:
            source_input_id = source_input.get("id")
            source_input_title = source_input.get("title")
            if source_input_title == "input-sinval-do-not-touch-it":
                result = target_api.post_input(format_input_to_create(source_input))
                click.echo("Input {} successfully imported from {} to {}.".format(
                    source_input.get("title"), source_api.get_host(), target_api.get_host()))

                source_extractors = source_api.get_extractors(source_input_id).get("extractors")
                for source_extractor in source_extractors:
                    formatted = format_extractor_to_create(source_extractor)
                    target_api.post_extractor(formatted, result.get("id"))


def compare_extractors(first_extractor, second_extractor):
    return first_extractor.get("title").lower() == second_extractor.get("title").lower()

def get_permission_map_by_stream_id(role_permissions):
    stream_by_permission_map = {}
    for permission in role_permissions:
        if "streams:" not in permission:
            continue
        resource_tag, permission_level, source_stream_id = permission.split(":")
        stream_permissions = stream_by_permission_map.get(source_stream_id)
        if stream_permissions is not None:
            stream_permissions.append(permission_level)
        else:
            stream_by_permission_map[source_stream_id] = [permission_level]

    return stream_by_permission_map


def get_unique_roles_to_create(source_roles, target_roles, update=False):
    for target_role in target_roles:
        for source_role in source_roles:
            source_role_is_equals_to_target_role = source_role.get("name").lower() == target_role.get("name").lower()
            if source_role_is_equals_to_target_role and not (update):
                source_roles.remove(source_role)
            if source_role.get("name").lower() in ('admin','reader'):
                source_roles.remove(source_role)
    return source_roles

if __name__ == "__main__":
    main()
