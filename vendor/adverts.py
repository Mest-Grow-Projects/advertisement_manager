from nicegui import ui
from vendor import show_vendor_adverts_list

@ui.page("/vendor/adverts")
def vendor_adverts():
    """Vendor adverts list page"""
    show_vendor_adverts_list()
