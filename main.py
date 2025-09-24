import os
import secrets
from nicegui import ui, app

# === Import shared components ===
from components.header import show_header

# === Import pages to register routes (via @ui.page) ===
from pages import home, view_advert
import pages.signin                 # /sign-in
import pages.vendor.dashboard       # /vendor/dashboard
import pages.vendor.add_advert      # /vendor/add_advert
import pages.vendor.edit_advert     # /vendor/edit_advert/{advert_id}
import pages.vendor.events          # /vendor/events

# Import new vendor pages
import vendor.dashboard             # /vendor/dashboard (new)
import vendor.create_advert         # /vendor/create_advert (new)
import vendor.adverts               # /vendor/adverts (new)
import vendor.edit_advert           # /vendor/edit_advert/{advert_id} (new)
import vendor.analytics             # /vendor/analytics (new)
import vendor.settings              # /vendor/settings (new)
import vendor                       # Import vendor module for sidebar functionality
import vendor.sidebar               # New sidebar component


# === Expose static assets (images, CSS, etc.) ===
app.add_static_files("/assets", "assets")


# === ROUTES ===
@ui.page("/")
def home_page() -> None:
    """Home page route."""
    show_header()
    home.show_home_page()


@ui.page("/view_advert")
def view_advert_page() -> None:
    """View adverts page route."""
    show_header()
    view_advert.show_view_advert_page()


# === START APP ===
if __name__ in {"__main__", "__mp_main__"}:
    # === STORAGE SECRET CONFIG ===
    # Use environment variable if set, otherwise generate a secure fallback
    STORAGE_SECRET = os.getenv("STORAGE_SECRET") or secrets.token_urlsafe(32)
    ui.run(storage_secret=STORAGE_SECRET)
