from nicegui import ui
import requests
from utils.api import base_url
from utils.auth import get_role, get_user_id, get_token
from components.footer import show_footer

@ui.page("/vendor/dashboard")
def show_vendor_dashboard():
    if not get_role() == 'vendor':
        return
    with ui.row().classes("w-full"):
        with ui.column().classes("w-[20%]"):
            show_side_bar()
        with ui.column().classes("w-[80%]"):
            ui.label("My Adverts").classes("text-2xl font-bold mb-4")
            container = ui.column().classes("gap-3")

            def refresh_list():
                container.clear()
                vendor_id = get_user_id()
                token = get_token()
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                
                try:
                    r = requests.get(f"{base_url}/food/all", headers=headers, timeout=15)
                    if 200 <= r.status_code < 300:
                        data = r.json()
                        items = data.get('data', [])
                    else:
                        ui.notify('Failed to load adverts', type='negative')
                        return
                except Exception as e:
                    ui.notify(f"Load failed: {e}", type='negative')
                    return
                    
                mine = [it for it in items if str((it.get('owner_id') or it.get('vendor_id') or '')) == str(vendor_id)]
                if not mine:
                    with container:
                        ui.label("No adverts yet. Create one from 'Add'.").classes('text-gray-600')
                    return
                    
                for it in mine:
                    with container:
                        with ui.row().classes('items-center justify-between w-full border rounded-lg p-3'):
                            ui.label(f"{it.get('name')} - ${it.get('price')}")
                            with ui.row().classes('gap-2'):
                                ui.button('Edit', on_click=lambda _=None, id=it.get('id'): ui.navigate.to(f"/vendor/edit_advert/{id}")).classes('text-white').style('background-color: #077d16 !important; hover:background-color: #065a11 !important;')
                                def do_delete(id=it.get('id')):
                                    try:
                                        d = requests.delete(f"{base_url}/food/{id}", headers=headers, timeout=15)
                                        if 200 <= d.status_code < 300:
                                            ui.notify('Deleted', type='positive')
                                            refresh_list()
                                        else:
                                            try:
                                                err = d.json()
                                                msg = err.get('message') or err.get('detail') or str(err)
                                            except Exception:
                                                msg = d.text
                                            ui.notify(f"Delete failed: {msg}", type='negative')
                                    except Exception as e:
                                        ui.notify(f"Delete error: {e}", type='negative')
                                ui.button('Delete', on_click=do_delete).classes('text-white').style('background-color: #077d16 !important; hover:background-color: #065a11 !important;')

            refresh_list()
    
    # Add footer
    show_footer()

def show_side_bar():
    """Simple sidebar for vendor navigation"""
    with ui.column().classes("p-4 bg-gray-100 h-screen"):
        ui.label("Vendor Menu").classes("text-xl font-bold mb-4")
        ui.link("Dashboard", "/vendor/dashboard").classes("block mb-2 text-blue-600 hover:underline")
        ui.link("Add Advert", "/vendor/add_advert").classes("block mb-2 text-blue-600 hover:underline")
        ui.link("View All", "/view_advert").classes("block mb-2 text-blue-600 hover:underline")
        ui.link("Home", "/").classes("block mb-2 text-blue-600 hover:underline")
