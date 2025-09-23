from nicegui import ui

def show_footer():
    """Modern compact footer component for BiteBridge"""
    with ui.element("div").classes("w-full py-8 px-6 bg-gray-900 text-white"):
        with ui.column().classes("w-full max-w-5xl mx-auto"):
            with ui.row().classes("w-full justify-between items-start flex-wrap gap-8"):
                with ui.column().classes("max-w-xs"):
                    ui.label("BiteBridge").classes("text-2xl font-bold text-green-400 mb-3")
                    ui.label("Discover amazing restaurants and delicious food in your area.").classes("text-gray-400 leading-relaxed text-sm")
                
                with ui.column():
                    ui.label("Quick Links").classes("text-lg font-semibold mb-3 text-white")
                    ui.link("Home", "/").classes("text-gray-400 hover:text-green-400 block mb-2 text-sm transition-colors")
                    ui.link("Restaurants", "/view_advert").classes("text-gray-400 hover:text-green-400 block mb-2 text-sm transition-colors")
                    ui.link("Sign In", "/sign-in").classes("text-gray-400 hover:text-green-400 block text-sm transition-colors")
                
                with ui.column():
                    ui.label("Contact").classes("text-lg font-semibold mb-3 text-white")
                    ui.label("hello@bitebridge.com").classes("text-gray-400 block mb-2 text-sm")
                    ui.label("+1 (555) 123-4567").classes("text-gray-400 block mb-2 text-sm")
                    ui.label("San Francisco, CA").classes("text-gray-400 block text-sm")
            
            ui.separator().classes("my-6 border-gray-700")
            with ui.row().classes("w-full justify-between items-center flex-wrap gap-4"):
                ui.label("© 2024 BiteBridge. All rights reserved.").classes("text-gray-500 text-sm")
                with ui.row().classes("gap-4"):
                    ui.label("Privacy Policy").classes("text-gray-500 hover:text-green-400 cursor-pointer text-sm transition-colors")
                    ui.label("Terms of Service").classes("text-gray-500 hover:text-green-400 cursor-pointer text-sm transition-colors")
                    ui.label("Support").classes("text-gray-500 hover:text-green-400 cursor-pointer text-sm transition-colors")
