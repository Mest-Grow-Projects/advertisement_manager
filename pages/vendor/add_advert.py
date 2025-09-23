from nicegui import ui
from components.side_bar import show_side_bar
import requests
from utils.api import base_url

def add_advert(data):
    responds = requests.post(f"{base_url}/food", data)
    print(responds.json())

@ui.page("/vendor/add_advert")
def show_add_advert_page():
    image_content = None

    def handle_image_upload(e):
        nonlocal image_content
        image_content = e.content

    with ui.row().classes("w-full"):
      with ui.column().classes("w-[20%]"):
         show_side_bar()
    with ui.column().classes("w-[80%]"):
        # Fullscreen background with flex centering
        with ui.element("div").style(
            "background-image: url('/assets/add.jpg');"
            "background-size: cover;"
            "background-position: center;"
            "width: 100vw;"
            "height: 100vh;"
            "display: flex;"
            "justify-content: center;"
            "align-items: center;"
        ):
            # Form card
            with ui.card().classes(
                'w-[600px] max-w-[90%] p-8 shadow-2xl rounded-2xl bg-white/95 backdrop-blur-lg'
            ):
                ui.label('CREATE A NEW ADVERT').classes(
                    'text-3xl font-extrabold text-center mb-2 text-green-700'
                )
                ui.label('Fill in the details below to post your advert').classes(
                    'text-base text-center text-gray-600 mb-6'
                )

                # Input fields
                Title = ui.input('Title').props('outlined dense').classes('w-full mb-4')
                Description = ui.textarea('Item Description').props(
                    'outlined dense auto-grow'
                ).classes('w-full mb-4')
                Price = ui.number('Price (Ghc)').props('outlined dense').classes('w-full mb-4')
                flyer =ui.upload().props("flat bordered").classes("w-full").style("border: 2px dashed #ccc; padding:20px:")

                # Submit user description
                def submit():
                    if not Title.value or not Description.value or not Price.value:
                        ui.notify('⚠️ Please fill in all fields', type='warning')
                        return
                    ui.notify(f'✅ Advert Created: {Title.value}', type='positive')

                # Action buttons
                with ui.row().classes('w-full justify-between mt-4'):
                    ui.button('Cancel', on_click=lambda: ui.notify('Cancelled')).classes(
                        'bg-gray-300 text-black w-[48%] py-2 rounded-xl hover:bg-gray-400'
                    )
                    ui.button('Submit Advert', on_click=submit).classes(
                        'bg-green-600 text-white w-[48%] py-2 rounded-xl hover:bg-green-700'
                    )

            #"image": image_content