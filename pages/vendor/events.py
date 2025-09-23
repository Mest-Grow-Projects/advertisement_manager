from nicegui import ui
from components.side_bar import show_side_bar
from utils.auth import require_vendor

@ui.page("/vendor/events")
def show_vendor_events():
    if not require_vendor():
        return
    with ui.row().classes("w-full"):
        with ui.column().classes("w-[20%]"):
            show_side_bar()
        with ui.column().classes("w-[80%]"):
            ui.label("Vendor events goes here")

