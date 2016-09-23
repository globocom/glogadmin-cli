
import click
import requests
import six
import json


class GraylogAPI(object):
    def __init__(self, graylog_api):
        self.graylog_api = graylog_api

    def get_streams(self):
        return self.graylog_api.streams()

    def get_roles(self):
        return self.graylog_api.get("roles")

    def post_role(self, role, **kwargs):
        url = "roles"
        params = {}

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item

        role['permissions'] = []
        post_header = {"Accept":"application/json", "Content-Type": "application/json"}
        r = requests.post(self.graylog_api.base_url + url, params=params, headers=post_header, auth=(self.graylog_api.username, self.graylog_api.password),
                          proxies=self.graylog_api.proxies, data=json.dumps(role))
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            click.echo("API error: Status: {} Message: {}".format(r.status_code, r.content))
            exit()
