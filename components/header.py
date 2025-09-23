from nicegui import ui
from utils.auth import get_role, clear_session

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
            role = get_role()
            ui.link('Home', '/').classes('text-gray-700 hover:text-red-500 no-underline transition-colors duration-300')
            ui.link('Restaurants', '/view_advert').classes('text-gray-700 hover:text-red-500 no-underline transition-colors duration-300')
            if role == 'vendor':
                ui.link('Vendor Dashboard', '/vendor/dashboard').classes('text-gray-700 hover:text-red-500 no-underline transition-colors duration-300')
                ui.link('Add', '/vendor/add_advert').classes('text-gray-700 hover:text-red-500 no-underline transition-colors duration-300')
                ui.button('Logout', on_click=lambda: (clear_session(), ui.navigate.to('/'))).classes('q-btn--flat text-red-600')
            elif role == 'user':
                ui.button('Logout', on_click=lambda: (clear_session(), ui.navigate.to('/'))).classes('q-btn--flat text-red-600')
            else:
                ui.link('Sign-in', '/sign-in').classes('text-gray-700 hover:text-red-500 no-underline transition-colors duration-300')

        # Mobile menu toggle
        ui.button('☰', on_click=lambda: ui.notify('Mobile menu coming soon')).classes(
            'md:hidden text-gray-700 text-2xl px-2'
        )

    # --- Spacer to prevent content hiding under header ---
    ui.space().classes("h-20")
