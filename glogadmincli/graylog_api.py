
import click
import requests
import six
import json

POST_DEFAULT_HEADER = {"Accept": "application/json", "Content-Type": "application/json"}

class GraylogAPI(object):

    def __init__(self, graylog_api):
        self.graylog_api = graylog_api

    def get(self, url, **kwargs):
        params = {}

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item
        r = requests.get(self.graylog_api.base_url + url, params=params, headers=self.graylog_api.get_header, auth=(self.graylog_api.username, self.graylog_api.password), proxies=self.graylog_api.proxies)

        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            click.echo("API error: Status: {} Message: {}".format(r.status_code, r.content))

    def get_host(self):
        return self.graylog_api.host

    def get_extractors(self, input_id):
        return self.get("system/inputs/{}/extractors".format(input_id))

    def get_inputs(self, **kwargs):
        return self.get("system/inputs", **kwargs)

    def get_streams(self):
        return self.get("streams")

    def get_roles(self):
        return self.get("roles")

    def get_stream(self, id):
        return self.get("streams/{}".format(id))

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

    def post_extractor(self, extractor, input_id):
        params = {}
        url = "system/inputs/{}/extractors".format(input_id)
        r = requests.post(self.graylog_api.base_url + url, params=params, headers=POST_DEFAULT_HEADER,
                          auth=(self.graylog_api.username, self.graylog_api.password),
                          proxies=self.graylog_api.proxies, data=json.dumps(extractor))

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
        return r

    def post_rule(self, stream_id, rule, **kwargs):
        url = "streams/{}/rules".format(stream_id)
        params = {}

        for label, item in six.iteritems(kwargs):
            if isinstance(item, list):
                params[label + "[]"] = item
            else:
                params[label] = item

        r = requests.post(self.graylog_api.base_url + url, params=params, headers=POST_DEFAULT_HEADER,
                          auth=(self.graylog_api.username, self.graylog_api.password),
                          proxies=self.graylog_api.proxies, data=json.dumps(rule))
        return r

    def put_streams_in_role(self, role, streams=[], **kwargs):
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

    def put_stream(self, stream_id, stream):
        url = "streams/{}".format(stream_id)

        r = requests.put(self.graylog_api.base_url + url, params={}, headers=POST_DEFAULT_HEADER,
                         auth=(self.graylog_api.username, self.graylog_api.password),
                         proxies=self.graylog_api.proxies, data=json.dumps(stream))

        if r.status_code != requests.codes.created:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))
        return r.json()

    def put_input(self, input_id, input):
        url = "system/inputs/{}".format(input_id)

        r = requests.put(self.graylog_api.base_url + url, params={}, headers=POST_DEFAULT_HEADER,
                         auth=(self.graylog_api.username, self.graylog_api.password),
                         proxies=self.graylog_api.proxies, data=json.dumps(input))

        if r.status_code != requests.codes.created:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))
        return r.json()

    def put_extractor(self, input_id, extractor_id, extractor):
        url = "system/inputs/{}/extractors/{}".format(input_id, extractor_id)

        r = requests.put(self.graylog_api.base_url + url, params={}, headers=POST_DEFAULT_HEADER,
                         auth=(self.graylog_api.username, self.graylog_api.password),
                         proxies=self.graylog_api.proxies, data=json.dumps(extractor))

        if r.status_code != requests.codes.ok:
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))
        return r.json()


    def get_role(self, role):
        return self.get("roles/{}".format(role.get("name")))

    def get_rules(self, stream_id):
        return self.get("streams/{}/rules".format(stream_id))

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
            return None

        return r.json()

    def delete_stream(self, stream_id):
        url = "streams/{}".format(stream_id)
        params = {}

        r = requests.delete(self.graylog_api.base_url + url, params=params,
                           auth=(self.graylog_api.username, self.graylog_api.password),
                           proxies=self.graylog_api.proxies)

        if r.status_code not in (200, 204):
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))

        return r

    def delete_rule(self, stream_id, rule_id):
        url = "streams/{}/rules/{}".format(stream_id, rule_id)
        params = {}

        r = requests.delete(self.graylog_api.base_url + url, params=params,
                            auth=(self.graylog_api.username, self.graylog_api.password),
                            proxies=self.graylog_api.proxies)

        if r.status_code not in (200, 204):
            click.echo("API - Status: {} Message: {}".format(r.status_code, r.content))

        return r
