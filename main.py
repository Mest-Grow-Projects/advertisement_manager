from nicegui import ui
from components.header import show_header
from pages.home import show_home_page
from pages.add_event import show_add_event_page
from pages.view_event import show_view_event_page
from pages.edit_event import show_edit_event_page


@ui.page("/")
def home_page():
    show_header()
    show_home_page

@ui.page("/add_event")
def add_event_page():
    show_header()
    show_add_event_page()

@ui.page("/edit_event")
def edit_event_page():
    show_header
    show_edit_event_page

@ui.page("/view_event")
def view_event_page():
    show_header()
    show_view_event_page

    



ui.run()