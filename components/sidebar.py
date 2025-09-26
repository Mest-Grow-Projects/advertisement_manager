from nicegui import ui

def show_side_bar():
    """Vendor sidebar component"""
    
    def handle_logout():
        """Handle logout directly and redirect to home page"""
        try:
            # Clear authentication tokens from storage
            ui.run_javascript("localStorage.removeItem('auth_token');")
            ui.run_javascript("localStorage.removeItem('user_id');")
            ui.run_javascript("localStorage.removeItem('user_role');")
            ui.run_javascript("sessionStorage.removeItem('auth_token');")
            ui.run_javascript("sessionStorage.removeItem('user_id');")
            ui.run_javascript("sessionStorage.removeItem('user_role');")
        except Exception as e:
            print(f"Error clearing storage: {e}")
        
        # Show logout notification
        ui.notify('Successfully logged out', type='positive')
        
        # Redirect to home page immediately
        ui.navigate.to('/')
    
    with ui.column().classes("p-8 h-full relative bg-gradient-to-b from-emerald-900 to-green-900"):
        # Profile Section
        with ui.column().classes("items-center mb-8 pb-8 border-b border-emerald-700"):
            # Profile Avatar
            with ui.element('div').classes("w-20 h-20 mb-4 bg-gradient-to-br from-emerald-400 to-green-500 rounded-full flex items-center justify-center shadow-lg"):
                ui.icon('restaurant', size='xl', color='white')
            
            ui.label("Vendor Account").classes("text-white text-lg font-semibold mb-1")
            ui.label("Restaurant Owner").classes("text-emerald-300 text-sm")
        
        # Navigation Menu
        with ui.column().classes("space-y-2 flex-1"):
            menu_items = [
                ("dashboard", "Dashboard", "/vendor/dashboard"),
                ("add", "Add Advert", "/vendor/add_advert"),
                ("explore", "Browse Advertisements", "/advertisements"),
                ("visibility", "View Adverts", "/view_advert"),
                ("home", "Home", "/")
            ]
            
            for icon, text, link in menu_items:
                is_active = link == "/vendor/dashboard"  # Simple active check
                
                # Determine classes based on active state
                if is_active:
                    link_classes = "w-full no-underline transition-all duration-300 transform -translate-x-2"
                    row_classes = "w-full items-center px-4 py-3 rounded-xl transition-all duration-300 bg-emerald-600 shadow-lg border-l-4 border-emerald-400"
                else:
                    link_classes = "w-full no-underline transition-all duration-300"
                    row_classes = "w-full items-center px-4 py-3 rounded-xl transition-all duration-300 bg-emerald-800 bg-opacity-50 hover:bg-emerald-700 hover:bg-opacity-70 hover:transform hover:-translate-y-0.5"
                
                with ui.link(link).classes(link_classes):
                    with ui.row().classes(row_classes):
                        ui.icon(icon, color='white').classes("text-xl mr-3")
                        ui.label(text).classes("text-white font-medium")
                        
                        if is_active:
                            ui.icon('chevron_right', color='white').classes("ml-auto")
        
        # Bottom Section
        with ui.column().classes("pt-8 border-t border-emerald-700"):
            # Quick Stats Mini
            with ui.column().classes("space-y-3 mb-6"):
                ui.label("Quick Stats").classes("text-emerald-300 text-sm font-semibold uppercase tracking-wide")
                
                with ui.row().classes("items-center justify-between"):
                    ui.label("Active Ads").classes("text-emerald-200 text-sm")
                    ui.label("0").classes("text-white font-bold")
                
                with ui.row().classes("items-center justify-between"):
                    ui.label("Total Views").classes("text-emerald-200 text-sm")
                    ui.label("0").classes("text-white font-bold")
            
            # Logout Button - Now redirects to home page
            with ui.row().classes("w-full"):
                ui.button("🚪 Logout", on_click=handle_logout, icon='logout').classes(
                    "w-full bg-emerald-700 hover:bg-emerald-600 text-white py-3 rounded-xl font-semibold transition-all"
                )
        
        # Decorative Elements
        with ui.element('div').classes("absolute bottom-0 left-0 w-full h-2 bg-gradient-to-r from-emerald-400 to-green-500"):
            pass