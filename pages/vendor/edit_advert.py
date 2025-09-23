from nicegui import ui
from components.side_bar import show_side_bar
from utils.api import base_url

@ui.page("/edit_advert")
def show_edit_advert_page():
    
    # --- Fullscreen background wrapper ---
    with ui.element("div").style(
        "background-image: url('/assets/edit.jpg');"
        "background-size: cover;"
        "background-position: center;"
        "width: 100vw;"
        "height: 100vh;"
        "display: flex;"
        "justify-content: center;"
        "align-items: center;"
        "margin: 0;"
        "padding: 0;"
    ):
       with ui.row().classes("w-full"):
           with ui.column().classes("w-[20%]"):
               show_side_bar()
       with ui.column().classes("w-[80%]"):
           ui.label("Dashboard Content goes here")
           #  Edit Advert Card
           with ui.card().classes('w-[600px] p-6 shadow-lg rounded-2xl bg-white/95 backdrop-blur'):
               ui.label('EDIT ADVERT').classes('text-2xl font-bold text-center mb-6 tracking-wide')

               # Input fields
               Title = ui.input('Title').props('outlined dense').classes('w-full mb-4')
               Description = ui.textarea('Item Description').props('outlined dense auto-grow').classes('w-full mb-4')
               Price = ui.number('Price (USD)').props('outlined dense').classes('w-full mb-4')
               Image = ui.select(
                   ['Keep current image', 'Upload new image from camera roll', 'Browse']
               ).props('outlined dense').classes('w-full mb-6')

               # Submit handler
               def submit():
                   if not Title.value or not Description.value or not Price.value:
                       ui.notify('⚠️ Please fill in all required fields', type='warning')
                       return
                   ui.notify(f'✅ Advert Updated: {Title.value}', type='positive')

               # Buttons row
               with ui.row().classes('justify-between mt-4'):
                   ui.button('Cancel', on_click=lambda: ui.notify('Edit cancelled')).classes(
                       'bg-gray-300 text-black w-[45%] py-2 rounded-xl hover:bg-gray-400'
                   )
                   ui.button('Save Changes', on_click=submit).classes(
                       'bg-black text-white w-[45%] py-2 rounded-xl hover:bg-gray-800'
                   )
