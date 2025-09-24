from nicegui import ui, app
import requests
from utils.auth import require_vendor, get_user_id, get_token
from utils.frontend_store import create_advert
from utils.api import base_url
from components.footer import show_footer

# Global variable for image
_advert_image = None

def _handle_image_upload(event):
    """Handle image upload for advert"""
    global _advert_image
    _advert_image = event.content

def _post_advert(data, files):
    """Post advert to API with enhanced error handling"""
    try:
        # Validate required fields
        if not all([data.get('name'), data.get('description'), data.get('price'), data.get('category')]):
            ui.notify("❌ Please fill in all required fields (title, description, price, category)", type="negative")
            return

        # Try remote API first
        token = get_token()
        user_id = get_user_id()

        if not user_id:
            ui.notify("❌ Authentication error. Please log in again.", type="negative")
            ui.navigate.to('/sign-in')
            return

        headers = {"Authorization": f"Bearer {token}"} if token else {}

        # Prepare data for API
        api_data = {
            "name": str(data['name']).strip(),
            "description": str(data['description']).strip(),
            "price": float(data['price']),
            "category": str(data['category']).strip()
        }

        print(f"🔍 DEBUG: Attempting API call to {base_url}/food")
        print(f"🔍 DEBUG: Data: {api_data}")
        print(f"🔍 DEBUG: Files: {bool(files)}")
        print(f"🔍 DEBUG: Token: {bool(token)}")

        response = requests.post(url=f"{base_url}/food", data=api_data, files=files, headers=headers, timeout=15)

        print(f"🔍 DEBUG: API Response Status: {response.status_code}")
        print(f"🔍 DEBUG: API Response: {response.text}")

        if response.status_code == 200:
            ui.notify("🎉 Advert created successfully!", type="positive")
            ui.navigate.to('/vendor/adverts')
            return
        else:
            print(f"❌ API Error: Status {response.status_code}, Response: {response.text}")
            ui.notify(f"⚠️ API Error ({response.status_code}). Using local storage...", type="warning")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error: {e}")
        ui.notify("🌐 Network error. Using local storage...", type="warning")
    except ValueError as e:
        print(f"❌ Data Error: {e}")
        ui.notify(f"❌ Invalid data format: {e}", type="negative")
        return
    except Exception as e:
        print(f"❌ API Error: {e}")
        ui.notify("⚠️ API error. Using local storage...", type="warning")

    # Fallback to local storage
    try:
        print("🔄 Attempting local storage fallback...")

        vendor_id = get_user_id()
        if not vendor_id:
            ui.notify("❌ Authentication error. Please log in again.", type="negative")
            ui.navigate.to('/sign-in')
            return

        image_data = _advert_image.decode() if _advert_image else ''

        print(f"🔍 DEBUG: Creating local advert for user {vendor_id}")
        print(f"🔍 DEBUG: Advert data: {data}")

        new_advert = create_advert(
            name=str(data['name']).strip(),
            description=str(data['description']).strip(),
            price=float(data['price']),
            owner_id=vendor_id,
            image=image_data
        )

        print(f"✅ Local advert created successfully: {new_advert['id']}")
        ui.notify("🎉 Advert created successfully (local)!", type="positive")
        ui.navigate.to('/vendor/adverts')
        return

    except Exception as local_e:
        print(f"❌ Local Storage Error: {local_e}")
        ui.notify(f"❌ Failed to create advert: {str(local_e)}", type="negative")
        return

def _validate_and_submit():
    """Validate form data and submit advert"""
    try:
        # Get form values
        title = advert_title.value or ""
        description = advert_description.value or ""
        price = advert_price.value or 0
        category = advert_category.value or ""

        # Validate required fields
        errors = []

        if not title.strip():
            errors.append("Advert title is required")
        elif len(title.strip()) < 3:
            errors.append("Advert title must be at least 3 characters")

        if not description.strip():
            errors.append("Description is required")
        elif len(description.strip()) < 10:
            errors.append("Description must be at least 10 characters")

        if not price or price <= 0:
            errors.append("Price must be greater than 0")
        elif price > 10000:
            errors.append("Price cannot exceed GH₵10,000")

        if not category:
            errors.append("Please select a category")

        if errors:
            ui.notify(f"❌ Please fix the following errors:\n• {'\n• '.join(errors)}", type="negative")
            return

        # Prepare data for submission
        data = {
            "name": title.strip(),
            "description": description.strip(),
            "price": price,
            "category": category
        }

        files = {"image": _advert_image} if _advert_image else {}

        # Submit the advert
        _post_advert(data, files)

    except Exception as e:
        print(f"❌ Validation Error: {e}")
        ui.notify(f"❌ Form validation error: {str(e)}", type="negative")

