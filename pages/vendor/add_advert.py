from nicegui import ui
from components.sidebar import show_side_bar
from utils.auth import require_vendor, get_user_id, get_token
import requests
import base64
import time
from typing import Optional, Dict, Any
import logging

# Configuration
CONFIG = {
    'BACKEND_URL': 'https://advertisement-platform-server-2zhr.onrender.com',
    'MAX_DESCRIPTION_LENGTH': 500,
    'MAX_TITLE_LENGTH': 100,
    'MAX_PRICE': 10000,
    'MAX_FILE_SIZE': 5_000_000,
    'SUBMISSION_COOLDOWN': 2,
    'API_TIMEOUT': 30
}

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIError(Exception):
    """Custom exception for API errors"""
    pass

class AdvertisementService:
    """Handles communication with the backend API"""
    
    @staticmethod
    def create_advertisement(advertisement_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new advertisement via API"""
        token = get_token()
        if not token:
            raise APIError("Authentication token not found")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(
                f"{CONFIG['BACKEND_URL']}/api/advertisements",
                json=advertisement_data,
                headers=headers,
                timeout=CONFIG['API_TIMEOUT']
            )
            
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json()
                raise APIError(f"Validation error: {error_data.get('message', 'Unknown error')}")
            elif response.status_code == 401:
                raise APIError("Authentication failed")
            elif response.status_code == 403:
                raise APIError("Permission denied")
            elif response.status_code == 422:
                error_data = response.json()
                raise APIError(f"Validation error: {error_data.get('message', 'Invalid data')}")
            else:
                raise APIError(f"Server error: {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise APIError("Request timeout")
        except requests.exceptions.ConnectionError:
            raise APIError("Connection error")
        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

class AdvertisementForm:
    """Manages the advertisement form state and validation"""
    
    def __init__(self):
        self.image_content: Optional[bytes] = None
        self.image_preview_url: Optional[str] = None
        self.is_submitting: bool = False
        self.last_submission_time: float = 0
        
    def set_image(self, image_content: bytes):
        """Set uploaded image"""
        self.image_content = image_content
        self.image_preview_url = f"data:image/jpeg;base64,{base64.b64encode(image_content).decode()}"
    
    def clear_image(self):
        """Clear uploaded image"""
        self.image_content = None
        self.image_preview_url = None
    
    def can_submit(self) -> bool:
        """Check if form can be submitted (rate limiting)"""
        return time.time() - self.last_submission_time > CONFIG['SUBMISSION_COOLDOWN']
    
    def start_submission(self):
        """Mark submission start"""
        self.is_submitting = True
        self.last_submission_time = time.time()
    
    def end_submission(self):
        """Mark submission end"""
        self.is_submitting = False

class FormValidator:
    """Handles form validation"""
    
    @staticmethod
    def validate_title(title: str) -> tuple[bool, str]:
        if not title or not title.strip():
            return False, "Title is required"
        if len(title.strip()) < 3:
            return False, "Title must be at least 3 characters"
        if len(title.strip()) > CONFIG['MAX_TITLE_LENGTH']:
            return False, f"Title must be less than {CONFIG['MAX_TITLE_LENGTH']} characters"
        return True, ""
    
    @staticmethod
    def validate_description(description: str) -> tuple[bool, str]:
        if not description or not description.strip():
            return False, "Description is required"
        if len(description) > CONFIG['MAX_DESCRIPTION_LENGTH']:
            return False, f"Description must be less than {CONFIG['MAX_DESCRIPTION_LENGTH']} characters"
        return True, ""
    
    @staticmethod
    def validate_price(price: Optional[float]) -> tuple[bool, str]:
        if price is None:
            return False, "Price is required"
        if price <= 0:
            return False, "Price must be greater than 0"
        if price > CONFIG['MAX_PRICE']:
            return False, f"Price must be less than {CONFIG['MAX_PRICE']}"
        return True, ""
    
    @staticmethod
    def validate_category(category: Optional[str]) -> tuple[bool, str]:
        if not category:
            return False, "Category is required"
        return True, ""
    
    @staticmethod
    def validate_prep_time(prep_time: Optional[int]) -> tuple[bool, str]:
        if prep_time is not None and prep_time < 0:
            return False, "Preparation time cannot be negative"
        return True, ""

class AdvertisementFormUI:
    """Handles the UI components for the advertisement form"""
    
    def __init__(self, form: AdvertisementForm, validator: FormValidator):
        self.form = form
        self.validator = validator
        self.components: Dict[str, Any] = {}
        self.submit_callback = None
    
    def create_page_header(self):
        """Create the page header"""
        with ui.column().classes("w-full text-center mb-8"):
            ui.icon('restaurant', size='xl', color='primary').classes("text-6xl mb-4")
            ui.label('Create New Advertisement').classes('text-4xl font-bold text-gray-800 mb-2')
            ui.label('Showcase your restaurant\'s offerings').classes('text-lg text-gray-600')
    
    def create_form_section(self):
        """Create the main form section"""
        with ui.card().classes('w-full max-w-4xl mx-auto p-8'):
            # Two-column layout for form fields
            with ui.grid(columns=2).classes("w-full gap-8"):
                self._create_left_column()
                self._create_right_column()
            
            self._create_image_section()
            self._create_status_section()
            self._create_action_buttons()
    
    def _create_left_column(self):
        """Create left column form fields"""
        with ui.column().classes("space-y-6"):
            # Title
            self._create_field(
                'title_input', 'Advert Title', 'input',
                placeholder='Enter advertisement title...'
            )
            
            # Price
            self._create_field(
                'price_input', 'Price (GHS)', 'number',
                placeholder='0.00', format='%.2f', min=0, max=CONFIG['MAX_PRICE'],
                prefix='GHS'
            )
            
            # Category
            self._create_select_field(
                'category_select', 'Category', [
                    'Appetizers', 'Main Course', 'Desserts', 'Beverages', 
                    'Breakfast', 'Lunch', 'Dinner', 'Vegetarian', 'Vegan'
                ]
            )
            
            # Preparation Time
            self._create_field(
                'prep_time_input', 'Preparation Time (minutes)', 'number',
                placeholder='30', min=0, max=300, suffix='minutes'
            )
    
    def _create_right_column(self):
        """Create right column form fields"""
        with ui.column().classes("space-y-6"):
            # Description with character counter
            with ui.column().classes("w-full space-y-2"):
                ui.label('Description').classes('text-lg font-semibold text-gray-700')
                with ui.row().classes("w-full justify-between"):
                    self.components['desc_counter'] = ui.label(f"0/{CONFIG['MAX_DESCRIPTION_LENGTH']}").classes("text-sm text-gray-500")
                
                self.components['description_textarea'] = ui.textarea(
                    placeholder='Describe your offering...'
                ).props('outlined auto-grow').classes('w-full')
            
            # Ingredients
            self._create_textarea_field(
                'ingredients_textarea', 'Ingredients',
                placeholder='List ingredients separated by commas...'
            )
            
            # Dietary Information
            self._create_field(
                'dietary_input', 'Dietary Information', 'input',
                placeholder='e.g., Vegetarian, Gluten-Free...'
            )
            
            # Spiciness Level
            self._create_select_field(
                'spiciness_select', 'Spiciness Level', 
                ['Not Spicy', 'Mild', 'Medium', 'Hot', 'Very Hot']
            )
    
    def _create_field(self, key: str, label: str, field_type: str, **kwargs):
        """Create a form field with consistent styling"""
        with ui.column().classes("w-full space-y-2"):
            ui.label(label).classes('text-lg font-semibold text-gray-700')
            
            if field_type == 'input':
                # Remove unsupported parameters
                kwargs.pop('max_length', None)
                self.components[key] = ui.input(**kwargs).props('outlined').classes('w-full')
            elif field_type == 'number':
                self.components[key] = ui.number(**kwargs).props('outlined').classes('w-full')
            elif field_type == 'textarea':
                # Remove unsupported parameters for textarea
                kwargs.pop('rows', None)
                self.components[key] = ui.textarea(**kwargs).props('outlined').classes('w-full')
    
    def _create_textarea_field(self, key: str, label: str, **kwargs):
        """Create a textarea field with specific styling"""
        with ui.column().classes("w-full space-y-2"):
            ui.label(label).classes('text-lg font-semibold text-gray-700')
            # Remove unsupported parameters
            kwargs.pop('rows', None)
            self.components[key] = ui.textarea(**kwargs).props('outlined').classes('w-full')
    
    def _create_select_field(self, key: str, label: str, options: list, **kwargs):
        """Create a select field"""
        with ui.column().classes("w-full space-y-2"):
            ui.label(label).classes('text-lg font-semibold text-gray-700')
            # Remove placeholder from kwargs as it's not supported by NiceGUI select
            kwargs.pop('placeholder', None)
            self.components[key] = ui.select(options, value=None, **kwargs).props('outlined').classes('w-full')
            # Add a label to indicate selection hint
            ui.label('Select an option').classes('text-xs text-gray-500')
    
    def _create_image_section(self):
        """Create image upload section"""
        with ui.column().classes("w-full space-y-4 mt-8"):
            ui.label('Advertisement Image').classes('text-lg font-semibold text-gray-700')
            
            if self.form.image_preview_url:
                self._show_image_preview()
            else:
                self._show_upload_area()
    
    def _show_image_preview(self):
        """Show image preview when image is uploaded"""
        with ui.column().classes("items-center space-y-4 p-6 border-2 border-dashed border-gray-300 rounded-lg"):
            ui.image(self.form.image_preview_url).classes("w-64 h-64 object-cover rounded-lg")
            with ui.row().classes("gap-3"):
                ui.button("Change Image", on_click=self._on_change_image, icon='edit').props('outlined')
                ui.button("Remove Image", on_click=self._on_remove_image, icon='delete').props('outlined').classes('text-red-500')
    
    def _show_upload_area(self):
        """Show upload area when no image is present"""
        with ui.column().classes("w-full text-center p-8 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50"):
            ui.icon('cloud_upload', size='xl').classes("text-4xl text-gray-400 mb-3")
            ui.label("Click to upload or drag & drop").classes("text-gray-700 font-medium")
            ui.label("PNG, JPG, WEBP (Max 5MB)").classes("text-gray-500 text-sm")
            
            ui.upload(
                on_upload=self._on_image_upload,
                max_file_size=CONFIG['MAX_FILE_SIZE'],
                multiple=False
            ).props("accept=.jpg,.jpeg,.png,.webp").classes("absolute inset-0 opacity-0")
    
    def _create_status_section(self):
        """Create form status section"""
        with ui.row().classes("w-full items-center justify-between mt-6 p-4 bg-blue-50 rounded-lg"):
            with ui.row().classes("items-center gap-3"):
                self.components['status_icon'] = ui.icon('info', color='blue')
                self.components['status_label'] = ui.label("Fill in all required fields").classes("text-blue-700")
            
            self.components['form_progress'] = ui.label().classes("text-blue-600")
    
    def _create_action_buttons(self):
        """Create form action buttons"""
        with ui.row().classes('w-full justify-end gap-4 mt-8'):
            ui.button('Cancel', on_click=self._on_cancel, icon='cancel').props('outlined').classes("bg-emerald-100 text-emerald-700 hover:bg-emerald-200")
            self.components['submit_button'] = ui.button(
                'Create Advertisement', 
                on_click=self._on_submit, 
                icon='check'
            ).props('unelevated').classes('bg-green-600 text-white')
    
    def set_submit_callback(self, callback):
        """Set the submit callback function"""
        self.submit_callback = callback
    
    def _update_desc_counter(self):
        """Update description character counter"""
        if 'description_textarea' in self.components and 'desc_counter' in self.components:
            text = self.components['description_textarea'].value or ''
            self.components['desc_counter'].set_text(f"{len(text)}/{CONFIG['MAX_DESCRIPTION_LENGTH']}")
    
    def _on_image_upload(self, e):
        """Handle image upload"""
        try:
            self.form.set_image(e.content)
            ui.notify('Image uploaded successfully', type='positive')
            # Use JavaScript to reload the image section instead of full page reload
            ui.run_javascript("location.reload()")
        except Exception as ex:
            ui.notify(f'Error uploading image: {str(ex)}', type='negative')
    
    def _on_change_image(self):
        """Handle change image request"""
        self.form.clear_image()
        ui.run_javascript("location.reload()")
    
    def _on_remove_image(self):
        """Handle remove image request"""
        self.form.clear_image()
        ui.notify('Image removed', type='info')
        ui.run_javascript("location.reload()")
    
    def _on_cancel(self):
        """Handle cancel action"""
        ui.navigate.to('/vendor/dashboard')
    
    def _on_submit(self):
        """Handle form submission"""
        if self.submit_callback:
            self.submit_callback()

class AdvertisementController:
    """Controls the advertisement creation flow"""
    
    def __init__(self):
        self.form = AdvertisementForm()
        self.validator = FormValidator()
        self.ui = AdvertisementFormUI(self.form, self.validator)
        self.ui.set_submit_callback(self.submit_advertisement)
    
    def _setup_validation(self):
        """Setup real-time form validation"""
        # Description character counter
        if 'description_textarea' in self.ui.components:
            self.ui.components['description_textarea'].on('input', self._update_desc_counter)
        
        # Field validation on blur
        fields_to_validate = [
            ('title_input', self.validator.validate_title),
            ('price_input', self.validator.validate_price),
            ('category_select', self.validator.validate_category)
        ]
        
        for field_name, validator_func in fields_to_validate:
            if field_name in self.ui.components:
                self.ui.components[field_name].on('blur', lambda f=field_name, v=validator_func: self._validate_field(f, v))
    
    def _validate_field(self, field_name: str, validator_func):
        """Validate a specific field"""
        value = self.ui.components[field_name].value
        is_valid, message = validator_func(value)
        
        if not is_valid and value:
            self.ui.components[field_name].props('error')
            if message:
                ui.notify(message, type='warning', timeout=2000)
        else:
            self.ui.components[field_name].props(remove='error')
    
    def _update_desc_counter(self):
        """Update description character counter"""
        self.ui._update_desc_counter()
        self._update_form_status()
    
    def _update_form_status(self):
        """Update the overall form status"""
        required_fields = [
            ('Title', self.ui.components['title_input'].value if 'title_input' in self.ui.components else None),
            ('Description', self.ui.components['description_textarea'].value if 'description_textarea' in self.ui.components else None),
            ('Price', self.ui.components['price_input'].value if 'price_input' in self.ui.components else None),
            ('Category', self.ui.components['category_select'].value if 'category_select' in self.ui.components else None)
        ]
        
        missing = [name for name, value in required_fields if not value]
        
        if not missing:
            self.ui.components['status_label'].set_text("All required fields are filled")
            self.ui.components['status_icon'].set_name('check_circle')
        else:
            self.ui.components['status_label'].set_text(f"Missing: {', '.join(missing)}")
            self.ui.components['status_icon'].set_name('error')
    
    def _prepare_advertisement_data(self) -> Dict[str, Any]:
        """Prepare data for API submission"""
        data = {
            "name": (self.ui.components['title_input'].value or '').strip(),
            "description": (self.ui.components['description_textarea'].value or '').strip(),
            "price": float(self.ui.components['price_input'].value or 0),
            "category": self.ui.components['category_select'].value or '',
            "ingredients": (self.ui.components['ingredients_textarea'].value or '').strip(),
            "dietaryInformation": (self.ui.components['dietary_input'].value or '').strip(),
            "preparationTime": int(self.ui.components['prep_time_input'].value or 0) if 'prep_time_input' in self.ui.components else 0,
            "spicinessLevel": self.ui.components['spiciness_select'].value or '' if 'spiciness_select' in self.ui.components else '',
            "vendorId": str(get_user_id()),
            "isAvailable": True
        }
        
        # Add image if available
        if self.form.image_content:
            try:
                data["image"] = base64.b64encode(self.form.image_content).decode('utf-8')
            except Exception as e:
                logger.error(f"Error encoding image: {e}")
        
        return {k: v for k, v in data.items() if v is not None}
    
    def _validate_form(self) -> tuple[bool, str]:
        """Validate the entire form"""
        validations = [
            self.validator.validate_title(self.ui.components['title_input'].value),
            self.validator.validate_description(self.ui.components['description_textarea'].value),
            self.validator.validate_price(self.ui.components['price_input'].value),
            self.validator.validate_category(self.ui.components['category_select'].value)
        ]
        
        for is_valid, message in validations:
            if not is_valid:
                return False, message
        
        return True, ""
    
    def submit_advertisement(self):
        """Handle form submission"""
        # Rate limiting
        if not self.form.can_submit():
            ui.notify('Please wait before submitting again', type='warning')
            return
        
        # Validation
        is_valid, error_message = self._validate_form()
        if not is_valid:
            ui.notify(error_message, type='negative')
            return
        
        # Authentication check
        if not get_token():
            ui.notify('Please log in again', type='negative')
            ui.navigate.to('/login')
            return
        
        # Update UI state
        self.form.start_submission()
        submit_button = self.ui.components['submit_button']
        submit_button.props('disabled loading')
        submit_button.set_text('Creating...')
        
        try:
            # Prepare and send data
            advertisement_data = self._prepare_advertisement_data()
            result = AdvertisementService.create_advertisement(advertisement_data)
            
            ui.notify('Advertisement created successfully!', type='positive')
            self._reset_form()
            
            # Redirect after delay
            ui.timer(2.0, lambda: ui.navigate.to('/vendor/dashboard'), once=True)
            
        except APIError as e:
            ui.notify(f'Error: {str(e)}', type='negative')
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            ui.notify('An unexpected error occurred', type='negative')
        finally:
            self.form.end_submission()
            submit_button.props(remove='disabled loading')
            submit_button.set_text('Create Advertisement')
    
    def _reset_form(self):
        """Reset the form to initial state"""
        for component in self.ui.components.values():
            if hasattr(component, 'value'):
                if hasattr(component, 'set_value'):
                    component.set_value(None)
                else:
                    component.value = ''
        
        self.form.clear_image()
    
    def render(self):
        """Render the complete page"""
        if not require_vendor():
            return
        
        with ui.column().classes("w-full min-h-screen bg-gray-50"):
            with ui.row().classes("w-full h-full"):
                # Sidebar
                with ui.column().classes("bg-gray-800 text-white min-h-screen w-64"):
                    show_side_bar()
                
                # Main content
                with ui.column().classes("flex-1 p-8 overflow-auto"):
                    self.ui.create_page_header()
                    self.ui.create_form_section()
        
        # Setup event handlers AFTER UI is rendered
        self._setup_validation()
        
        # Initial status update
        self._update_form_status()
        self._update_desc_counter()

@ui.page("/vendor/add_advert")
def advertisement_creation_page():
    """Page function for advertisement creation"""
    controller = AdvertisementController()
    controller.render()

# For testing purposes
if __name__ == "__main__":
    ui.run()