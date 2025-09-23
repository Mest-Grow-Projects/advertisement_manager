from nicegui import ui
from components.side_bar import show_side_bar

@ui.page("/vendor/dashboard")
def show_vendor_dashboard():
   with ui.row().classes("w-full"):
      with ui.column().classes("w-[20%]"):
         show_side_bar()
      with ui.column().classes("w-[80%]"):
        ui.label("Dashboard Content goes here")
