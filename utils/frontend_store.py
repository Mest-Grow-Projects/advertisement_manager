from typing import Dict, List, Optional, Any
from nicegui import app
import hashlib
import uuid

USERS_KEY = 'mock_users'
ADVERTS_KEY = 'mock_adverts'


def _ensure_init():
    store = app.storage.general
    if USERS_KEY not in store:
        # seed with a sample vendor and user (password: 123456)
        pwd = hashlib.sha256('123456'.encode()).hexdigest()
        store[USERS_KEY] = [
            {'id': 'v1', 'name': 'Demo Vendor', 'email': 'vendor@example.com', 'password': pwd, 'role': 'vendor'},
            {'id': 'u1', 'name': 'Demo User', 'email': 'user@example.com', 'password': pwd, 'role': 'user'},
        ]
    if ADVERTS_KEY not in store:
        store[ADVERTS_KEY] = [
            {'id': 'a1', 'name': 'Spicy Jollof', 'description': 'Delicious Ghanaian jollof', 'price': 50, 'owner_id': 'v1', 'image': ''},
            {'id': 'a2', 'name': 'Waakye Special', 'description': 'Beans and rice combo', 'price': 35, 'owner_id': 'v1', 'image': ''},
        ]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# Users

def create_user(name: str, email: str, password: str, role: str) -> Dict[str, Any]:
    _ensure_init()
    users: List[Dict[str, Any]] = app.storage.general[USERS_KEY]
    if any(u['email'].lower() == email.lower() for u in users):
        raise ValueError('Email already registered')
    new_user = {
        'id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'password': hash_password(password),
        'role': role,
    }
    users.append(new_user)
    app.storage.general[USERS_KEY] = users
    return new_user


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    _ensure_init()
    users: List[Dict[str, Any]] = app.storage.general[USERS_KEY]
    h = hash_password(password)
    for u in users:
        if u['email'].lower() == email.lower() and u['password'] == h:
            return u
    return None


# Adverts

def list_adverts() -> List[Dict[str, Any]]:
    _ensure_init()
    return list(app.storage.general[ADVERTS_KEY])


def get_advert(advert_id: str) -> Optional[Dict[str, Any]]:
    _ensure_init()
    for a in app.storage.general[ADVERTS_KEY]:
        if str(a['id']) == str(advert_id):
            return a
    return None


def create_advert(name: str, description: str, price: float, owner_id: str, image: str = '') -> Dict[str, Any]:
    _ensure_init()
    adverts: List[Dict[str, Any]] = app.storage.general[ADVERTS_KEY]
    new_ad = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'price': price,
        'owner_id': owner_id,
        'image': image,
    }
    adverts.append(new_ad)
    app.storage.general[ADVERTS_KEY] = adverts
    return new_ad


def update_advert(advert_id: str, name: str, description: str, price: float) -> Dict[str, Any]:
    _ensure_init()
    adverts: List[Dict[str, Any]] = app.storage.general[ADVERTS_KEY]
    for a in adverts:
        if str(a['id']) == str(advert_id):
            a['name'] = name
            a['description'] = description
            a['price'] = price
            app.storage.general[ADVERTS_KEY] = adverts
            return a
    raise KeyError('Advert not found')


def delete_advert(advert_id: str) -> None:
    _ensure_init()
    adverts: List[Dict[str, Any]] = app.storage.general[ADVERTS_KEY]
    app.storage.general[ADVERTS_KEY] = [a for a in adverts if str(a['id']) != str(advert_id)]
