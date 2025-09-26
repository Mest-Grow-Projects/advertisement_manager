from nicegui import ui
from components.sidebar import show_side_bar
from utils.auth import require_vendor, get_user_id, get_token
from utils.api import base_url
import requests
import base64

@ui.page("/vendor/edit_advert/{advert_id}")
def show_edit_advert_page(advert_id: str):
    if not require_vendor():
        return
    
    # State for image handling
    image_content = None
    image_preview_url = None
    current_image_url = None

    def handle_image_upload(e):
        nonlocal image_content, image_preview_url
        image_content = e.content
        image_preview_url = f"data:image/jpeg;base64,{base64.b64encode(e.content).decode()}"
        ui.notify('✅ New image uploaded successfully!', type='positive')

    def clear_image():
        nonlocal image_content, image_preview_url
        image_content = None
        image_preview_url = None
        ui.notify('🗑️ New image removed', type='info')

    # Load advert data
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    advert = None
    
    try:
        # Use your actual base URL
        response = requests.get(f"https://advertisement-platform-server-2zhr.onrender.com/api/food/{advert_id}", headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # Adjust based on your API response structure
            advert = data.get('data') or data
            if advert and advert.get('image'):
                current_image_url = advert.get('image')
        else:
            ui.notify(f'Failed to load advert: {response.status_code}', type='negative')
            ui.navigate.to('/vendor/dashboard')
            return
            
    except requests.exceptions.Timeout:
        ui.notify('Request timeout. Please try again.', type='negative')
        ui.navigate.to('/vendor/dashboard')
        return
    except requests.exceptions.ConnectionError:
        ui.notify('Connection error. Please check your internet.', type='negative')
        ui.navigate.to('/vendor/dashboard')
        return
    except Exception as e:
        ui.notify(f'Error loading advert: {str(e)}', type='negative')
        ui.navigate.to('/vendor/dashboard')
        return

    # Ownership check
    current_user = get_user_id()
    if advert:
        owner_id = advert.get('owner_id') or advert.get('vendor_id')
        if current_user and owner_id and str(owner_id) != str(current_user):
            ui.notify('You can only edit your own adverts', type='warning')
            ui.navigate.to('/vendor/dashboard')
            return

    # --- Enhanced Layout with Green Theme ---
    with ui.row().classes("w-full min-h-screen bg-gradient-to-br from-green-50 to-emerald-50"):
        # Sidebar
        with ui.column().classes("w-80 bg-gradient-to-b from-emerald-900 to-green-900 shadow-2xl min-h-screen relative"):
            show_side_bar()

        # Main content area
        with ui.column().classes("flex-1 p-8 overflow-auto"):
            # Header Section
            with ui.column().classes("w-full text-center mb-8"):
                ui.icon('edit', size='xl', color='green').classes("text-green-500 text-6xl mb-4")
                ui.label('EDIT ADVERTISEMENT').classes(
                    'text-4xl font-bold text-green-900 mb-2'
                )
                ui.label('Update your restaurant offering').classes(
                    'text-lg text-green-600'
                )

            # Main Edit Form Card
            with ui.card().classes(
                'w-full max-w-3xl mx-auto p-8 bg-white border-2 border-green-200 rounded-2xl shadow-2xl hover:shadow-3xl transition-all duration-300'
            ):
                # Form Sections in 2-column layout
                with ui.grid(columns=2).classes("w-full gap-8"):
                    # Left Column - Basic Information
                    with ui.column().classes("space-y-6"):
                        # Title Section
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Advert Title').classes('text-lg font-semibold text-green-800')
                            title_input = ui.input(
                                value=advert.get('name', '') if advert else '',
                                placeholder='Enter a catchy title for your dish...'
                            ).props('outlined dense').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                        # Price Section
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Price (GHS)').classes('text-lg font-semibold text-green-800')
                            price_input = ui.number(
                                value=advert.get('price', 0) if advert else 0,
                                placeholder='0.00',
                                format='%.2f',
                                min=0,
                                max=1000
                            ).props('outlined dense prefix=GHS').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                        # Category Section
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Category').classes('text-lg font-semibold text-green-800')
                            category_select = ui.select(
                                options=[
                                    'Appetizers', 'Main Course', 'Desserts', 'Beverages',
                                    'Specials', 'Breakfast', 'Lunch', 'Dinner',
                                    'Snacks', 'Salads', 'Soups', 'Seafood', 'Vegetarian', 'Vegan'
                                ],
                                value=advert.get('category', '') if advert else '',
                                placeholder='Select food category'
                            ).props('outlined dense').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                        # Preparation Time
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Preparation Time (minutes)').classes('text-lg font-semibold text-green-800')
                            prep_time_input = ui.number(
                                value=advert.get('preparation_time', 0) if advert else 0,
                                placeholder='e.g., 30',
                                min=0,
                                max=300
                            ).props('outlined dense suffix=minutes').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                        # Spiciness Level
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Spiciness Level').classes('text-lg font-semibold text-green-800')
                            spiciness_select = ui.select(
                                options=['Mild', 'Medium', 'Hot', 'Very Hot', 'Not Spicy'],
                                value=advert.get('spiciness_level', '') if advert else '',
                                placeholder='Select spiciness level'
                            ).props('outlined dense').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                    # Right Column - Detailed Information
                    with ui.column().classes("space-y-6"):
                        # Description Section
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Description').classes('text-lg font-semibold text-green-800')
                            description_textarea = ui.textarea(
                                value=advert.get('description', '') if advert else '',
                                placeholder='Describe your dish in detail...'
                            ).props('outlined dense auto-grow rows=4').classes('w-full border-green-300 focus:border-green-500 text-green-900')
                            desc_counter = ui.label(f"{len(advert.get('description', '')) if advert else 0}/500 characters").classes("text-green-600 text-sm")

                        # Ingredients Section
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Ingredients').classes('text-lg font-semibold text-green-800')
                            ingredients_textarea = ui.textarea(
                                value=advert.get('ingredients', '') if advert else '',
                                placeholder='List the main ingredients, separated by commas...'
                            ).props('outlined dense auto-grow rows=2').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                        # Dietary Information
                        with ui.column().classes("w-full space-y-3"):
                            ui.label('Dietary Information').classes('text-lg font-semibold text-green-800')
                            dietary_input = ui.input(
                                value=advert.get('dietary_info', '') if advert else '',
                                placeholder='e.g., Vegetarian, Gluten-Free, etc.'
                            ).props('outlined dense').classes('w-full border-green-300 focus:border-green-500 text-green-900')

                # Image Management Section - Full Width
                with ui.column().classes("w-full space-y-4 mt-6"):
                    ui.label('Advertisement Image').classes('text-lg font-semibold text-green-800')
                    
                    # Current Image Preview
                    if advert and advert.get('image'):
                        with ui.column().classes("items-center space-y-4 p-6 border-2 border-green-300 border-dashed rounded-xl bg-green-50"):
                            ui.label("Current Image").classes("text-green-700 font-semibold")
                            ui.image(advert['image']).classes("w-64 h-64 object-cover rounded-xl shadow-lg border-2 border-green-300")
                    
                    # New Image Upload
                    with ui.column().classes("w-full space-y-4"):
                        ui.label("Update Image (Optional)").classes("text-green-700 font-medium")
                        
                        if image_preview_url:
                            with ui.column().classes("items-center space-y-4 p-6 border-2 border-green-300 border-dashed rounded-xl bg-green-50"):
                                ui.image(image_preview_url).classes("w-64 h-64 object-cover rounded-xl shadow-lg border-2 border-green-300")
                                with ui.row().classes("gap-3"):
                                    ui.button("Change Image", on_click=clear_image, icon='photo_camera').props('outlined').classes(
                                        'text-blue-600 border-blue-400 hover:bg-blue-50'
                                    )
                                    ui.button("Remove New Image", on_click=clear_image, icon='delete').props('outlined').classes(
                                        'text-red-600 border-red-400 hover:bg-red-50'
                                    )
                        else:
                            # Upload Area
                            with ui.column().classes("w-full text-center p-6 border-2 border-dashed border-green-300 rounded-xl bg-green-50 hover:bg-green-100 transition-all duration-300 cursor-pointer relative group"):
                                ui.icon('cloud_upload', size='xl', color='green').classes("text-green-400 mb-3 text-4xl")
                                ui.label("Click to upload new image").classes("text-green-700 font-semibold mb-1")
                                ui.label("PNG, JPG, WEBP (Max 5MB)").classes("text-green-600 text-sm")
                                
                                flyer = ui.upload(
                                    on_upload=handle_image_upload,
                                    max_file_size=5_000_000,
                                    multiple=False
                                ).props("accept=.jpg,.jpeg,.png,.webp flat bordered").classes("w-full h-full opacity-0 absolute inset-0 cursor-pointer")

                # Action Buttons
                with ui.row().classes('w-full justify-between gap-4 mt-8'):
                    ui.button('← Cancel', 
                             on_click=lambda: ui.navigate.to('/vendor/dashboard'),
                             icon='arrow_back').classes(
                        'px-8 py-3 bg-gradient-to-r from-gray-400 to-gray-500 text-white rounded-xl hover:from-gray-500 hover:to-gray-600 font-semibold shadow-lg transition-all flex-1 cursor-pointer'
                    )
                    
                    submit_btn = ui.button('Save Changes →', 
                             on_click=lambda: submit_form(advert_id),
                             icon='check').classes(
                        'px-8 py-3 bg-gradient-to-r from-emerald-500 to-green-600 text-white rounded-xl hover:from-emerald-600 hover:to-green-700 font-bold shadow-lg hover:shadow-xl transition-all transform hover:scale-105 flex-1 cursor-pointer'
                    )

            # Tips Card
            with ui.card().classes("w-full max-w-3xl mx-auto mt-8 p-6 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-200 rounded-2xl shadow-lg"):
                ui.label("Editing Tips").classes("text-xl font-bold text-green-800 mb-4 text-center")
                with ui.grid(columns=2).classes("w-full gap-4"):
                    with ui.column().classes("space-y-2"):
                        ui.label("• Update images regularly for freshness").classes("text-green-700 text-sm")
                        ui.label("• Keep prices competitive").classes("text-green-700 text-sm")
                        ui.label("• Highlight seasonal specials").classes("text-green-700 text-sm")
                    with ui.column().classes("space-y-2"):
                        ui.label("• Update descriptions with new features").classes("text-green-700 text-sm")
                        ui.label("• Review dietary information accuracy").classes("text-green-700 text-sm")
                        ui.label("• Test new images for appeal").classes("text-green-700 text-sm")

    # Enhanced Submit Handler
    def submit_form(advert_id):
        # Basic validation
        if not title_input.value or not description_textarea.value or price_input.value is None:
            ui.notify('⚠️ Please fill in all required fields', type='warning')
            return
        
        if len(description_textarea.value) > 500:
            ui.notify('⚠️ Description too long (max 500 characters)', type='warning')
            return

        # Build payload with all fields
        payload = {
            "name": title_input.value.strip(),
            "description": description_textarea.value.strip(),
            "price": float(price_input.value),
            "category": category_select.value if category_select.value else (advert or {}).get('category', ''),
            "ingredients": ingredients_textarea.value.strip() if ingredients_textarea.value else (advert or {}).get('ingredients', ''),
            "dietary_info": dietary_input.value.strip() if dietary_input.value else (advert or {}).get('dietary_info', ''),
            "preparation_time": int(prep_time_input.value) if prep_time_input.value else (advert or {}).get('preparation_time', 0),
            "spiciness_level": spiciness_select.value if spiciness_select.value else (advert or {}).get('spiciness_level', ''),
            "is_available": True
        }
        
        # Remove empty fields to avoid validation errors
        payload = {k: v for k, v in payload.items() if v is not None and v != ''}
        
        # Add new image if available
        if image_content:
            try:
                image_base64 = base64.b64encode(image_content).decode('utf-8')
                payload["image"] = f"data:image/jpeg;base64,{image_base64}"
            except Exception as e:
                ui.notify(f'⚠️ Error processing image: {e}', type='warning')
                return

        try:
            # Show loading state
            submit_btn.props('disabled loading')
            submit_btn.set_text('Saving Changes...')
            
            # Make API request to your backend
            response = requests.put(
                f"https://advertisement-platform-server-2zhr.onrender.com/api/food/{advert_id}",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                ui.notify('✅ Advertisement updated successfully!', type='positive')
                
                # Navigate back to dashboard after delay
                ui.timer(2.0, lambda: ui.navigate.to('/vendor/dashboard'), once=True)
                
            elif response.status_code == 400:
                error_data = response.json()
                error_msg = error_data.get('detail', 'Validation error occurred')
                ui.notify(f'❌ Validation error: {error_msg}', type='negative')
                
            elif response.status_code == 401:
                ui.notify('❌ Authentication failed. Please log in again.', type='negative')
                
            elif response.status_code == 403:
                ui.notify('❌ Permission denied. You can only edit your own adverts.', type='negative')
                
            elif response.status_code == 404:
                ui.notify('❌ Advert not found. It may have been deleted.', type='negative')
                ui.timer(2.0, lambda: ui.navigate.to('/vendor/dashboard'), once=True)
                
            elif response.status_code == 422:
                error_data = response.json()
                details = error_data.get('detail', [])
                error_messages = []
                for detail in details:
                    if isinstance(detail, dict):
                        loc = detail.get('loc', [])
                        msg = detail.get('msg', 'Invalid input')
                        field = loc[-1] if loc else 'field'
                        error_messages.append(f"{field}: {msg}")
                error_msg = "; ".join(error_messages) if error_messages else "Validation error"
                ui.notify(f'❌ Input error: {error_msg}', type='negative')
                
            else:
                ui.notify(f'❌ Server error: {response.status_code}', type='negative')
                
        except requests.exceptions.Timeout:
            ui.notify('⏰ Request timeout. Please try again.', type='negative')
        except requests.exceptions.ConnectionError:
            ui.notify('🌐 Connection error. Please check your internet connection.', type='negative')
        except Exception as e:
            ui.notify(f'❌ Unexpected error: {str(e)}', type='negative')
        finally:
            # Restore submit button
            submit_btn.props(remove='disabled loading')
            submit_btn.set_text('Save Changes →')

    # Real-time description counter update
    def update_desc_counter():
        current_length = len(description_textarea.value or '')
        desc_counter.set_text(f"{current_length}/500 characters")
        
        if current_length > 500:
            desc_counter.classes(replace="text-red-600 font-semibold")
        elif current_length > 400:
            desc_counter.classes(replace="text-orange-600")
        else:
            desc_counter.classes(replace="text-green-600")

    # Set up real-time validation
    description_textarea.on('input', lambda e: update_desc_counter())

    # Initial counter update
    update_desc_counter()

