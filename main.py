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


people = {
    184007908: 'Руденок Максим',
    420058114: 'Казьмин Даниил',
    # 198658352: 'Смелкин Никита'
}


if __name__ == "__main__":
    
    for id in people:
        new_person_friends = get_friends(id)

        if new_person_friends is None:
            print(f'Ошибка при получении друзей id{id}.')
            continue

        new_person = Person(id=id, friends=new_person_friends)

        for friend in new_person_friends:
            friends = get_friends(friend)

            if friends is None or friends == []:
                print(f'Ошибка при получении друзей id{friend}.')
                continue

            Person(id=friend, friends=friends)
        
    Person.jsonify('data.json')
