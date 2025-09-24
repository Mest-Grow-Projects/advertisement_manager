from nicegui import ui, app
import requests
from typing import List, Dict, Any, Optional
from utils.api import base_url
from utils.auth import get_role, require_vendor, get_user_id, get_token, clear_session
from utils.frontend_store import list_adverts, create_advert, update_advert, delete_advert, get_advert
from components.footer import show_footer

# Global state for view mode
view_mode = {'value': 'grid'}  # 'grid' or 'list'

def show_vendor_sidebar():
    """Vendor sidebar with navigation"""
    ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Caveat:wght@400..700&family=Gwendolyn:wght@400;700&family=Josefin+Sans:ital,wght@0,100..700;1,100..700&family=Lavishly+Yours&family=Stoke:wght@300;400&display=swap" rel="stylesheet">')

    ui.query('.nicegui-content').classes('m-0 p-0 gap-0')
    with ui.column().classes(
        "bg-gray-100 p-4 w-full shadow-lg h-full justify-between items-center"
    ).style('font-family: "Stoke", serif; font-style: normal;'):
        # Top section with branding and vendor info
        with ui.column().classes("w-full items-center mb-6"):
            ui.link("🍔 BiteBridge", "/vendor/dashboard").classes(
                "text-2xl font-extrabold text-green-600 no-underline"
            ).style('font-family: "Gwendolyn", cursive; font-weight: 700; font-style: normal')
            ui.label("Vendor Portal").classes("text-lg font-bold text-gray-800")

        ui.separator().classes("w-full bg-green-500 h-0.5 mb-6")

        # Navigation links section
        with ui.column().classes("w-full space-y-4 flex-grow"):
            # Dashboard
            with ui.row().classes(
                "w-full items-center cursor-pointer hover:bg-green-200 transition-colors p-2 rounded-lg"
            ):
                ui.icon("dashboard").classes("text-green-600")
                ui.link("Dashboard", "/vendor/dashboard").classes(
                    "text-gray-700 font-semibold no-underline text-lg"
                )

            # Create Advert
            with ui.row().classes(
                "w-full items-center cursor-pointer hover:bg-green-200 transition-colors p-2 rounded-lg"
            ):
                ui.icon("add_box").classes("text-green-600")
                ui.link("Create Advert", "/vendor/create_advert").classes(
                    "text-gray-700 font-semibold no-underline text-lg"
                )

            # View Adverts
            with ui.row().classes(
                "w-full items-center cursor-pointer hover:bg-green-200 transition-colors p-2 rounded-lg"
            ):
                ui.icon("view_list").classes("text-green-600")
                ui.link("My Adverts", "/vendor/adverts").classes(
                    "text-gray-700 font-semibold no-underline text-lg"
                )

            # Analytics
            with ui.row().classes(
                "w-full items-center cursor-pointer hover:bg-green-200 transition-colors p-2 rounded-lg"
            ):
                ui.icon("analytics").classes("text-green-600")
                ui.link("Analytics", "/vendor/analytics").classes(
                    "text-gray-700 font-semibold no-underline text-lg"
                )

            # Settings
            with ui.row().classes(
                "w-full items-center cursor-pointer hover:bg-green-200 transition-colors p-2 rounded-lg"
            ):
                ui.icon("settings").classes("text-green-600")
                ui.link("Settings", "/vendor/settings").classes(
                    "text-gray-700 font-semibold no-underline text-lg"
                )

        # Logout button at the bottom
        with ui.column().classes("w-full items-center mt-auto"):
            ui.separator().classes("w-full bg-green-500 h-0.5 my-6")
            with ui.row().classes(
                "w-full items-center cursor-pointer p-2 rounded-lg hover:bg-red-100 transition-colors"
            ):
                ui.icon("logout").classes("text-red-600")
                ui.button(
                    "Logout", on_click=lambda: (clear_session(), ui.navigate.to('/'))
                ).classes(
                    "bg-transparent text-red-600 font-semibold shadow-none text-lg"
                ).props(
                    "flat no-caps"
                )

