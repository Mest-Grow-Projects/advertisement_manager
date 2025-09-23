from nicegui import ui
from components.side_bar import show_side_bar
from utils.auth import require_vendor, get_user_id, get_token
from utils.api import base_url
import requests

@ui.page("/vendor/edit_advert/{advert_id}")
def show_edit_advert_page(advert_id: str):
    if not require_vendor():
        return
    # --- Fullscreen background wrapper ---
    with ui.element("div").style(
        "background-image: url('/assets/edit.jpg');"
        "background-size: cover;"
        "background-position: center;"
        "width: 100vw;"
        "height: 100vh;"
        "display: flex;"
        "justify-content: center;"
        "align-items: center;"
        "margin: 0;"
        "padding: 0;"
    ):
        with ui.row().classes("w-full"):
            with ui.column().classes("w-[20%]"):
                show_side_bar()
            with ui.column().classes("w-[80%]"):
                # Load advert data
                token = get_token()
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                advert = None
                try:
                    resp = requests.get(f"{base_url}/food/{advert_id}", headers=headers, timeout=15)
                    if 200 <= resp.status_code < 300:
                        data = resp.json()
                        advert = data.get('data') or data
                    else:
                        ui.notify('Failed to load advert', type='negative')
                        ui.navigate.to('/vendor/dashboard')
                        return
                except Exception as e:
                    ui.notify(f'Network error: {e}', type='negative')
                    ui.navigate.to('/vendor/dashboard')
                    return

                # Ownership check
                current_user = get_user_id()
                owner_id = (advert or {}).get('owner_id') or (advert or {}).get('vendor_id')
                if current_user and owner_id and str(owner_id) != str(current_user):
                    ui.notify('You can only edit your own adverts', type='warning')
                    ui.navigate.to('/vendor/dashboard')
                    return

                #  Edit Advert Card
                with ui.card().classes('w-[600px] p-6 shadow-lg rounded-2xl bg-white/95 backdrop-blur'):
                    ui.label('EDIT ADVERT').classes('text-2xl font-bold text-center mb-6 tracking-wide')

                    # Input fields prefilled
                    Title = ui.input('Title', value=(advert or {}).get('name')).props('outlined dense').classes('w-full mb-4')
                    Description = ui.textarea('Item Description', value=(advert or {}).get('description')).props('outlined dense auto-grow').classes('w-full mb-4')
                    Price = ui.number('Price (USD)', value=(advert or {}).get('price')).props('outlined dense').classes('w-full mb-4')
                    Image = ui.select(
                        ['Keep current image', 'Upload new image from camera roll', 'Browse']
                    ).props('outlined dense').classes('w-full mb-6')

                    # Submit handler
                    def submit():
                        if not Title.value or not Description.value or Price.value is None:
                            ui.notify('⚠️ Please fill in all required fields', type='warning')
                            return
                        payload = {
                            "name": Title.value,
                            "description": Description.value,
                            "price": float(Price.value),
                        }
                        try:
                            r = requests.put(f"{base_url}/food/{advert_id}", json=payload, headers=headers, timeout=20)
                            if 200 <= r.status_code < 300:
                                ui.notify('✅ Advert Updated', type='positive')
                            else:
                                try:
                                    err = r.json()
                                    msg = err.get('message') or err.get('detail') or str(err)
                                except Exception:
                                    msg = r.text
                                ui.notify(f'Update failed: {msg}', type='negative')
                        except Exception as e:
                            ui.notify(f'Network error: {e}', type='negative')

                    # Buttons row
                    with ui.row().classes('justify-between mt-4'):
                        ui.button('Cancel', on_click=lambda: ui.navigate.to('/vendor/dashboard')).classes(
                            'bg-gray-300 text-black w-[45%] py-2 rounded-xl hover:bg-gray-400'
                        )
                        ui.button('Save Changes', on_click=submit).classes(
                            'text-white w-[45%] py-2 rounded-xl'
                        ).style('background-color: #077d16 !important; hover:background-color: #065a11 !important;')
