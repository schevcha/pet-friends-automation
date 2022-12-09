import os
import pytest
from QA_Automation.api import PetFriends
from QA_Automation.settings import valid_email, valid_password

pf = PetFriends()

"""Позитивные проверки для каждого API"""


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем успешность запроса api-ключа и наличие слова 'key' в результате"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос списка всех питомцев возвращает не пустой список.
    Для этого сохраняем api-ключ в переменную auth_key. Фильтр 'my_pets' позволяет получить список только своих животных"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_post_new_pet_simple(name='Tom', animal_type='cat', age='5'):
    """Проверка успешности добавления нового питомца без фото. В результате должен сформироваться id созданного питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert 'id' in result


def test_post_new_pet(name='Lady', animal_type='dog', age='7', pet_photo='images/img.png'):
    """Тест на успешность добавления нового питомца с фото. Проверяем ответ по параметру name"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.post_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверка возможности удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Дон', animal_type='Пёс', age=5):
    """Проверка возможности обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_photo_of_pet(pet_photo='images/img.png'):
    """Проверка возможности обновления фото животного"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert pet_photo is not None
    else:
        raise Exception("There is no my pets")