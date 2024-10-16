import requests

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
        import json

        with open(file_name, 'w', encoding='UTF-8') as file:
            for person in Person.data:
                json.dump(person.__dict__, file, indent=4)

    data = []
    

TOKEN = '0ebe6cb70ebe6cb70ebe6cb7700d9eb02500ebe0ebe6cb769b0f246f161e9e6511725da'
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
    
def collect_friends(user_id: str) -> list:
    user_friends = get_friends(user_id)

    if user_friends is None:
            # print(f'Ошибка при получении друзей id{user_id}.')
            return
    
    if not user_friends:
            # print(f'У id{user_id} список друзей пуст.')
            return
    
    print(f'Пользователь id{user_id}')
    return user_friends


people = {
    184007908: 'Руденок Максим',
    420058114: 'Казьмин Даниил',
    # 198658352: 'Смелкин Никита'
}

if __name__ == "__main__":

    for id in people:

        friends1 = collect_friends(id) # Друзья участника группы
        Person(id=id, friends=friends1) # Добавление участника группы и его друзей

        for friend1 in friends1:
            friends2 = collect_friends(friend1) # Друзья друзей участника группы

            if friends2 is not None:
                Person(id=friend1, friends=friends2) # Добавление друзей участника группы и их друзей
            else:
                continue

            for friend2 in friends2:
                print(f'Друг друга: id{friend2}')
                Person(id=friend2, friends=[]) # Добавление друзей друзей участника группы

    print(len(Person.data)) 
    Person.jsonify('data.json')
