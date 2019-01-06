import requests
import time

from config import VK_CONFIG as vk
from typing import Union, List, Optional
from api_models import User, Message



def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3)-> Optional[requests.models.Response]:
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for t in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=(timeout, 3))
            return response
        except requests.exceptions.RequestException:
            if t == max_retries - 1:
                raise
            delay = backoff_factor * 2 ** t
            # time.sleep прерывает работу скрипта на определнное кол-во времени (в данное время - откладывается)
            time.sleep(delay)

def get_friends(user_id, fields)-> Union[List[User], List[int]]:
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    # параметры запроса к серваку
    query_params = {
        'access_token': vk['access_token'],
        'user_id': user_id,
        'fields': fields,
        'version': vk['version']
    }
    # запрос делается, в {} вставляется домен из конфига (import config)
    query = "{domain}/friends.get?".format(domain=vk['domain'])
    # получение ответа
    response = get(query, query_params)
    # переделывание в джейсон
    json_doc = response.json()
    fail = json_doc.get('error')
    if fail != 0:
        return json_doc['response']


def messages_get_history(user_id: int, offset=0, count=200)-> list:
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    # очередные параметры к серваку
    query_params = {
        'domain': vk['domain'],
        'access_token': vk['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': count,
        'version': vk['version']
    }
    messages = []
    i = 0
    while i < count:
        if (i / 200) % 3 == 0 and i:
            time.sleep(1)
        if count - i <= 200:
            query_params['count'] = count - i
        url = "{domain}/messages.getHistory?offset={offset}&count={count}&user_id={user_id}&" \
              "access_token={access_token}&v={version}".format(**query_params)
        # ответ =
        response = requests.get(url)
        # переделывание ответов в джейсон
        json_doc = response.json()
        fail = json_doc.get('error')
        if fail:
            raise Exception(json_doc['error']['error_msg'])
        messages.extend(json_doc['response']['items'])
        i += 200
        query_params['offset'] += i
    return messages