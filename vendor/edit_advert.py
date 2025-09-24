from nicegui import ui
from vendor import show_edit_advert

@ui.page("/vendor/edit_advert/{advert_id}")
def vendor_edit_advert(advert_id: str):
    """Vendor edit advert page"""
    show_edit_advert(advert_id)
