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

    # Add custom CSS for enhanced styling
    ui.add_head_html('''
    <style>
    .line-clamp-2 {
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }

    .gradient-text {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .card-hover-effect:hover {
        transform: translateY(-8px) rotate(1deg);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }
    </style>
    ''')

    with ui.row().classes("w-full min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100"):
        # Sidebar
        with ui.column().classes("w-[20%] bg-white shadow-lg min-h-screen"):
            show_vendor_sidebar()

        # Main content area
        with ui.column().classes("w-[80%] p-6"):
            # Header with title and quick actions
            with ui.row().classes("w-full items-center justify-between mb-8"):
                with ui.column():
                    ui.label("🍳 Vendor Dashboard").classes("text-4xl font-bold gradient-text mb-2")
                    ui.label("Manage your restaurant's delicious offerings").classes("text-gray-600 text-lg")

                with ui.row().classes("gap-3"):
                    ui.button("📊 Analytics", on_click=lambda: ui.notify("Analytics coming soon!")).classes(
                        "px-6 py-3 bg-gradient-to-r from-purple-500 to-purple-600 text-white rounded-xl hover:from-purple-600 hover:to-purple-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
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
        with ui.card().classes("flex-1 p-8 bg-gradient-to-br from-blue-500 via-blue-600 to-blue-700 text-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border-0 relative overflow-hidden"):
            # Background pattern
            with ui.element().classes("absolute top-0 right-0 opacity-10"):
                ui.icon("restaurant_menu", size="120px").classes("text-white")

            with ui.column().classes("relative z-10"):
                ui.label("📋 Total Adverts").classes("text-lg font-semibold mb-3 opacity-90")
                total_ads_label = ui.label(str(total_ads)).classes("text-5xl font-bold mb-2")
                ui.label("Active listings").classes("text-sm opacity-75")

        # Active Adverts Card
        with ui.card().classes("flex-1 p-8 bg-gradient-to-br from-emerald-500 via-green-600 to-green-700 text-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border-0 relative overflow-hidden"):
            # Background pattern
            with ui.element().classes("absolute top-0 right-0 opacity-10"):
                ui.icon("check_circle", size="120px").classes("text-white")

            with ui.column().classes("relative z-10"):
                ui.label("✅ Active Adverts").classes("text-lg font-semibold mb-3 opacity-90")
                active_ads_label = ui.label(str(active_ads)).classes("text-5xl font-bold mb-2")
                ui.label("Currently visible").classes("text-sm opacity-75")

        # Categories Card
        with ui.card().classes("flex-1 p-8 bg-gradient-to-br from-purple-500 via-purple-600 to-purple-700 text-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border-0 relative overflow-hidden"):
            # Background pattern
            with ui.element().classes("absolute top-0 right-0 opacity-10"):
                ui.icon("category", size="120px").classes("text-white")

            with ui.column().classes("relative z-10"):
                ui.label("🏷️ Categories").classes("text-lg font-semibold mb-3 opacity-90")
                categories_label = ui.label(str(len(categories))).classes("text-5xl font-bold mb-2")
                ui.label("Menu categories").classes("text-sm opacity-75")

        # Total Views Card (placeholder)
        with ui.card().classes("flex-1 p-8 bg-gradient-to-br from-orange-500 via-orange-600 to-orange-700 text-white rounded-2xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1 border-0 relative overflow-hidden"):
            # Background pattern
            with ui.element().classes("absolute top-0 right-0 opacity-10"):
                ui.icon("visibility", size="120px").classes("text-white")

            with ui.column().classes("relative z-10"):
                ui.label("👁️ Total Views").classes("text-lg font-semibold mb-3 opacity-90")
                views_label = ui.label("1,234").classes("text-5xl font-bold mb-2")
                ui.label("Customer views").classes("text-sm opacity-75")

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
                with ui.card().classes("w-full p-12 text-center bg-gradient-to-br from-gray-50 to-gray-100 border-2 border-dashed border-gray-300 rounded-2xl"):
                    # Icon
                    with ui.element().classes("mb-6"):
                        ui.icon("restaurant", size="80px").classes("text-gray-400")

                    # Main message
                    ui.label("No adverts found").classes("text-2xl font-bold text-gray-700 mb-3")

                    # Subtitle
                    ui.label("Start by creating your first delicious advert to showcase your restaurant's offerings").classes("text-gray-500 text-lg mb-8 max-w-md mx-auto leading-relaxed")

                    # Create button
                    ui.button("🍳 Create Your First Advert", on_click=lambda: ui.navigate.to('/vendor/create_advert')).classes(
                        "px-8 py-4 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 text-lg"
                    )

                    # Tips section
                    with ui.element().classes("mt-8 p-6 bg-white rounded-xl shadow-sm"):
                        ui.label("💡 Tips for Great Adverts:").classes("text-lg font-semibold text-gray-800 mb-4")
                        with ui.column().classes("gap-2 text-left"):
                            ui.label("• Use high-quality food photos").classes("text-gray-600")
                            ui.label("• Write compelling descriptions").classes("text-gray-600")
                            ui.label("• Set competitive prices").classes("text-gray-600")
                            ui.label("• Choose relevant categories").classes("text-gray-600")

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
        """Create a modern, aesthetically pleasing card for grid view"""
        # Modern image URLs for food/restaurant themes
        food_images = [
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=250&fit=crop&auto=format&q=80',  # Pizza
            'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&h=250&fit=crop&auto=format&q=80',  # Burger
            'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=250&fit=crop&auto=format&q=80',  # Pasta
            'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=250&fit=crop&auto=format&q=80',  # Sushi
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=250&fit=crop&auto=format&q=80',  # Steak
            'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=250&fit=crop&auto=format&q=80',  # Salad
            'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=400&h=250&fit=crop&auto=format&q=80',  # Tacos
            'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=250&fit=crop&auto=format&q=80',  # Chicken
        ]

        # Use advert image if available, otherwise use a random food image
        image_url = advert.get('image')
        if not image_url or image_url.startswith('data:'):
            import random
            image_url = random.choice(food_images)

        # Get category color
        category = advert.get('category', 'General').lower()
        category_colors = {
            'pizza': 'bg-red-500',
            'burger': 'bg-yellow-500',
            'pasta': 'bg-orange-500',
            'sushi': 'bg-pink-500',
            'steak': 'bg-purple-500',
            'salad': 'bg-green-500',
            'tacos': 'bg-blue-500',
            'chicken': 'bg-indigo-500',
        }
        category_color = category_colors.get(category, 'bg-gray-500')

        with ui.card().classes("group relative overflow-hidden bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-2 border-0 card-hover-effect"):
            # Image section with overlay
            with ui.card_section().classes("relative p-0 overflow-hidden"):
                ui.image(image_url).classes("w-full h-56 object-cover transition-transform duration-500 group-hover:scale-110")

                # Gradient overlay
                with ui.element().classes("absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"):
                    pass

                # Category badge
                with ui.element().classes(f"absolute top-4 left-4 {category_color} text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide"):
                    ui.label(category.title())

                # Price badge
                with ui.element().classes("absolute top-4 right-4 bg-white/90 backdrop-blur-sm text-green-600 px-3 py-2 rounded-full font-bold text-lg shadow-lg"):
                    ui.label(f"GH₵ {advert.get('price', 0)}")

                # Status indicator (Active/Inactive)
                status = advert.get('is_active', True)
                status_color = "bg-green-500" if status else "bg-red-500"
                with ui.element().classes(f"absolute bottom-4 right-4 {status_color} text-white px-2 py-1 rounded-full text-xs font-semibold"):
                    ui.label("Active" if status else "Inactive")

            # Content section
            with ui.card_section().classes("p-6"):
                # Title with truncation
                title = advert.get('name', 'No name')
                with ui.element().classes("mb-3"):
                    ui.label(title).classes("text-xl font-bold text-gray-900 leading-tight line-clamp-2")

                # Description with better formatting
                description = advert.get('description', 'No description')
                truncated_desc = description[:120] + "..." if len(description) > 120 else description
                with ui.element().classes("mb-4"):
                    ui.label(truncated_desc).classes("text-gray-600 text-sm leading-relaxed")

                # Rating stars (placeholder for future implementation)
                with ui.element().classes("flex items-center mb-4"):
                    # Star rating placeholder
                    with ui.row().classes("gap-1"):
                        for i in range(5):
                            ui.icon("star", size="16px").classes("text-yellow-400")
                    ui.label("(4.5)").classes("text-gray-500 text-sm ml-2")

                # Action buttons with modern styling
                with ui.row().classes("w-full gap-3"):
                    ui.button("👁️ View", on_click=lambda: ui.notify("View details coming soon!")).classes(
                        "flex-1 px-4 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

                    ui.button("✏️ Edit", on_click=lambda: edit_advert(advert.get('id'))).classes(
                        "flex-1 px-4 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
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

                    ui.button("🗑️ Delete", on_click=do_delete).classes(
                        "flex-1 px-4 py-3 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

                # Created date (if available)
                if 'created_at' in advert:
                    with ui.element().classes("mt-4 pt-4 border-t border-gray-100"):
                        ui.label(f"Created: {advert['created_at']}").classes("text-xs text-gray-400")

    def create_advert_list_item(advert):
        """Create a modern, aesthetically pleasing list item for list view"""
        # Modern image URLs for food/restaurant themes
        food_images = [
            'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=250&fit=crop&auto=format&q=80',  # Pizza
            'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400&h=250&fit=crop&auto=format&q=80',  # Burger
            'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=250&fit=crop&auto=format&q=80',  # Pasta
            'https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=250&fit=crop&auto=format&q=80',  # Sushi
            'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400&h=250&fit=crop&auto=format&q=80',  # Steak
            'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=400&h=250&fit=crop&auto=format&q=80',  # Salad
            'https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=400&h=250&fit=crop&auto=format&q=80',  # Tacos
            'https://images.unsplash.com/photo-1574484284002-952d92456975?w=400&h=250&fit=crop&auto=format&q=80',  # Chicken
        ]

        # Use advert image if available, otherwise use a random food image
        image_url = advert.get('image')
        if not image_url or image_url.startswith('data:'):
            import random
            image_url = random.choice(food_images)

        # Get category color
        category = advert.get('category', 'General').lower()
        category_colors = {
            'pizza': 'bg-red-500',
            'burger': 'bg-yellow-500',
            'pasta': 'bg-orange-500',
            'sushi': 'bg-pink-500',
            'steak': 'bg-purple-500',
            'salad': 'bg-green-500',
            'tacos': 'bg-blue-500',
            'chicken': 'bg-indigo-500',
        }
        category_color = category_colors.get(category, 'bg-gray-500')

        with ui.card().classes("group w-full p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 bg-white rounded-2xl border-0 shadow-lg card-hover-effect"):
            with ui.row().classes("w-full items-center gap-6"):
                # Image section
                with ui.column().classes("w-32 h-32 rounded-xl overflow-hidden shadow-lg"):
                    ui.image(image_url).classes("w-full h-full object-cover transition-transform duration-300 group-hover:scale-110")

                # Content section
                with ui.column().classes("flex-1"):
                    # Header with title and badges
                    with ui.row().classes("w-full items-start justify-between mb-3"):
                        with ui.column().classes("flex-1"):
                            # Title
                            title = advert.get('name', 'No name')
                            ui.label(title).classes("text-xl font-bold text-gray-900 leading-tight mb-2")

                            # Category badge
                            with ui.element().classes(f"{category_color} text-white px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide inline-block"):
                                ui.label(category.title())

                        # Price badge
                        with ui.element().classes("bg-green-500 text-white px-4 py-2 rounded-full font-bold text-lg shadow-lg"):
                            ui.label(f"GH₵ {advert.get('price', 0)}")

                    # Description
                    description = advert.get('description', 'No description')
                    truncated_desc = description[:200] + "..." if len(description) > 200 else description
                    ui.label(truncated_desc).classes("text-gray-600 text-sm leading-relaxed mb-4")

                    # Rating and status row
                    with ui.row().classes("w-full items-center justify-between"):
                        # Rating stars
                        with ui.row().classes("gap-1 items-center"):
                            for i in range(5):
                                ui.icon("star", size="14px").classes("text-yellow-400")
                            ui.label("(4.5)").classes("text-gray-500 text-sm ml-2")

                        # Status indicator
                        status = advert.get('is_active', True)
                        status_color = "bg-green-500" if status else "bg-red-500"
                        with ui.element().classes(f"{status_color} text-white px-3 py-1 rounded-full text-xs font-semibold"):
                            ui.label("Active" if status else "Inactive")

                # Action buttons
                with ui.column().classes("items-end justify-center gap-3"):
                    ui.button("👁️ View", on_click=lambda: ui.notify("View details coming soon!")).classes(
                        "px-6 py-2 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-xl hover:from-blue-600 hover:to-blue-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

                    ui.button("✏️ Edit", on_click=lambda: edit_advert(advert.get('id'))).classes(
                        "px-6 py-2 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
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

                    ui.button("🗑️ Delete", on_click=do_delete).classes(
                        "px-6 py-2 bg-gradient-to-r from-red-500 to-red-600 text-white rounded-xl hover:from-red-600 hover:to-red-700 font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    )

    def edit_advert(advert_id):
        """Navigate to edit advert page"""
        ui.navigate.to(f'/vendor/edit_advert/{advert_id}')

    refresh_adverts()

def show_create_advert():
    """Show enhanced create advert form with modern UI"""
    if not require_vendor():
        return

    # Add custom CSS for enhanced form styling
    ui.add_head_html('''
    <style>
    .form-section {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

    .form-section:hover {
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
        transition: all 0.3s ease;
    }

    .image-preview {
        border: 2px dashed #d1d5db;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        background: #f9fafb;
        transition: all 0.3s ease;
    }

    .image-preview:hover {
        border-color: #10b981;
        background: #f0fdf4;
    }

    .image-preview.dragover {
        border-color: #10b981;
        background: #ecfdf5;
        transform: scale(1.02);
    }

    .category-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .price-input {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
    }

    .form-step {
        display: none;
    }

    .form-step.active {
        display: block;
    }

    .step-indicator {
        display: flex;
        justify-content: center;
        margin-bottom: 32px;
    }

    .step-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: #d1d5db;
        margin: 0 8px;
        transition: all 0.3s ease;
    }

    .step-dot.active {
        background: #10b981;
        transform: scale(1.3);
    }

    .step-dot.completed {
        background: #10b981;
    }
    </style>
    ''')

    ui.query(".nicegui-content").classes('m-0 p-0 gap-0')
    with ui.element('main').classes('w-full min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-100 p-8'):
        with ui.card().classes('w-full max-w-4xl mx-auto shadow-2xl bg-white rounded-3xl overflow-hidden'):
            # Header
            with ui.element().classes('bg-gradient-to-r from-green-600 to-emerald-600 text-white p-8'):
                with ui.row().classes('w-full items-center justify-between'):
                    with ui.column():
                        ui.label("🍳 Create New Advert").classes('text-3xl font-bold mb-2')
                        ui.label("Share your delicious offerings with customers").classes('text-green-100 text-lg')

                    # Step indicator
                    with ui.element().classes('step-indicator'):
                        ui.element().classes('step-dot active').props('id=step1-dot')
                        ui.element().classes('step-dot').props('id=step2-dot')
                        ui.element().classes('step-dot').props('id=step3-dot')

            # Form content
            with ui.column().classes('p-8 space-y-6'):

                # Step 1: Basic Information
                with ui.element().classes('form-step active').props('id=step1'):
                    with ui.element().classes('form-section'):
                        ui.label("📝 Basic Information").classes('text-xl font-bold text-gray-800 mb-6')

                        with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-6'):
                            # Title
                            with ui.column():
                                advert_title = ui.input(
                                    label="Advert Title *",
                                    placeholder="e.g., Delicious Jollof Rice Special"
                                ).classes('w-full').props('outlined dense')
                                ui.label("Choose a catchy, descriptive title").classes('text-sm text-gray-500 mt-1')

                            # Category
                            with ui.column():
                                categories = [
                                    'Rice Dishes', 'Local Cuisine', 'Continental', 'Fast Food',
                                    'Beverages', 'Desserts', 'Snacks', 'Grilled Items',
                                    'Soups & Stews', 'Vegetarian', 'Seafood', 'Other'
                                ]
                                advert_category = ui.select(
                                    categories,
                                    label="Category *",
                                    value=categories[0]
                                ).classes('w-full').props('outlined dense')
                                ui.label("Select the most appropriate category").classes('text-sm text-gray-500 mt-1')

                        # Description
                        with ui.column():
                            advert_description = ui.textarea(
                                label="Description *",
                                placeholder="Describe your dish, ingredients, preparation method, and why customers should try it..."
                            ).classes('w-full').props('outlined dense')
                            ui.label("Provide detailed information to attract customers").classes('text-sm text-gray-500 mt-1')

                # Step 2: Pricing & Image
                with ui.element().classes('form-step').props('id=step2'):
                    with ui.element().classes('form-section'):
                        ui.label("💰 Pricing & Visuals").classes('text-xl font-bold text-gray-800 mb-6')

                        with ui.grid().classes('grid-cols-1 lg:grid-cols-2 gap-8'):
                            # Pricing section
                            with ui.column():
                                ui.label("Price Information").classes('text-lg font-semibold mb-4')

                                with ui.row().classes('items-end gap-4'):
                                    with ui.column().classes('flex-1'):
                                        advert_price = ui.number(
                                            label="Price (GH₵) *",
                                            placeholder="0.00"
                                        ).classes('price-input').props('outlined dense prefix=GH₵')
                                        ui.label("Set a competitive price").classes('text-sm text-gray-500 mt-1')

                                    with ui.column():
                                        ui.label("Price Type").classes('text-sm font-medium text-gray-700 mb-2')
                                        price_type = ui.radio([
                                            'Fixed Price',
                                            'Price Range',
                                            'Starting From'
                                        ], value='Fixed Price').classes('gap-2').props('dense')

                                # Special offers
                                with ui.column():
                                    ui.label("Special Offers (Optional)").classes('text-sm font-medium text-gray-700 mb-3')
                                    special_offers = ui.textarea(
                                        placeholder="e.g., Buy 2 get 1 free, 20% discount on orders above GH₵50..."
                                    ).classes('w-full').props('outlined dense')
                                    ui.label("Add any special offers or discounts").classes('text-sm text-gray-500 mt-1')

                            # Image section
                            with ui.column():
                                ui.label("Food Image").classes('text-lg font-semibold mb-4')

                                # Image preview area
                                image_preview = ui.element().classes('image-preview w-full h-64 flex flex-col items-center justify-center cursor-pointer')
                                preview_image = ui.image().classes('max-w-full max-h-full object-contain').props('id=preview-image')

                                # Upload controls
                                with ui.row().classes('w-full justify-center gap-4 mt-4'):
                                    ui.upload(
                                        auto_upload=True,
                                        on_upload=lambda e: handle_image_upload(e, image_preview, preview_image)
                                    ).classes('px-6 py-3 bg-green-500 text-white rounded-xl hover:bg-green-600 transition-colors').props('color=green accept=image/*')

                                    ui.button("📷 Choose from Gallery", on_click=lambda: ui.notify("Gallery feature coming soon!")).classes(
                                        'px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition-colors'
                                    )

                                ui.label("Upload a high-quality image of your dish (JPG, PNG, max 5MB)").classes('text-sm text-gray-500 text-center mt-2')

                # Step 3: Review & Submit
                with ui.element().classes('form-step').props('id=step3'):
                    with ui.element().classes('form-section'):
                        ui.label("✅ Review & Submit").classes('text-xl font-bold text-gray-800 mb-6')

                        # Summary card
                        with ui.card().classes('bg-gray-50 p-6 rounded-xl mb-6'):
                            ui.label("📋 Summary").classes('text-lg font-semibold mb-4')

                            with ui.grid().classes('grid-cols-1 md:grid-cols-2 gap-4'):
                                summary_title = ui.label("Title: ").classes('text-gray-600')
                                summary_category = ui.label("Category: ").classes('text-gray-600')
                                summary_price = ui.label("Price: ").classes('text-gray-600')
                                summary_description = ui.label("Description: ").classes('text-gray-600')

                        # Terms and conditions
                        with ui.column():
                            ui.label("📜 Terms & Conditions").classes('text-lg font-semibold mb-3')

                            with ui.element().classes('bg-yellow-50 border border-yellow-200 rounded-lg p-4'):
                                with ui.column().classes('gap-2 text-sm text-gray-700'):
                                    ui.label("• I confirm that all information provided is accurate").classes()
                                    ui.label("• I have the rights to use the uploaded image").classes()
                                    ui.label("• I agree to follow the platform's advertising guidelines").classes()
                                    ui.label("• I understand that false advertising may result in account suspension").classes()

                            agree_terms = ui.checkbox("I agree to the terms and conditions").classes('mt-4').props('dense')

                        # Submit button
                        submit_btn = ui.button(
                            "🚀 Create Advert",
                            on_click=lambda: submit_advert()
                        ).classes(
                            'w-full py-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 mt-6'
                        ).props('disable')

    # Navigation buttons
    with ui.row().classes('w-full justify-between px-8 py-6 bg-gray-50 border-t'):
        prev_btn = ui.button("← Previous", on_click=lambda: navigate_step(-1)).classes(
            'px-8 py-3 bg-gray-500 text-white rounded-xl hover:bg-gray-600 transition-colors'
        ).props('disable')

        next_btn = ui.button("Next →", on_click=lambda: navigate_step(1)).classes(
            'px-8 py-3 bg-green-500 text-white rounded-xl hover:bg-green-600 transition-colors font-semibold'
        )

        cancel_btn = ui.button("Cancel", on_click=lambda: ui.navigate.to('/vendor/dashboard')).classes(
            'px-8 py-3 bg-red-500 text-white rounded-xl hover:bg-red-600 transition-colors'
        )

    # Add footer
    show_footer()

    # JavaScript for form functionality
    ui.run_javascript('''
    let currentStep = 1;
    const totalSteps = 3;

    function navigateStep(direction) {
        const prevBtn = document.querySelector('[disable=""]');
        const nextBtn = document.querySelector('.q-btn:has(+ .q-btn)');
        const submitBtn = document.querySelector('.q-btn:last-child');

        if (direction === 1 && currentStep < totalSteps) {
            currentStep++;
            updateStepDisplay();
        } else if (direction === -1 && currentStep > 1) {
            currentStep--;
            updateStepDisplay();
        }
    }

    function updateStepDisplay() {
        // Update step dots
        for (let i = 1; i <= totalSteps; i++) {
            const dot = document.getElementById(`step${i}-dot`);
            if (dot) {
                dot.classList.remove('active', 'completed');
                if (i < currentStep) {
                    dot.classList.add('completed');
                } else if (i === currentStep) {
                    dot.classList.add('active');
                }
            }
        }

        // Show/hide form steps
        const steps = document.querySelectorAll('.form-step');
        steps.forEach((step, index) => {
            if (index + 1 === currentStep) {
                step.style.display = 'block';
            } else {
                step.style.display = 'none';
            }
        });

        // Update navigation buttons
        const prevBtn = document.querySelector('.q-btn:first-child');
        const nextBtn = document.querySelector('.q-btn:nth-child(2)');

        if (prevBtn) {
            prevBtn.style.display = currentStep === 1 ? 'none' : 'block';
        }
        if (nextBtn) {
            nextBtn.style.display = currentStep === totalSteps ? 'none' : 'inline-flex';
        }
    }

    // Initialize
    updateStepDisplay();
    ''')

# Global variables for form data
form_data = {
    'title': '',
    'description': '',
    'price': 0,
    'category': '',
    'image': None,
    'special_offers': '',
    'price_type': 'Fixed Price',
    'agree_terms': False
}

def handle_image_upload(event, preview_element, image_element):
    """Handle image upload and preview"""
    global form_data

    # Update form data
    form_data['image'] = event.content

    # Show preview
    image_element.set_source(f"data:{event.type};base64,{event.content.decode()}")
    preview_element.classes('image-preview w-full h-64 bg-green-50 border-green-300')

    ui.notify("Image uploaded successfully!", type="positive")

def navigate_step(direction):
    """Navigate between form steps"""
    # This will be handled by JavaScript
    pass

def submit_advert():
    """Submit the advert form"""
    global form_data

    # Validate form
    if not all([
        form_data['title'],
        form_data['description'],
        form_data['price'] > 0,
        form_data['category'],
        form_data['agree_terms']
    ]):
        ui.notify("Please fill in all required fields and agree to terms!", type="negative")
        return

    # Show loading state
    submit_btn = ui.element().props('id=submit-btn')
    if submit_btn:
        submit_btn.props('loading')

    try:
        # Try remote API first
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        data = {
            "name": form_data['title'],
            "description": form_data['description'],
            "price": form_data['price'],
            "category": form_data['category']
        }
        files = {"image": form_data['image']} if form_data['image'] else {}

        response = requests.post(url=f"{base_url}/food", data=data, files=files, headers=headers, timeout=15)
        if response.status_code == 200:
            ui.notify("🎉 Advert created successfully!", type="positive")
            ui.navigate.to('/vendor/dashboard')
            return

    except Exception as e:
        # Fallback to local storage
        try:
            vendor_id = get_user_id()
            if not vendor_id:
                ui.notify("Authentication error. Please log in again.", type="negative")
                return

            image_data = form_data['image'].decode() if form_data['image'] else ''

            create_advert(
                name=form_data['title'],
                description=form_data['description'],
                price=float(form_data['price']),
                owner_id=vendor_id,
                image=image_data
            )
            ui.notify("🎉 Advert created successfully (local)!", type="positive")
            ui.navigate.to('/vendor/dashboard')
            return
        except Exception as local_e:
            ui.notify(f"Failed to create advert: {local_e}", type="negative")
            return

    ui.notify("Failed to create advert. Please try again.", type="negative")

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
