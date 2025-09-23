from nicegui import ui

def show_header():
    # --- Fixed header ---
    with ui.row().classes(
        'w-full items-center justify-between px-8 py-4 shadow-md bg-white '
        'fixed top-0 left-0 z-50'
    ):
        # Logo
        ui.label('🍔 BiteBridge').classes('text-3xl font-bold text-red-600')

        # Desktop navigation
        with ui.row().classes('md:flex gap-8 text-lg font-medium'):
            for name, link in [
                ('Home', '/'),
                ('Restaurants', '/view_advert'),
                ('Add', '/vendor/add_advert'),
                ('Edit', '/edit_advert'),
                ('Sign-in', '/sign-in')
            ]:
                ui.link(name, link).classes(
                    'text-gray-700 hover:text-red-500 no-underline transition-colors duration-300'
                )

        # Mobile menu toggle
        ui.button('☰', on_click=lambda: ui.notify('Mobile menu coming soon')).classes(
            'md:hidden text-gray-700 text-2xl px-2'
        )

    # --- Spacer to prevent content hiding under header ---
    ui.space().classes("h-20")
