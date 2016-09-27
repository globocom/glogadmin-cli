
import click
import requests
import six
import json

POST_DEFAULT_HEADER = {"Accept": "application/json", "Content-Type": "application/json"}

class GraylogAPI(object):

    def __init__(self, graylog_api):
        self.graylog_api = graylog_api

    def get_extractors(self, input_id):
        return self.graylog_api.get("system/inputs/{}/extractors".format(input_id))

    def get_inputs(self):
        return self.graylog_api.get("system/inputs")

    def get_streams(self):
        return self.graylog_api.streams()

    def get_roles(self):
        return self.graylog_api.get("roles")

    def get_stream(self, id):
        return self.graylog_api.get("streams/{}".format(id))

    def post_input(self, input, **kwargs):
        url = "system/inputs"
        params = {}

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item
        r = requests.post(self.graylog_api.base_url + url, params=params, headers=POST_DEFAULT_HEADER,
                          auth=(self.graylog_api.username, self.graylog_api.password),
                          proxies=self.graylog_api.proxies, data=json.dumps(input))

        if r.status_code == requests.codes.created:
            return r.json()
        else:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))
            return r.json()


    def post_role(self, role, **kwargs):
        url = "roles"
        params = {}

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item

        role['permissions'] = []
        r = requests.post(self.graylog_api.base_url + url, params=params, headers=POST_DEFAULT_HEADER,
                          auth=(self.graylog_api.username, self.graylog_api.password),
                          proxies=self.graylog_api.proxies, data=json.dumps(role))

        if r.status_code == requests.codes.created:
            return r.json()
        else:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))
            return r.json()

    def put_streams_in_role(self, role, streams, **kwargs):
        url = "roles/{}".format(role.get("name"))
        params = {}
        for stream in streams:
            role["permissions"].append("streams:read:{}".format(stream.get("stream_id")))
            role["permissions"].append("streams:edit:{}".format(stream.get("stream_id")))

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item

        r = requests.put(self.graylog_api.base_url + url, params=params, headers=POST_DEFAULT_HEADER,
                         auth=(self.graylog_api.username, self.graylog_api.password),
                         proxies=self.graylog_api.proxies, data=json.dumps(role))

        if r.status_code != requests.codes.created:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))
        return r.json()

    def post_stream(self, stream, **kwargs):
        url = "streams"
        params = {}

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item

        r = requests.post(self.graylog_api.base_url + url, params=params, headers=POST_DEFAULT_HEADER,
                          auth=(self.graylog_api.username, self.graylog_api.password),
                          proxies=self.graylog_api.proxies, data=json.dumps(stream))

        if r.status_code != requests.codes.created:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))

        return r.json()
