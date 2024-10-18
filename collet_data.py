import requests
import json

class Person:
    def __init__(self, id, friends):
        self.id = id
        self.friends = friends
        Person.data.append(self)

    def __repr__(self):
        return f'id={self.id}, friends={self.friends}'
    
    @property
    def __dict__(self):
        return {
            'id': self.id,
            'friends': self.friends
        }   

    @staticmethod
    def jsonify(file_name: str):
        with open(file_name, 'w', encoding='UTF-8') as file:
            json_data = [person.__dict__ for person in Person.data]
            json.dump(json_data, file, indent=4, ensure_ascii=False)

    data = []
    

TOKEN = '' # Токен VK API
VERSION = 5.199

def get_friends(user_id: str) -> list | None:
    params = {
        'access_token': TOKEN,
        'v': VERSION,
        'user_id': user_id,
        'order': 'hints',
    }

    response = requests.get('https://api.vk.com/method/friends.get', params=params)

    try:
        return response.json()['response']['items']
    except KeyError:
        return None
    
def collect_friends(user_id: int, used_ids, num) -> list:
    user_friends = get_friends(user_id)

    if user_friends is None:
            print(f'Ошибка при получении друзей id{user_id}.')
            return
    
    if not user_friends:
            print(f'У id{user_id} список друзей пуст.')
            return
    
    return user_friends


people = {
    184007908: 'Руденок Максим',
    420058114: 'Казьмин Даниил',
    198658352: 'Смелкин Никита'
}

if __name__ == "__main__":

    used_ids = []

    for id in people:

        if id in used_ids:
            continue

        friends1 = collect_friends(id, used_ids, 1) # Друзья участника группы
        used_ids.append(id)
        Person(id=id, friends=friends1) # Добавление участника группы и его друзей

        for friend1 in friends1:

            if friend1 in used_ids:
                continue

            friends2 = collect_friends(friend1, used_ids, 2) # Друзья друзей участника группы
            used_ids.append(friend1)

            if friends2 is not None:
                Person(id=friend1, friends=friends2) # Добавление друзей участника группы и их друзей
            else:
                continue

    Person.jsonify('data.json')
