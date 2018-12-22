# coding: utf-8

import json
from api import API, ApiException

api_key = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'


def save(data):
    with open('groups.json', 'w', encoding="utf-8") as outfile:
        for chunk in json.JSONEncoder(ensure_ascii=False, indent=4).iterencode(data):
            outfile.write(chunk)


def main(id):
    api = API(api_key)

    if not id.isdigit():
        id = api.get_id(id)
    ids = api.get_users_ids(id)
    groups_set = set(api.get_user_groups(id))

    if not len(groups_set):
        print("У пользователя нет групп")
        return

    for user in ids:
        try:
            groups = set(api.get_user_groups(user))
            groups_set = groups_set - groups
        except ApiException as ex:
            print(ex)

    if not len(groups_set):
        print("Нет групп удовлетворяющих условию")
        return

    items = list()
    for group in groups_set:
        group_id, name, members_count = api.get_group_info(group)
        items.append({'id': group_id, 'name': name, 'members_count': members_count})

    for item in items:
        print(item)
    save({'items': items})


if __name__ == '__main__':
    user_id = input("Введиите id:")
    try:
        main(user_id)
    except Exception as e:
        print(e)
