from nicegui import ui
import requests
from utils.api import base_url

def show_view_advert_page():
    response = requests.get(f"{base_url}/food/all")
    json_data = response.json()

    ui.label("Browse Restaurants").classes("text-2xl font-bold mb-4 text-center mx-10")

    # --- Data for restaurants ---
    restaurants = json_data["data"]

    # --- Search input ---
    search_box = ui.input(placeholder="Search restaurants...").props("outlined dense clearable").classes(
        "w-1/2 mx-auto mb-6"
    )

    # --- Container for results ---
    results_container = ui.row().classes("justify-center gap-10 flex-wrap")

    def render_cards():
        results_container.clear()
        query = (search_box.value or "").lower()
        for r in restaurants:
            if query in r["name"].lower() or query in r["description"].lower():
                with results_container:
                    with ui.card().classes("w-60 shadow-md hover:shadow-lg transition p-3"):
                        ui.image(r["image"]).classes("rounded-lg")
                        ui.label(r["name"]).classes("text-lg font-semibold mt-2")
                        ui.label(r["description"]).classes("text-sm text-gray-600 mb-2")
                        ui.button("View", on_click=lambda name=r["name"]: ui.notify(f"Viewing {name}")).classes(
                            "w-full bg-green-600 text-white rounded-lg hover:bg-green-700"
                        )

    # First render
    render_cards()

    # Update on input
    search_box.on('input', lambda e: render_cards())
