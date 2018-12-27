# coding: utf-8

import json
import requests


MANY_REQUESTS_PER_SECOND_ERROR = 6


class ApiException(Exception):
    pass


class API(object):
    req_url = 'https://api.vk.com/method/{}?{}&access_token={}&v={}'
    api_version = 5.92

    def __init__(self, key):
        self.key = key

    @staticmethod
    def _parse_response(response):
        return json.loads(response)["response"]

    @staticmethod
    def _parse_error(response):
        return json.loads(response)['error']

    def get_users_ids(self, user_id):
        print('- friends.get {}'.format(user_id))
        params = list()
        params.append('user_id=' + str(user_id))
        req = self.req_url.format("friends.get", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        if 'error' in response:
            resp = self._parse_error(response)
            if int(resp['error_code']) == MANY_REQUESTS_PER_SECOND_ERROR:
                return self.get_user_groups(user_id)
            else:
                raise ApiException(resp['error_msg'])

        return self._parse_response(response)['items']

    def get_user_groups(self, user_id):
        print('- groups.get {}'.format(user_id))
        params = list()
        params.append('user_id=' + str(user_id))
        req = self.req_url.format("groups.get", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        if 'error' in response:
            resp = self._parse_error(response)
            if int(resp['error_code']) == MANY_REQUESTS_PER_SECOND_ERROR:
                return self.get_user_groups(user_id)
            else:
                raise ApiException(resp['error_msg'])

        return self._parse_response(response)['items']

    def get_id(self, user_id):
        print('- users.get {}'.format(user_id))
        params = list()
        params.append('user_ids=' + str(user_id))
        req = self.req_url.format("users.get", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        return self._parse_response(response)[0]['id']

    def get_group_info(self, user_id):
        print('- groups.getById {}'.format(user_id))
        params = list()
        params.append('group_id=' + str(user_id))
        params.append('fields=members_count')
        req = self.req_url.format("groups.getById", "&".join(params), self.key, self.api_version)
        response = requests.get(req).text
        if 'error' in response:
            resp = self._parse_error(response)
            if int(resp['error_code']) == MANY_REQUESTS_PER_SECOND_ERROR:
                return self.get_group_info(user_id)
            else:
                raise ApiException(resp['error_msg'])

        response = self._parse_response(response)
        return response[0]['id'], response[0]['name'], response[0]['members_count']

