import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder



class PetFriends:
    """API-библиотека к веб приложению Pet Friends"""

    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'


    def get_api_key(self, email, password):
        """Метод запрашивает api-ключ  и возвращает статус запроса и результат по заданным почте и паролю"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def get_list_of_pets(self, auth_key, filter):
        """Метод запроса списка всех питомцев на сайте/списка своих питомцев"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def post_create_pet_simple(self, auth_key, name, animal_type, age):
        """Метод создания новой карточки питомца без фото"""

        headers = {'auth_key': auth_key['key']}
        formData = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers, params=formData)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def post_new_pet(self, auth_key, name, animal_type, age, pet_photo):
        """Метод создания карточки питомца с фото"""

        data = MultipartEncoder(
        fields={
            'name': name,
            'animal_type': animal_type,
            'age': age,
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')
        })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        На сегодняшний день тут есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомуа по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def post_add_photo_of_pet(self, auth_key, pet_id, pet_photo):
        """Метод обновления фото существующего питомца"""

        data = MultipartEncoder(
            fields={'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')}
        )
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

