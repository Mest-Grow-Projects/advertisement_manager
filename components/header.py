from nicegui import ui 

def show_header():
    with ui.row():
        ui.link("Home", "/")
        ui.link("Add event", "/")
        ui.link("Add event", "/add_event")
        ui.link("Edit event", "/edit_event")
        ui.link("View event", "/view_event")

