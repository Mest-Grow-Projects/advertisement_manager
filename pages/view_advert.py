from nicegui import ui

def show_view_advert_page():
    ui.label("Browse Restaurants").classes("text-2xl font-bold mb-4 text-center mx-10")

    # --- Data for restaurants ---
    restaurants = [
        {"name": "Food Haven", "desc": "Description of project 1", "img": "https://cdn.pixabay.com/photo/2017/03/26/11/53/hors-doeuvre-2175326_640.jpg"},
        {"name": "Food Master", "desc": "Description of project 2", "img": "https://cdn.pixabay.com/photo/2017/03/10/13/57/cooking-2132874_1280.jpg"},
        {"name": "Hungry Bugs", "desc": "Description of project 3", "img": "https://cdn.pixabay.com/photo/2017/05/07/08/56/pancakes-2291908_640.jpg"},
        {"name": "FryFry", "desc": "Description of project 4", "img": "https://cdn.pixabay.com/photo/2014/10/19/20/59/hamburger-494706_640.jpg"},
        {"name": "Pizza&Pizza", "desc": "Description of project 5", "img": "https://cdn.pixabay.com/photo/2017/02/15/10/57/pizza-2068272_640.jpg"},
    ]

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
            if query in r["name"].lower() or query in r["desc"].lower():
                with results_container:
                    with ui.card().classes("w-60 shadow-md hover:shadow-lg transition p-3"):
                        ui.image(r["img"]).classes("rounded-lg")
                        ui.label(r["name"]).classes("text-lg font-semibold mt-2")
                        ui.label(r["desc"]).classes("text-sm text-gray-600 mb-2")
                        ui.button("View", on_click=lambda name=r["name"]: ui.notify(f"Viewing {name}")).classes(
                            "w-full bg-green-600 text-white rounded-lg hover:bg-green-700"
                        )

    # First render
    render_cards()

    # Update on input
    search_box.on('input', lambda e: render_cards())