@ui.page("/vendor/create_advert")
def show_create_advert_page():
    """Modern create advert page based on sample structure"""
    if not require_vendor():
        return

    with ui.element("main").classes("relative w-full max-w-[1440px] mx-auto min-h-[1563px] bg-[#F8F8FA] rounded-[20px] pb-12"):

        # Hero Section
        with ui.element("section").classes("absolute left-[312px] right-[312px] top-[50px] flex flex-col items-center gap-[33px] w-[816px]"):
            ui.label(" Create Your Perfect Advert").classes("text-[36px] font-bold leading-[42px] text-center text-black w-full")
            ui.label("Showcase your culinary masterpieces with style").classes("text-[18px] text-gray-600 text-center w-full")

        # Form Section
        with ui.element("section").classes("absolute left-[312px] right-[312px] top-[189px] flex flex-col items-center gap-[33px] w-[816px]"):
            ui.label("Advert Details").classes("text-[36px] font-bold leading-[42px] text-center text-black w-full")

            # Advert Title
            with ui.element("div").classes("w-full relative"):
                ui.label("Advert Title").classes("absolute left-0 top-[-25px] text-[12px] text-black font-roboto")
                global advert_title
                advert_title = ui.input(placeholder="Enter advert title").classes("w-full h-[46px] bg-white rounded-[5px] px-4 py-2 text-[12px] text-[#687C94] font-roboto border-none outline-none")

            # Price
            with ui.element("div").classes("w-full relative mt-6"):
                ui.label("Price (GH₵)").classes("absolute left-0 top-[-25px] text-[12px] text-black font-roboto")
                global advert_price
                advert_price = ui.number(placeholder="0.00").classes("w-full h-[46px] bg-white rounded-[5px] px-4 py-2 text-[12px] text-[#687C94] font-roboto border-none outline-none").props("prefix=GH₵")

            # Category Selection
            with ui.element("div").classes("w-full relative mt-6"):
                ui.label("Category").classes("absolute left-0 top-[-25px] text-[12px] text-black font-roboto")
                categories = [
                    'Rice Dishes', 'Local Cuisine', 'Continental', 'Fast Food',
                    'Beverages', 'Desserts', 'Snacks', 'Grilled Items',
                    'Soups & Stews', 'Vegetarian', 'Seafood', 'Other'
                ]
                global advert_category
                advert_category = ui.select(categories, value=categories[0]).classes("w-full h-[46px] bg-white rounded-[5px] px-4 py-2 text-[12px] text-[#687C94] font-roboto border-none outline-none")

        # Description & Image Section
        with ui.element("section").classes("absolute left-[314px] right-[313px] top-[500px] flex flex-col items-center gap-[40px] w-[813px]"):
            ui.label("Description & Visual").classes("text-[36px] font-bold leading-[42px] text-center text-black w-full")

            # Advert Image Upload
            with ui.element("div").classes("w-full flex flex-col items-start gap-2"):
                ui.label("Food Image").classes("text-[12px] text-black font-roboto")
                ui.upload(label="Select food image", auto_upload=True, on_upload=_handle_image_upload).classes("w-full")

            # Advert Description
            with ui.element("div").classes("w-full flex flex-col items-start gap-2 mt-4"):
                ui.label("Description").classes("text-[12px] text-black font-roboto")
                global advert_description
                advert_description = ui.textarea(placeholder="Describe your dish, ingredients, preparation method, and why customers should try it...").classes("w-full h-[173px] bg-white rounded-[5px] px-4 py-2 text-[12px] text-[#687C94] font-roboto border-none outline-none")

            # Submit Button
            ui.button("Create Advert", on_click=lambda: _validate_and_submit()).classes("w-full sm:w-full md:w-full lg:w-full xl:w-full h-[49px] sm:h-[49px] md:h-[56px] lg:h-[56px] xl:h-[56px] bg-gradient-to-r from-[#10b981] to-[#059669] text-white text-[14px] sm:text-[14px] md:text-[16px] lg:text-[16px] xl:text-[16px] font-roboto rounded-[5px] mt-8 hover:from-[#059669] hover:to-[#047857] transition-all duration-300 shadow-lg hover:shadow-xl")

    # Add footer
    show_footer()