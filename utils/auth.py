from typing import Optional, Tuple
import requests
from nicegui import app, ui
from .api import base_url

# --- Safe session helpers ---

def _ensure_session_storage():
    # This function is now a no-op, as the checks are done in each session function
    pass

def set_session(token: Optional[str], role: Optional[str], user_id: Optional[str], name: Optional[str] = None) -> None:
    try:
        app.storage.user['token'] = token
        app.storage.user['role'] = role
        app.storage.user['user_id'] = user_id
        app.storage.user['name'] = name
    except RuntimeError:
        # Storage not initialized yet, ignore silently
        pass

def clear_session() -> None:
    try:
        app.storage.user.clear()
    except RuntimeError:
        # Storage not initialized yet, ignore silently
        pass

def get_role() -> Optional[str]:
    if not hasattr(app, 'storage'):
        return None
    try:
        return app.storage.user.get('role')
    except RuntimeError:
        return None

def get_user_id() -> Optional[str]:
    if not hasattr(app, 'storage'):
        return None
    try:
        return app.storage.user.get('user_id')
    except RuntimeError:
        return None

def get_token() -> Optional[str]:
    if not hasattr(app, 'storage'):
        return None
    try:
        return app.storage.user.get('token')
    except RuntimeError:
        return None

def is_vendor() -> bool:
    return get_role() == 'vendor'

def is_user() -> bool:
    return get_role() == 'user'

def require_vendor() -> bool:
    if not is_vendor():
        ui.notify('Vendor access required. Please sign in as a vendor.', type='warning')
        ui.navigate.to('/sign-in')
        return False
    return True


# --- Backend API auth helpers ---
def api_signup(name: str, email: str, password: str, role: str) -> Tuple[bool, str, Optional[str], Optional[str]]:
    """
    Attempts to sign up a user. Returns (success, message, token, user_id).
    """
    try:
        payload = {
            'name': name,
            'email': email,
            'password': password,
            'role': role,
        }
        r = requests.post(f"{base_url}/auth/signup", json=payload, timeout=15)
        if 200 <= r.status_code < 300:
            data = r.json()
            token = data.get('token') or data.get('access_token')
            user_id = (data.get('user') or {}).get('id') or data.get('user_id')
            return True, 'Account created', token, user_id
        else:
            try:
                err = r.json()
                msg = err.get('message') or err.get('detail') or str(err)
            except Exception:
                msg = r.text
            return False, msg, None, None
    except Exception as e:
        return False, f"Signup failed: {e}", None, None


def api_login(email: str, password: str) -> Tuple[bool, str, Optional[str], Optional[str], Optional[str], Optional[str]]:
    """
    Attempts to log in. Returns (success, message, token, user_id, role, name).
    """
    try:
        payload = {
            'email': email,
            'password': password,
        }
        r = requests.post(f"{base_url}/auth/login", json=payload, timeout=15)
        if 200 <= r.status_code < 300:
            data = r.json()
            token = data.get('token') or data.get('access_token')
            user = data.get('user') or {}
            user_id = user.get('id') or data.get('user_id')
            role = user.get('role') or data.get('role')
            name = user.get('name') or data.get('name')
            return True, 'Logged in', token, user_id, role, name
        else:
            try:
                err = r.json()
                msg = err.get('message') or err.get('detail') or str(err)
            except Exception:
                msg = r.text
            return False, msg, None, None, None, None
    except Exception as e:
        return False, f"Login failed: {e}", None, None, None, None
