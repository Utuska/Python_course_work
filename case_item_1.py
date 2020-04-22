import json
import requests
import time

class User:

    def __init__(self, id ):
        self.user_id = id
        self.friend_leng = 0 # число друзей
        self.number = 1 # переменная для счетчика обработанных друзей
        self.version = 5.103
        self.friends_id = [] # задаем список групп друзей
        self.list_group_friend = [] # задаем список групп друзей
        self.main_groups = [] # задаем список групп пользователя
        self.unique_groups_information = [] # информация уникальных групп
        self.token = 'f521c678206906cf2f8a5d179f463407449a616469bddb48c7ebd1eab8b99a45b47c242adf63cef2b6c77'

    # получаем список друзей
    def list_friend(self):
        response = requests.get('https://api.vk.com/method/friends.get',
                                params={
                                    'access_token': self.token,
                                    'user_id': self.user_id,
                                    'count': 200,
                                    'order': 'name',
                                    'v': self.version
                                })
        try:
            self.friends_id = response.json()
            self.friend_leng = len(self.friends_id['response']['items'])
            #print(f'Список друзей {self.friends_id["response"]["items"]}')

        except KeyError:
            print('Ошибка с определение друзей пользователя\n'
                  'Проверьте праквильность введенного id пользователя или токен')
            raise SystemExit(1)

    def conclusion_work(self):
        if self.number <= self.friend_leng:
            percentage = float('{:.2f}'.format(self.number * 100 / self.friend_leng))
            print(f'{self.number} / {self.friend_leng} ({percentage} %)')
            self.number += 1

    # получаем список    групп     друзей
    def list_groups_friends(self):

        print('Идет запись групп друзей')
        for friends_id in self.friends_id['response']['items']:

            # отображение обработанных друзей
            self.conclusion_work()

            response_one = requests.get('https://api.vk.com/method/users.getSubscriptions',
                                        params={
                                            'access_token': self.token,
                                            'user_id': friends_id,
                                            'extended': '1',
                                            'v': self.version
                                        })

            information_group = response_one.json()
            # print(information_group)

            # проверяем есть ли группа в списке групп друзей
            try:
                for id_group in information_group['response']['items']:
                    # print(id_group['id'])
                    if id_group['id'] not in self.list_group_friend:
                        self.list_group_friend.append(id_group['id'])
            except KeyError:
                continue
            time.sleep(0.6)
            #print(self.list_group_friend)




    # получаем список групп пользователя
    def list_groups_maim(self):
        response_main = requests.get('https://api.vk.com/method/users.getSubscriptions',
                                     params={
                                         'access_token': self.token,
                                         'user_id': self.user_id,
                                         'extended': '1',
                                         'v': self.version
                                     })


        try:
            self.main_groups = response_main.json()
        except json.decoder.JSONDecodeError:
            print('Произошла ошибка при формировании групп пользователя')
            raise SystemExit(1)


    # определение групп которые есть только у основного пользователя
    def unique_pool(self):
        print('\nВыявление групп, которые есть только у пользователя\n')
        for id_main in self.main_groups['response']['items']:
            # print(id_main['id'])
            if id_main['id'] not in self.list_group_friend:
                print('{}{}'.format('http://vk.com/club', id_main['id']))
                response_information = requests.get('https://api.vk.com/method/groups.getById',
                                                    params={
                                                        'access_token': self.token,
                                                        'group_id': id_main['id'],
                                                        'fields': 'members_count',
                                                        'v': 5.103
                                                    })

                information_group = response_information.json()
                self.unique_groups_information.append({'name': information_group['response'][0]['name'], 'gid': information_group['response'][0]['id'], 'members_count': information_group['response'][0]['members_count']})
                print(information_group['response'][0])

            time.sleep(0.6)


    def json_write(self):
        with open("information_groups.json", "w", encoding="utf-8") as file:
            for i in self.unique_groups_information:
                json.dump(i, file)



if __name__ == "__main__":
    unit_1 = User(67465626)
    # записываем id друзей
    unit_1.list_friend()
    # записываем все группы друзей в общий список (без повторов)
    unit_1.list_groups_friends()
    # записываем список групп основного пользователя
    unit_1.list_groups_maim()
    # определяем группы, которых нет у друзей
    unit_1.unique_pool()
    # записываем информацию в отдельный файл
    unit_1.json_write()
    print(f'Основная информация о группах {unit_1.unique_groups_information}')