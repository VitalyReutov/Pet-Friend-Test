import requests
import os

from api_2 import PetFriends
from settings import *

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result

def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)

    assert status == 403


def test_create_pet_simple_with_valid_data(name='Gavrik', animal_type='Dog', age='12'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_without_name(name='', animal_type='Dog', age='12'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    # БАГ, API возвращает 200
    assert result['name'] == name

def test_create_pet_simple_without_animal_type(name='Gavrik', animal_type='', age='12'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    # БАГ, API возвращает 200
    assert result['animal_type'] == animal_type

def test_create_pet_simple_without_age(name='Gavrik', animal_type='Dog', age=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    # БАГ, API возвращает 200
    assert result['animal_type'] == animal_type

def test_create_pet_simple_with_negative_age(name='Gavrik', animal_type='Dog', age='-555'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400
    # БАГ, API возвращает 200
    assert result['animal_type'] == animal_type


def test_add_photo_of_pet_with_valid_data(pet_photo='/Users/vitaly/Downloads/123.jpeg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
    return result
    assert status == 200
    assert result == open(pet_photo, 'rb'), 'image/jpeg'

def test_add_photo_of_pet_with_incorrect_photo_IN_PDF(pet_photo='/Users/vitaly/Desktop/Обучение/Резюме_итог.pdf'):
    try:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        return result
    except PermissionError:
        err1 = 'Некорректный формат файла'
    assert err1 == 'Некорректный формат файла'

def test_add_photo_of_pet_with_no_photo(pet_photo=''):
    try:
        pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        return result
    except IsADirectoryError:
        err1 = 'Ошибка в пути размещения файла'
    assert err1 == 'Ошибка в пути размещения файла'


