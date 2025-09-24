from nicegui import ui
import requests
from utils.api import base_url
from utils.auth import get_role, get_user_id, get_token
from components.footer import show_footer

@ui.page("/vendor/dashboard")
def show_vendor_dashboard():
    role = get_role()
    if role != 'vendor':
        ui.label("Access Denied").classes("text-2xl text-red-600 text-center mt-20")
        ui.label("Please log in as a vendor to access this page.").classes("text-gray-600 text-center")
        ui.button("Go to Sign In", on_click=lambda: ui.navigate.to('/sign-in')).classes(
            "mt-4 px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
        )
        return

    # State management for view toggle
    view_mode = {'value': 'grid'}  # 'grid' or 'list'

    with ui.row().classes("w-full min-h-screen bg-gray-50"):
        # Sidebar
        with ui.column().classes("w-[20%] bg-white shadow-lg min-h-screen"):
            show_side_bar()

        # Main content area
        with ui.column().classes("w-[80%] p-6"):
            # Header with title and quick actions
            with ui.row().classes("w-full items-center justify-between mb-8"):
                ui.label("Vendor Dashboard").classes("text-3xl font-bold text-gray-900")
                with ui.row().classes("gap-3"):
                    ui.button("📊 Analytics", on_click=lambda: ui.notify("Analytics coming soon!")).classes(
                        "px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-xl hover:from-green-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )
                    ui.button("➕ New Advert", on_click=lambda: ui.navigate.to('/vendor/add_advert')).classes(
                        "px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

            # Summary Statistics Section
            with ui.row().classes("w-full gap-6 mb-8"):
                # Total Adverts Card
                with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-blue-500 to-blue-600 text-white"):
                    ui.label("📋 Total Adverts").classes("text-lg font-semibold mb-2")
                    total_ads = ui.label("0").classes("text-3xl font-bold")

                # Active Adverts Card
                with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-green-500 to-green-600 text-white"):
                    ui.label("✅ Active Adverts").classes("text-lg font-semibold mb-2")
                    active_ads = ui.label("0").classes("text-3xl font-bold")

                # Total Views Card
                with ui.card().classes("flex-1 p-6 bg-gradient-to-r from-purple-500 to-purple-600 text-white"):
                    ui.label("👁️ Total Views").classes("text-lg font-semibold mb-2")
                    total_views = ui.label("0").classes("text-3xl font-bold")

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

            def toggle_view(mode):
                view_mode['value'] = mode
                refresh_list()

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

                # Filter by vendor and search
                mine = [it for it in items if str((it.get('owner_id') or it.get('vendor_id') or '')) == str(vendor_id)]
                search_term = search_input.value.lower() if search_input.value else ""
                if search_term:
                    mine = [it for it in mine if search_term in it.get('name', '').lower() or search_term in it.get('description', '').lower()]

                # Update statistics
                total_ads.set_text(str(len(mine)))
                active_ads.set_text(str(len([it for it in mine if it.get('is_active', True)])))
                total_views.set_text("1,234")  # TODO: Get actual view count from API

                if not mine:
                    with container:
                        with ui.card().classes("w-full p-8 text-center bg-gray-50"):
                            ui.label("No adverts found").classes("text-xl text-gray-600 mb-4")
                            ui.button("Create Your First Advert", on_click=lambda: ui.navigate.to('/vendor/add_advert')).classes(
                                "px-8 py-4 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                            )
                    return

                # Display adverts based on view mode
                if view_mode['value'] == 'grid':
                    # Grid View
                    with container:
                        with ui.grid().classes("grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"):
                            for it in mine:
                                create_advert_card(it, headers)
                else:
                    # List View
                    with container:
                        for it in mine:
                            create_advert_list_item(it, headers)

            def create_advert_card(advert, headers):
                """Create a card for grid view"""
                with ui.card().classes("overflow-hidden hover:shadow-lg transition-shadow"):
                    # Image placeholder or actual image
                    with ui.card_section().classes("p-0"):
                        ui.image("https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=250&fit=crop&auto=format&q=80").classes(
                            "w-full h-48 object-cover"
                        )

                    with ui.card_section().classes("p-4"):
                        ui.label(advert.get('name', 'No name')).classes("text-lg font-bold text-gray-900 mb-2")
                        ui.label(f"GH₵ {advert.get('price', 0)}").classes("text-xl font-semibold text-green-600 mb-2")
                        ui.label(advert.get('description', 'No description')[:100] + "...").classes("text-gray-600 text-sm mb-4")

                        with ui.row().classes("w-full justify-between items-center"):
                            with ui.row().classes("gap-2"):
                                ui.button("Edit", on_click=lambda _=None, id=advert.get('id'):
                                         ui.navigate.to(f"/vendor/edit_advert/{id}")).classes(
                                    "px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                                )

                                def do_delete(id=advert.get('id')):
                                    try:
                                        d = requests.delete(f"{base_url}/food/{id}", headers=headers, timeout=15)
                                        if 200 <= d.status_code < 300:
                                            ui.notify('Deleted successfully', type='positive')
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

                                ui.button("Delete", on_click=do_delete).classes(
                                    "px-4 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                                )

            def create_advert_list_item(advert, headers):
                """Create a list item for list view"""
                with ui.card().classes("w-full p-4 hover:shadow-md transition-shadow"):
                    with ui.row().classes("w-full items-center justify-between"):
                        with ui.column().classes("flex-1"):
                            ui.label(advert.get('name', 'No name')).classes("text-lg font-bold text-gray-900")
                            ui.label(f"GH₵ {advert.get('price', 0)}").classes("text-green-600 font-semibold")
                            ui.label(advert.get('description', 'No description')[:150] + "...").classes("text-gray-600 text-sm")

                        with ui.row().classes("gap-2"):
                            ui.button("Edit", on_click=lambda _=None, id=advert.get('id'):
                                     ui.navigate.to(f"/vendor/edit_advert/{id}")).classes(
                                "px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-lg hover:from-blue-600 hover:to-blue-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                            )

                            def do_delete(id=advert.get('id')):
                                try:
                                    d = requests.delete(f"{base_url}/food/{id}", headers=headers, timeout=15)
                                    if 200 <= d.status_code < 300:
                                        ui.notify('Deleted successfully', type='positive')
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

                            ui.button("Delete", on_click=do_delete).classes(
                                "px-6 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-lg hover:from-red-600 hover:to-red-700 font-semibold shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
                            )

            refresh_list()

    # Add footer
    show_footer()

def show_side_bar():
    """Simple sidebar for vendor navigation"""
    with ui.column().classes("p-6 bg-gradient-to-b from-green-50 to-emerald-50 h-screen border-r-2 border-green-100"):
        ui.label("Vendor Menu").classes("text-2xl font-bold mb-6 text-green-800")
        ui.link("Dashboard", "/vendor/dashboard").classes("block mb-3 px-4 py-3 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 hover:text-green-900 font-semibold transition-all duration-300")
        ui.link("Add Advert", "/vendor/add_advert").classes("block mb-3 px-4 py-3 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 hover:text-green-900 font-semibold transition-all duration-300")
        ui.link("View All", "/view_advert").classes("block mb-3 px-4 py-3 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 hover:text-green-900 font-semibold transition-all duration-300")
        ui.link("Home", "/").classes("block mb-3 px-4 py-3 bg-green-100 text-green-800 rounded-lg hover:bg-green-200 hover:text-green-900 font-semibold transition-all duration-300")
