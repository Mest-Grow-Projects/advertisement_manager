from nicegui import ui
import requests
from utils.api import base_url
from components.footer import show_footer
from utils.auth import get_role, get_user_id, get_token

def show_view_advert_page():
    try:
        response = requests.get(f"{base_url}/food/all", timeout=15)
        if 200 <= response.status_code < 300:
            json_data = response.json()
            restaurants = json_data.get("data", [])
        else:
            ui.notify('Failed to load adverts', type='negative')
            restaurants = []
    except Exception as e:
        ui.notify(f'Error loading adverts: {e}', type='negative')
        restaurants = []

    ui.label("Browse Restaurants").classes("text-2xl font-bold mb-4 text-center mx-10")

    # --- Data for restaurants ---

    # --- Search input ---
    search_box = ui.input(placeholder="Search restaurants...").props("outlined dense clearable").classes(
        "w-1/2 mx-auto mb-6 px-4 py-3 border-2 border-green-200 rounded-xl focus:border-green-500 focus:outline-none transition-colors"
    )

    # --- Container for results ---
    results_container = ui.row().classes("justify-center gap-10 flex-wrap")

    def show_advert_modal(advert):
        """Show detailed modal for an advert with edit/delete options for vendors"""
        current_role = get_role()
        current_user_id = get_user_id()
        is_owner = (current_role == 'vendor' and 
                   str(current_user_id) == str(advert.get('owner_id') or advert.get('vendor_id')))
        
        with ui.dialog() as dialog, ui.card().classes('w-[600px] max-w-[90vw]'):
            # Header
            with ui.row().classes('w-full items-center justify-between mb-4'):
                ui.label(advert.get('name', 'Untitled')).classes('text-2xl font-bold')
                ui.button('×', on_click=dialog.close).classes('text-xl px-3 py-1 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105').style('border: none;')
            
            # Image
            if advert.get('image'):
                ui.image(advert['image']).classes('w-full h-48 object-cover rounded-lg mb-4')
            else:
                ui.element('div').classes('w-full h-48 bg-gray-200 rounded-lg mb-4 flex items-center justify-center').add(
                    ui.label('No Image Available').classes('text-gray-500')
                )
            
            # Details
            ui.label('Description').classes('font-semibold text-lg mb-2')
            ui.label(advert.get('description', 'No description available')).classes('text-gray-700 mb-4')
            
            ui.label('Price').classes('font-semibold text-lg mb-2')
            ui.label(f"${advert.get('price', 'N/A')}").classes('text-2xl font-bold text-green-600 mb-4')
            
            # Action buttons
            with ui.row().classes('w-full justify-between mt-6'):
                # Left side - Close button
                ui.button('Close', on_click=dialog.close).classes(
                    'px-8 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl hover:from-gray-600 hover:to-gray-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105'
                )
                
                # Right side - Edit/Delete buttons (always visible for vendors)
                with ui.row().classes('gap-2'):
                    if current_role == 'vendor':
                        # Edit button (always visible for vendors)
                        ui.button('Edit', on_click=lambda: (
                            dialog.close(),
                            ui.navigate.to(f"/vendor/edit_advert/{advert.get('id')}")
                        )).classes('px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105').style(
                            'border: none;'
                        )
                        
                        # Delete button with confirmation (always visible for vendors)
                        def confirm_delete():
                            with ui.dialog() as confirm_dialog, ui.card().classes('w-[400px]'):
                                ui.label('Confirm Delete').classes('text-xl font-bold mb-4')
                                ui.label(f'Are you sure you want to delete "{advert.get("name", "this advert")}"?').classes('mb-6')
                                ui.label('This action cannot be undone.').classes('text-red-600 mb-6')
                                
                                with ui.row().classes('w-full justify-end gap-2'):
                                    ui.button('Cancel', on_click=confirm_dialog.close).classes(
                                        'px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl hover:from-gray-600 hover:to-gray-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105'
                                    )
                                    
                                    def delete_advert():
                                        token = get_token()
                                        headers = {"Authorization": f"Bearer {token}"} if token else {}
                                        try:
                                            resp = requests.delete(f"{base_url}/food/{advert.get('id')}", headers=headers, timeout=15)
                                            if 200 <= resp.status_code < 300:
                                                ui.notify('Advert deleted successfully', type='positive')
                                                confirm_dialog.close()
                                                dialog.close()
                                                # Refresh the page
                                                ui.navigate.to('/view_advert')
                                            else:
                                                try:
                                                    err = resp.json()
                                                    msg = err.get('message') or err.get('detail') or str(err)
                                                except Exception:
                                                    msg = resp.text
                                                ui.notify(f"Delete failed: {msg}", type='negative')
                                        except Exception as e:
                                            ui.notify(f"Delete error: {e}", type='negative')
                                    
                                    ui.button('Delete', on_click=delete_advert).classes(
                                        'px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105'
                                    ).style('border: none;')
                            
                            confirm_dialog.open()
                        
                        ui.button('Delete', on_click=confirm_delete).classes(
                            'px-8 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105'
                        ).style('border: none;')
                        
                        # Show ownership indicator
                        if not is_owner:
                            ui.label('(Not your advert)').classes('text-xs text-gray-500 ml-2')
        
        dialog.open()

    def render_cards():
        results_container.clear()
        query = (search_box.value or "").lower()
        for r in restaurants:
            if query in r["name"].lower() or query in r["description"].lower():
                with results_container:
                    with ui.card().classes("w-60 shadow-md hover:shadow-lg transition p-3"):
                        if r.get("image"):
                            ui.image(r["image"]).classes("rounded-lg h-32 w-full object-cover")
                        else:
                            ui.element('div').classes('h-32 w-full bg-gray-200 rounded-lg flex items-center justify-center').add(
                                ui.label('No Image').classes('text-gray-500')
                            )
                        ui.label(r["name"]).classes("text-lg font-semibold mt-2")
                        ui.label(r["description"][:50] + "..." if len(r.get("description", "")) > 50 else r.get("description", "")).classes("text-sm text-gray-600 mb-2")
                        ui.label(f"${r.get('price', 'N/A')}").classes("text-lg font-bold text-green-600 mb-2")
                        ui.button("View Details", on_click=lambda advert=r: show_advert_modal(advert)).classes(
                            "w-full px-6 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                        ).style('border: none;')

    # First render
    render_cards()

    # Update on input
    search_box.on('input', lambda e: render_cards())
    
    # Add footer
    show_footer()
