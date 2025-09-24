from nicegui import ui
from vendor import show_vendor_sidebar
from components.footer import show_footer

@ui.page("/vendor/settings")
def vendor_settings():
    """Vendor settings page"""
    from utils.auth import require_vendor
    if not require_vendor():
        return

    with ui.row().classes("w-full min-h-screen bg-gray-50"):
        # Sidebar
        with ui.column().classes("w-[20%] bg-white shadow-lg min-h-screen"):
            show_vendor_sidebar()

        # Main content area
        with ui.column().classes("w-[80%] p-6"):
            ui.label("Settings").classes("text-3xl font-bold text-gray-900 mb-8")
            ui.label("Settings feature coming soon!").classes("text-xl text-gray-600")

    show_footer()
