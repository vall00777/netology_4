# coding: utf-8

import json
import requests

parse_response = lambda response: json.loads(response)["response"]
parse_error = lambda response: json.loads(response)['error']

MANY_REQUESTS_PER_SECOND_ERROR = 6


class ApiException(Exception):
    pass


class API(object):
    req_url = 'https://api.vk.com/method/{}?{}&access_token={}&v={}'
    api_version = 5.92

    def __init__(self, key):
        self.key = key

    def get_users_ids(self, id):
        print('- friends.get {}'.format(id))
        params = list()
        params.append('user_id=' + str(id))
        req = self.req_url.format("friends.get", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        if 'error' in response:
            resp = parse_error(response)
            if int(resp['error_code']) == MANY_REQUESTS_PER_SECOND_ERROR:
                return self.get_user_groups(id)
            else:
                raise ApiException(resp['error_msg'])

        return parse_response(response)['items']

    def get_user_groups(self, id):
        print('- groups.get {}'.format(id))
        params = list()
        params.append('user_id='+str(id))
        req = self.req_url.format("groups.get", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        if 'error' in response:
            resp = parse_error(response)
            if int(resp['error_code']) == MANY_REQUESTS_PER_SECOND_ERROR:
                return self.get_user_groups(id)
            else:
                raise ApiException(resp['error_msg'])

        return parse_response(response)['items']

    def get_id(self, id):
        print('- users.get {}'.format(id))
        params = list()
        params.append('user_ids=' + str(id))
        req = self.req_url.format("users.get", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        return parse_response(response)[0]['id']

    def get_group_info(self, id):
        print('- groups.getById {}'.format(id))
        params = list()
        params.append('group_id=' + str(id))
        params.append('fields=members_count')
        req = self.req_url.format("groups.getById", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        if 'error' in response:
            resp = parse_error(response)
            if int(resp['error_code']) == MANY_REQUESTS_PER_SECOND_ERROR:
                return self.get_group_info(id)
            else:
                raise ApiException(resp['error_msg'])

        response = parse_response(response)
        return response[0]['id'], response[0]['name'], response[0]['members_count']
