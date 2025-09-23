from nicegui import ui, app
from components.header import show_header
from pages.home import show_home_page
from pages.view_advert import show_view_advert_page
from pages.vendor.edit_advert import show_edit_advert_page
from pages.vendor.dashboard import *
from pages.vendor.add_advert import*
from pages.vendor.edit_advert import*
from pages.vendor.events import*




# Expose the assets folder
app.add_static_files("/assets", "assets")


@ui.page("/")
def home_page():
    show_header()
    show_home_page()




@ui.page("/view_advert")
def view_advert_page():
    show_header()
    show_view_advert_page()

    
ui.run()