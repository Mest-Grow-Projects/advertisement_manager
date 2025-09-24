from nicegui import ui
from vendor import show_vendor_dashboard

@ui.page("/vendor/dashboard")
def vendor_dashboard():
    """Vendor dashboard page"""
    show_vendor_dashboard()