def show_vendor_dashboard():
    """Main vendor dashboard with statistics and overview"""
    if not require_vendor():
        return

    with ui.row().classes("w-full min-h-screen bg-gray-50"):
        # Sidebar
        with ui.column().classes("w-[20%] bg-white shadow-lg min-h-screen"):
            show_vendor_sidebar()

        # Main content area
        with ui.column().classes("w-[80%] p-6"):
            # Header with title and quick actions
            with ui.row().classes("w-full items-center justify-between mb-8"):
                ui.label("Vendor Dashboard").classes("text-3xl font-bold text-gray-900")
                with ui.row().classes("gap-3"):
                    ui.button("📊 Analytics", on_click=lambda: ui.notify("Analytics coming soon!")).classes(
                        "px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )
                    ui.button("➕ New Advert", on_click=lambda: ui.navigate.to('/vendor/create_advert')).classes(
                        "px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

            # Summary Statistics Section
            show_dashboard_stats()

            # View Toggle and Search
            with ui.row().classes("w-full items-center justify-between mb-6"):
                with ui.row().classes("gap-3"):
                    ui.button("Grid View", on_click=lambda: toggle_view('grid')).classes(
                        "px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105" if view_mode['value'] == 'list' else "px-6 py-3 bg-gradient-to-r from-emerald-600 to-green-700 text-white rounded-xl hover:from-emerald-700 hover:to-green-800 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )
                    ui.button("List View", on_click=lambda: toggle_view('list')).classes(
                        "px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105" if view_mode['value'] == 'grid' else "px-6 py-3 bg-gradient-to-r from-emerald-600 to-green-700 text-white rounded-xl hover:from-emerald-700 hover:to-green-800 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

                # Search input
                search_input = ui.input("Search adverts...").classes("w-64 px-4 py-3 border-2 border-green-200 rounded-xl focus:border-green-500 focus:outline-none transition-colors").props("outlined dense")

            # Adverts Container
            container = ui.column().classes("gap-4 w-full")
            show_vendor_adverts(container, search_input)

    # Add footer
    show_footer()

def show_dashboard_stats():
    """Show dashboard statistics cards"""
    vendor_id = get_user_id()
    if not vendor_id:
        return

    # Get user adverts for statistics
    try:
        # Try remote API first
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        r = requests.get(f"{base_url}/food/all", headers=headers, timeout=15)
        if 200 <= r.status_code < 300:
            data = r.json()
            all_adverts = data.get('data', [])
        else:
            all_adverts = list_adverts()
    except Exception:
        all_adverts = list_adverts()

    # Filter by vendor
    user_adverts = [adv for adv in all_adverts if str(adv.get('owner_id', '')) == str(vendor_id)]

    # Calculate statistics
    total_ads = len(user_adverts)
    active_ads = len([adv for adv in user_adverts if adv.get('is_active', True)])

    # Category breakdown
    categories = {}
    for adv in user_adverts:
        cat = adv.get('category', 'Uncategorized')
        categories[cat] = categories.get(cat, 0) + 1

    with ui.row().classes("w-full gap-6 mb-8"):
        # Total Adverts Card
        with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white"):
            ui.label("📋 Total Adverts").classes("text-lg font-semibold mb-2")
            total_ads_label = ui.label(str(total_ads)).classes("text-3xl font-bold")

        # Active Adverts Card
        with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-green-500 to-green-600 text-white"):
            ui.label("✅ Active Adverts").classes("text-lg font-semibold mb-2")
            active_ads_label = ui.label(str(active_ads)).classes("text-3xl font-bold")

        # Categories Card
        with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-purple-500 to-purple-600 text-white"):
            ui.label("🏷️ Categories").classes("text-lg font-semibold mb-2")
            categories_label = ui.label(str(len(categories))).classes("text-3xl font-bold")

        # Total Views Card (placeholder)
        with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-orange-500 to-orange-600 text-white"):
            ui.label("👁️ Total Views").classes("text-lg font-semibold mb-2")
            views_label = ui.label("1,234").classes("text-3xl font-bold")

def toggle_view(mode: str):
    """Toggle between grid and list view"""
    view_mode['value'] = mode

def show_vendor_adverts(container, search_input):
    """Show vendor adverts in container"""
    def refresh_adverts():
        container.clear()
        vendor_id = get_user_id()
        if not vendor_id:
            return

        try:
            # Try remote API first
            token = get_token()
            headers = {"Authorization": f"Bearer {token}"} if token else {}

            r = requests.get(f"{base_url}/food/all", headers=headers, timeout=15)
            if 200 <= r.status_code < 300:
                data = r.json()
                all_adverts = data.get('data', [])
            else:
                all_adverts = list_adverts()
        except Exception:
            all_adverts = list_adverts()

        # Filter by vendor and search
        user_adverts = [adv for adv in all_adverts if str(adv.get('owner_id', '')) == str(vendor_id)]
        search_term = search_input.value.lower() if search_input.value else ""
        if search_term:
            user_adverts = [adv for adv in user_adverts if
                          search_term in adv.get('name', '').lower() or
                          search_term in adv.get('description', '').lower()]

        if not user_adverts:
            with container:
                with ui.card().classes("w-full p-8 text-center bg-gray-50"):
                    ui.label("No adverts found").classes("text-xl text-gray-600 mb-4")
                    ui.button("Create Your First Advert", on_click=lambda: ui.navigate.to('/vendor/create_advert')).classes(
                        "px-8 py-4 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )
            return

        # Display adverts based on view mode
        if view_mode['value'] == 'grid':
            with container:
                with ui.grid().classes("grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"):
                    for advert in user_adverts:
                        create_advert_card(advert)
        else:
            with container:
                for advert in user_adverts:
                    create_advert_list_item(advert)

    def create_advert_card(advert):
        """Create a card for grid view"""
        with ui.card().classes("overflow-hidden hover:shadow-lg transition-shadow"):
            # Image placeholder or actual image
            with ui.card_section().classes("p-0"):
                image_url = advert.get('image', 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=250&fit=crop&auto=format&q=80')
                ui.image(image_url).classes("w-full h-48 object-cover")

            with ui.card_section().classes("p-4"):
                ui.label(advert.get('name', 'No name')).classes("text-lg font-bold text-gray-900 mb-2")
                ui.label(f"GH₵ {advert.get('price', 0)}").classes("text-xl font-semibold text-green-600 mb-2")
                ui.label(advert.get('description', 'No description')[:100] + "...").classes("text-gray-600 text-sm mb-4")

                with ui.row().classes("w-full justify-between items-center"):
                    with ui.row().classes("gap-2"):
                        ui.button("Edit", on_click=lambda: edit_advert(advert.get('id'))).classes(
                            "px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                        )

                        def do_delete(adv_id=advert.get('id')):
                            try:
                                # Try remote API first
                                token = get_token()
                                headers = {"Authorization": f"Bearer {token}"} if token else {}

                                d = requests.delete(f"{base_url}/food/{adv_id}", headers=headers, timeout=15)
                                if 200 <= d.status_code < 300:
                                    ui.notify('Advert deleted successfully', type='positive')
                                    refresh_adverts()
                                else:
                                    # Fallback to local delete
                                    delete_advert(str(adv_id))
                                    ui.notify('Advert deleted successfully (local)', type='positive')
                                    refresh_adverts()
                            except Exception as e:
                                # Fallback to local delete
                                try:
                                    delete_advert(str(adv_id))
                                    ui.notify('Advert deleted successfully (local)', type='positive')
                                    refresh_adverts()
                                except Exception as local_e:
                                    ui.notify(f"Delete failed: {local_e}", type='negative')

                        ui.button("Delete", on_click=do_delete).classes(
                            "px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                        )

    def create_advert_list_item(advert):
        """Create a list item for list view"""
        with ui.card().classes("w-full p-4 hover:shadow-md transition-shadow"):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("flex-1"):
                    ui.label(advert.get('name', 'No name')).classes("text-lg font-bold text-gray-900")
                    ui.label(f"GH₵ {advert.get('price', 0)}").classes("text-green-600 font-semibold")
                    ui.label(advert.get('description', 'No description')[:150] + "...").classes("text-gray-600 text-sm")

                with ui.row().classes("gap-2"):
                    ui.button("Edit", on_click=lambda: edit_advert(advert.get('id'))).classes(
                        "px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                    )

                    def do_delete(adv_id=advert.get('id')):
                        try:
                            # Try remote API first
                            token = get_token()
                            headers = {"Authorization": f"Bearer {token}"} if token else {}

                            d = requests.delete(f"{base_url}/food/{adv_id}", headers=headers, timeout=15)
                            if 200 <= d.status_code < 300:
                                ui.notify('Advert deleted successfully', type='positive')
                                refresh_adverts()
                            else:
                                # Fallback to local delete
                                delete_advert(str(adv_id))
                                ui.notify('Advert deleted successfully (local)', type='positive')
                                refresh_adverts()
                        except Exception as e:
                            # Fallback to local delete
                            try:
                                delete_advert(str(adv_id))
                                ui.notify('Advert deleted successfully (local)', type='positive')
                                refresh_adverts()
                            except Exception as local_e:
                                ui.notify(f"Delete failed: {local_e}", type='negative')

                    ui.button("Delete", on_click=do_delete).classes(
                        "px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                    )

    def edit_advert(advert_id):
        """Navigate to edit advert page"""
        ui.navigate.to(f'/vendor/edit_advert/{advert_id}')

    refresh_adverts()

def show_create_advert():
    """Show create advert form"""
    if not require_vendor():
        return

    ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Caveat:wght@400..700&family=Gwendolyn:wght@400;700&family=Josefin+Sans:ital,wght@0,100..700;1,100..700&family=Lavishly+Yours&family=Stoke:wght@300;400&display=swap" rel="stylesheet">')

    ui.query(".nicegui-content").classes('m-0 p-0 gap-0')
    with ui.element('main').classes('w-full h-full flex flex-col justify-center items-center p-4').style('font-family: "Josefin Sans", sans-serif'):
        with ui.card().classes('w-[50%] flex flex-col justify-center items-center shadow-lg bg-gray-100'):
            ui.label("🍔 BiteBridge").style('font-family: "Gwendolyn", cursive; font-weight: 700; font-style: normal').classes('text-2xl font-bold text-gray-800')
            ui.label("Create New Advert").classes('text-xl font-bold text-green-900')
            ui.separator().classes('w-[20%] h-0.5 bg-green-800')

            advert_title = ui.input(label="Title", placeholder="Enter advert title").classes('w-full bg-white px-2').props('borderless')
            advert_description = ui.textarea(label="Description", placeholder="Enter advert description").classes('w-full bg-white px-2').props('borderless')
            advert_price = ui.number(label="Price", placeholder="Enter price").classes('w-full bg-white px-w').props('borderless')
            advert_category = ui.input(label="Category", placeholder="Enter category").classes('w-full bg-white').props('borderless')

            # Image upload
            uploaded_image = None
            ui.upload(auto_upload=True, on_upload=lambda e: setattr(uploaded_image, 'content', e.content)).classes('w-full mb-4').props('color=green')

            def create_advert_handler():
                if not all([advert_title.value, advert_description.value, advert_price.value, advert_category.value]):
                    ui.notify("Please fill in all fields!", type="negative")
                    return

                try:
                    # Try remote API first
                    token = get_token()
                    headers = {"Authorization": f"Bearer {token}"} if token else {}
                    data = {
                        "name": advert_title.value,
                        "description": advert_description.value,
                        "price": advert_price.value,
                        "category": advert_category.value
                    }
                    files = {"image": uploaded_image.content} if uploaded_image and hasattr(uploaded_image, 'content') else {}

                    response = requests.post(url=f"{base_url}/food", data=data, files=files, headers=headers, timeout=15)
                    if response.status_code == 200:
                        ui.notify("Advert created successfully!", type="positive")
                        ui.navigate.to('/vendor/dashboard')
                        return

                except Exception as e:
                    # Fallback to local storage
                    try:
                        vendor_id = get_user_id()
                        if not vendor_id:
                            ui.notify("Authentication error. Please log in again.", type="negative")
                            return

                        image_data = uploaded_image.content.decode() if uploaded_image and hasattr(uploaded_image, 'content') else ''

                        create_advert(
                            name=advert_title.value,
                            description=advert_description.value,
                            price=float(advert_price.value),
                            owner_id=vendor_id,
                            image=image_data
                        )
                        ui.notify("Advert created successfully (local)!", type="positive")
                        ui.navigate.to('/vendor/dashboard')
                        return
                    except Exception as local_e:
                        ui.notify(f"Failed to create advert: {local_e}", type="negative")
                        return

                ui.notify("Failed to create advert. Please try again.", type="negative")

            ui.button(text="Create Advert", on_click=create_advert_handler).props('flat dense').classes('bg-green-600 text-white w-[80%] py-2').style('border: solid 2px gray')

    # Add footer
    show_footer()

def show_vendor_adverts_list():
    """Show all vendor adverts in a dedicated page"""
    if not require_vendor():
        return

    with ui.row().classes("w-full min-h-screen bg-gray-50"):
        # Sidebar
        with ui.column().classes("w-[20%] bg-white shadow-lg min-h-screen"):
            show_vendor_sidebar()

        # Main content area
        with ui.column().classes("w-[80%] p-6"):
            # Header
            with ui.row().classes("w-full items-center justify-between mb-8"):
                ui.label("My Adverts").classes("text-3xl font-bold text-gray-900")
                ui.button("➕ New Advert", on_click=lambda: ui.navigate.to('/vendor/create_advert')).classes(
                    "px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                )

            # View Toggle and Search
            with ui.row().classes("w-full items-center justify-between mb-6"):
                with ui.row().classes("gap-3"):
                    ui.button("Grid View", on_click=lambda: toggle_view('grid')).classes(
                        "px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105" if view_mode['value'] == 'list' else "px-6 py-3 bg-gradient-to-r from-emerald-600 to-green-700 text-white rounded-xl hover:from-emerald-700 hover:to-green-800 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )
                    ui.button("List View", on_click=lambda: toggle_view('list')).classes(
                        "px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105" if view_mode['value'] == 'grid' else "px-6 py-3 bg-gradient-to-r from-emerald-600 to-green-700 text-white rounded-xl hover:from-emerald-700 hover:to-green-800 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

                search_input = ui.input("Search adverts...").classes("w-64 px-4 py-3 border-2 border-green-200 rounded-xl focus:border-green-500 focus:outline-none transition-colors").props("outlined dense")

            # Adverts Container
            container = ui.column().classes("gap-4 w-full")
            show_vendor_adverts(container, search_input)

    # Add footer
    show_footer()

def show_edit_advert(advert_id: str):
    """Show edit advert form"""
    if not require_vendor():
        return

    # Get advert data
    try:
        # Try remote API first
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        r = requests.get(f"{base_url}/food/{advert_id}", headers=headers, timeout=15)
        if 200 <= r.status_code < 300:
            advert_data = r.json()
        else:
            advert_data = get_advert(advert_id)
    except Exception:
        advert_data = get_advert(advert_id)

    if not advert_data:
        ui.label("Advert not found").classes("text-xl text-red-600")
        return

    ui.add_head_html('<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Caveat:wght@400..700&family=Gwendolyn:wght@400;700&family=Josefin+Sans:ital,wght@0,100..700;1,100..700&family=Lavishly+Yours&family=Stoke:wght@300;400&display=swap" rel="stylesheet">')

    ui.query(".nicegui-content").classes('m-0 p-0 gap-0')
    with ui.element('main').classes('w-full h-full flex flex-col justify-center items-center p-4').style('font-family: "Josefin Sans", sans-serif'):
        with ui.card().classes('w-[50%] flex flex-col justify-center items-center shadow-lg bg-gray-100'):
            ui.label("🍔 BiteBridge").style('font-family: "Gwendolyn", cursive; font-weight: 700; font-style: normal').classes('text-2xl font-bold text-gray-800')
            ui.label("Edit Advert").classes('text-xl font-bold text-green-900')
            ui.separator().classes('w-[20%] h-0.5 bg-green-800')

            advert_title = ui.input(label="Title", value=advert_data.get('name', '')).classes('w-full bg-white px-2').props('borderless')
            advert_description = ui.textarea(label="Description", value=advert_data.get('description', '')).classes('w-full bg-white px-2').props('borderless')
            advert_price = ui.number(label="Price", value=advert_data.get('price', 0)).classes('w-full bg-white px-w').props('borderless')
            advert_category = ui.input(label="Category", value=advert_data.get('category', '')).classes('w-full bg-white').props('borderless')

            def update_advert_handler():
                if not all([advert_title.value, advert_description.value, advert_price.value, advert_category.value]):
                    ui.notify("Please fill in all fields!", type="negative")
                    return

                try:
                    # Try remote API first
                    token = get_token()
                    headers = {"Authorization": f"Bearer {token}"} if token else {}
                    data = {
                        "name": advert_title.value,
                        "description": advert_description.value,
                        "price": advert_price.value,
                        "category": advert_category.value
                    }

                    response = requests.put(url=f"{base_url}/food/{advert_id}", json=data, headers=headers, timeout=15)
                    if response.status_code == 200:
                        ui.notify("Advert updated successfully!", type="positive")
                        ui.navigate.to('/vendor/dashboard')
                        return

                except Exception as e:
                    # Fallback to local storage
                    try:
                        update_advert(
                            advert_id=advert_id,
                            name=advert_title.value,
                            description=advert_description.value,
                            price=float(advert_price.value)
                        )
                        ui.notify("Advert updated successfully (local)!", type="positive")
                        ui.navigate.to('/vendor/dashboard')
                        return
                    except Exception as local_e:
                        ui.notify(f"Failed to update advert: {local_e}", type="negative")
                        return

                ui.notify("Failed to update advert. Please try again.", type="negative")

            with ui.row().classes("w-full justify-between"):
                ui.button(text="Cancel", on_click=lambda: ui.navigate.to('/vendor/dashboard')).classes('bg-gray-500 text-white px-6 py-2')
                ui.button(text="Update Advert", on_click=update_advert_handler).props('flat dense').classes('bg-green-600 text-white px-6 py-2')

    # Add footer
    show_footer()
