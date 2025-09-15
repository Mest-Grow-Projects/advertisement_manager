from nicegui import ui

def show_home_page():
    # Load Google Fonts 
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;800&display=swap" rel="stylesheet">
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow-x: hidden;
            }
            .hero-section {
                min-height: 100vh;   /* full height */
                width: 100vw;        /* full width */
                background-size: cover;
                background-position: center;
                position: relative;
                margin: 0;
                padding: 0;
            }
            .hero-overlay {
                position: absolute;
                inset: 0;
                background: rgba(0, 0, 0, 0.6);
            }
        </style>
    ''')

    # Fullscreen background section
    with ui.element("div").classes(
        "hero-section flex flex-col items-center justify-center text-center"
    ).style("background-image: url('/assets/dishes-mediterranean-cuisine.jpg');"):

        # Dark overlay
        ui.element("div").classes("hero-overlay")

        # Content
        with ui.column().classes("relative z-10 max-w-3xl px-6 items-center"):
            ui.label("Welcome to BiteBridge").classes(
                "hero-title text-5xl md:text-6xl font-extrabold text-white mb-4 drop-shadow-xl tracking-wide"
            )

            ui.label("Bridging the gap between you and your next meal!").classes(
                "hero-subtitle text-lg md:text-2xl text-gray-200 mb-8 italic drop-shadow-sm"
            )

            