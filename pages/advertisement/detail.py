# pages/advertisement/detail.py
from nicegui import ui
from utils.auth import get_token
import requests
from typing import Dict, Any, List, Optional

class AdvertisementDetailPage:
    """Enhanced advertisement detail page with recommendations"""
    
    def __init__(self, advertisement_id: str):
        self.advertisement_id = advertisement_id
        self.advertisement: Optional[Dict[str, Any]] = None
        self.recommended_advertisements: List[Dict[str, Any]] = []
        self.BACKEND_URL = "https://advertisement-platform-server-2zhr.onrender.com"
    
    def load_advertisement_data(self):
        """Load advertisement details from backend"""
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        try:
            # Load main advertisement
            response = requests.get(
                f"{self.BACKEND_URL}/api/advertisements/{self.advertisement_id}",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                self.advertisement = response.json()
                # Load recommendations after main ad is loaded
                self.load_recommendations()
            else:
                ui.notify('Advertisement not found', type='warning')
                
        except requests.exceptions.ConnectionError:
            ui.notify('Connection error. Please check your internet connection.', type='negative')
        except requests.exceptions.Timeout:
            ui.notify('Request timeout. Please try again.', type='negative')
        except Exception as e:
            ui.notify(f'Error loading advertisement: {str(e)}', type='negative')
    
    def load_recommendations(self):
        """Load recommended advertisements based on current ad"""
        if not self.advertisement:
            return
        
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        try:
            # Load all advertisements to find recommendations
            response = requests.get(
                f"{self.BACKEND_URL}/api/advertisements",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                all_ads = response.json()
                self.recommended_advertisements = self.get_recommendations(all_ads)
                
        except Exception as e:
            print(f"Error loading recommendations: {e}")
    
    def get_recommendations(self, all_ads: List[Dict[str, Any]], limit: int = 4) -> List[Dict[str, Any]]:
        """Get recommended advertisements based on similarity"""
        if not self.advertisement:
            return []
        
        current_ad = self.advertisement
        recommendations = []
        
        for ad in all_ads:
            # Skip current advertisement and inactive ads
            if ad.get('id') == current_ad.get('id') or not ad.get('isAvailable', False):
                continue
            
            similarity_score = self.calculate_similarity(current_ad, ad)
            
            if similarity_score > 0:
                recommendations.append((ad, similarity_score))
        
        # Sort by similarity score (highest first) and take top recommendations
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return [ad for ad, score in recommendations[:limit]]
    
    def calculate_similarity(self, ad1: Dict[str, Any], ad2: Dict[str, Any]) -> float:
        """Calculate similarity score between two advertisements"""
        score = 0.0
        
        # Category similarity (highest weight)
        if ad1.get('category') and ad2.get('category'):
            if ad1['category'] == ad2['category']:
                score += 0.4
        
        # Price similarity (similar price range)
        price1 = ad1.get('price', 0)
        price2 = ad2.get('price', 0)
        if price1 > 0 and price2 > 0:
            price_ratio = min(price1, price2) / max(price1, price2)
            score += price_ratio * 0.3
        
        # Dietary preferences similarity
        dietary1 = ad1.get('dietaryInformation', '').lower()
        dietary2 = ad2.get('dietaryInformation', '').lower()
        if dietary1 and dietary2 and any(word in dietary2 for word in dietary1.split()):
            score += 0.2
        
        # Spiciness level similarity
        if ad1.get('spicinessLevel') and ad2.get('spicinessLevel'):
            if ad1['spicinessLevel'] == ad2['spicinessLevel']:
                score += 0.1
        
        return score
    
    def create_advertisement_header(self):
        """Create the advertisement header section"""
        if not self.advertisement:
            return
        
        ad = self.advertisement
        
        with ui.column().classes("w-full bg-white rounded-lg shadow-sm p-6 mb-6"):
            with ui.row().classes("w-full items-start justify-between"):
                # Title and basic info
                with ui.column().classes("flex-1"):
                    ui.label(ad.get('name', 'Unnamed Advertisement')).classes("text-3xl font-bold text-gray-800 mb-2")
                    
                    with ui.row().classes("items-center gap-4 flex-wrap"):
                        # Category badge
                        if ad.get('category'):
                            ui.badge(ad.get('category'), color='blue').props('rounded')
                        
                        # Price
                        ui.label(f"GHS {ad.get('price', 0):.2f}").classes("text-2xl font-bold text-green-600")
                        
                        # Preparation time
                        if ad.get('preparationTime'):
                            with ui.row().classes("items-center gap-1 text-gray-600"):
                                ui.icon('schedule', size='sm')
                                ui.label(f"{ad.get('preparationTime')} minutes")
                        
                        # Status badge
                        status_color = 'positive' if ad.get('isAvailable') else 'negative'
                        status_text = 'Available' if ad.get('isAvailable') else 'Unavailable'
                        ui.badge(status_text, color=status_color).props('rounded')
                
                # Vendor info (if available)
                if ad.get('vendorName'):
                    with ui.column().classes("text-right"):
                        ui.label('Sold by').classes("text-gray-500 text-sm")
                        ui.label(ad.get('vendorName')).classes("font-semibold")
    
    def create_image_gallery(self):
        """Create image gallery section"""
        if not self.advertisement or not self.advertisement.get('image'):
            return
        
        with ui.column().classes("w-full mb-6"):
            ui.image(f"data:image/jpeg;base64,{self.advertisement['image']}").classes("w-full h-80 object-cover rounded-lg shadow-md")
    
    def create_details_section(self):
        """Create advertisement details section"""
        if not self.advertisement:
            return
        
        ad = self.advertisement
        
        with ui.grid(columns=2).classes("w-full gap-6 mb-6"):
            # Left column - Description and key details
            with ui.column().classes("space-y-6"):
                # Description
                with ui.card().classes("p-4"):
                    ui.label('Description').classes("text-xl font-semibold text-gray-800 mb-2")
                    ui.label(ad.get('description', 'No description provided.')).classes("text-gray-600 leading-relaxed")
                
                # Ingredients
                if ad.get('ingredients'):
                    with ui.card().classes("p-4"):
                        ui.label('Ingredients').classes("text-xl font-semibold text-gray-800 mb-2")
                        ingredients_list = [ing.strip() for ing in ad.get('ingredients', '').split(',') if ing.strip()]
                        with ui.column().classes("space-y-1"):
                            for ingredient in ingredients_list:
                                with ui.row().classes("items-center gap-2"):
                                    ui.icon('check', size='xs', color='green')
                                    ui.label(ingredient).classes("text-gray-600")
            
            # Right column - Additional information
            with ui.column().classes("space-y-6"):
                # Dietary information
                if ad.get('dietaryInformation'):
                    with ui.card().classes("p-4"):
                        ui.label('Dietary Information').classes("text-xl font-semibold text-gray-800 mb-2")
                        ui.label(ad.get('dietaryInformation')).classes("text-gray-600")
                
                # Spiciness level
                if ad.get('spicinessLevel'):
                    with ui.card().classes("p-4"):
                        ui.label('Spiciness Level').classes("text-xl font-semibold text-gray-800 mb-2")
                        with ui.row().classes("items-center gap-2"):
                            # Spiciness indicator
                            spiciness = ad.get('spicinessLevel', '').lower()
                            pepper_count = 0
                            if 'mild' in spiciness:
                                pepper_count = 1
                            elif 'medium' in spiciness:
                                pepper_count = 2
                            elif 'hot' in spiciness:
                                pepper_count = 3
                            elif 'very hot' in spiciness:
                                pepper_count = 4
                            
                            for i in range(pepper_count):
                                ui.icon('whatshot', color='red' if i > 1 else 'orange')
                            
                            ui.label(ad.get('spicinessLevel')).classes("text-gray-600 ml-2")
                
                # Additional details card
                with ui.card().classes("p-4"):
                    ui.label('Additional Details').classes("text-xl font-semibold text-gray-800 mb-3")
                    
                    with ui.column().classes("space-y-3"):
                        # Preparation time
                        if ad.get('preparationTime'):
                            with ui.row().classes("items-center justify-between"):
                                ui.label('Preparation Time:').classes("text-gray-600 font-medium")
                                ui.label(f"{ad.get('preparationTime')} minutes").classes("text-gray-800")
                        
                        # Category
                        if ad.get('category'):
                            with ui.row().classes("items-center justify-between"):
                                ui.label('Category:').classes("text-gray-600 font-medium")
                                ui.label(ad.get('category')).classes("text-gray-800")
                        
                        # Availability
                        with ui.row().classes("items-center justify-between"):
                            ui.label('Availability:').classes("text-gray-600 font-medium")
                            status_color = 'green' if ad.get('isAvailable') else 'red'
                            status_text = 'In Stock' if ad.get('isAvailable') else 'Out of Stock'
                            ui.label(status_text).classes(f"text-{status_color}-600 font-semibold")
    
    def create_recommendations_section(self):
        """Create recommendations section"""
        if not self.recommended_advertisements:
            return
        
        with ui.column().classes("w-full mb-6"):
            ui.label('You Might Also Like').classes("text-2xl font-bold text-gray-800 mb-4")
            
            with ui.grid(columns=2).classes("w-full gap-4"):
                for advert in self.recommended_advertisements:
                    self.create_recommendation_card(advert)
    
    def create_recommendation_card(self, advert: Dict[str, Any]):
        """Create a recommendation card"""
        with ui.card().classes("w-full cursor-pointer hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1").on_click(lambda ad=advert: self.navigate_to_advertisement(ad.get('id'))):
            # Image
            if advert.get('image'):
                ui.image(f"data:image/jpeg;base64,{advert['image']}").classes("w-full h-40 object-cover")
            else:
                with ui.column().classes("w-full h-40 bg-gray-100 flex items-center justify-center"):
                    ui.icon('restaurant', size='xl', color='gray')
            
            # Content
            with ui.column().classes("p-4"):
                # Title and category
                ui.label(advert.get('name', 'Unnamed')).classes("font-semibold text-gray-800 line-clamp-1 mb-1")
                ui.label(advert.get('category', 'Unknown')).classes("text-sm text-gray-500 mb-2")
                
                # Price and quick info
                with ui.row().classes("items-center justify-between"):
                    ui.label(f"GHS {advert.get('price', 0):.2f}").classes("text-green-600 font-bold")
                    
                    # Quick info badges
                    with ui.row().classes("items-center gap-1"):
                        if advert.get('preparationTime'):
                            ui.badge(f"⏱{advert.get('preparationTime')}m", color='blue').props('rounded dense')
                        if advert.get('spicinessLevel'):
                            spiciness = advert.get('spicinessLevel', '').lower()
                            if 'hot' in spiciness or 'very' in spiciness:
                                ui.badge('🌶️', color='orange').props('rounded dense')
                
                # Dietary tags (if any)
                if advert.get('dietaryInformation'):
                    dietary_tags = [tag.strip() for tag in advert.get('dietaryInformation', '').split(',')]
                    with ui.row().classes("flex-wrap gap-1 mt-2"):
                        for tag in dietary_tags[:2]:  # Show max 2 tags
                            if tag:
                                ui.badge(tag, color='green').props('rounded dense outline')
    
    def navigate_to_advertisement(self, advertisement_id: str):
        """Navigate to another advertisement detail page"""
        if advertisement_id:
            ui.navigate.to(f"/advertisement/{advertisement_id}")
    
    def create_action_buttons(self):
        """Create action buttons section"""
        with ui.row().classes("w-full justify-center gap-4 mb-6"):
            # Back to browse button
            ui.button('Back to Browse', on_click=lambda: ui.navigate.to('/advertisements'), icon='arrow_back').props('outlined')
            
            # Contact vendor button (if available)
            if self.advertisement and self.advertisement.get('isAvailable'):
                ui.button('Contact Vendor', on_click=self.contact_vendor, icon='message').props('unelevated')
            
            # Share button
            ui.button('Share', on_click=self.share_advertisement, icon='share').props('outlined')
    
    def contact_vendor(self):
        """Handle contact vendor action"""
        if self.advertisement:
            vendor_name = self.advertisement.get('vendorName', 'the vendor')
            ui.notify(f'Contacting {vendor_name}...', type='info')
            # Here you could implement actual contact logic
    
    def share_advertisement(self):
        """Handle share advertisement action"""
        if self.advertisement:
            ui.notify('Share functionality coming soon!', type='info')
            # Here you could implement actual sharing logic
    
    def create_loading_state(self):
        """Create loading state"""
        with ui.column().classes("w-full h-64 flex items-center justify-center"):
            ui.spinner(size='lg', color='primary')
            ui.label('Loading advertisement...').classes("text-gray-600 mt-2")
    
    def create_error_state(self):
        """Create error state for when advertisement is not found"""
        with ui.column().classes("w-full h-64 flex items-center justify-center text-center"):
            ui.icon('error', size='xl', color='red').classes("mb-4")
            ui.label('Advertisement Not Found').classes("text-xl font-bold text-gray-800 mb-2")
            ui.label('The advertisement you are looking for does not exist or has been removed.').classes("text-gray-600 mb-4")
            ui.button('Back to Browse', on_click=lambda: ui.navigate.to('/advertisements'), icon='arrow_back').props('unelevated')
    
    def render(self):
        """Render the detail page"""
        # Load data first
        self.load_advertisement_data()
        
        with ui.column().classes("w-full min-h-screen bg-gray-50 p-4 md:p-8"):
            # Back button at top
            with ui.row().classes("w-full max-w-6xl mx-auto mb-4"):
                ui.button('← Back', on_click=lambda: ui.navigate.to('/advertisements'), icon='arrow_back').props('flat')
            
            # Main content container
            with ui.column().classes("w-full max-w-6xl mx-auto"):
                if self.advertisement is None:
                    # Still loading or error
                    if hasattr(self, 'advertisement') and self.advertisement is None:
                        self.create_loading_state()
                    else:
                        self.create_error_state()
                    return
                
                # Advertisement content
                self.create_advertisement_header()
                self.create_image_gallery()
                self.create_details_section()
                self.create_recommendations_section()
                self.create_action_buttons()

@ui.page("/advertisement/{advertisement_id}")
def advertisement_detail_page(advertisement_id: str):
    """Advertisement detail page route"""
    page = AdvertisementDetailPage(advertisement_id)
    page.render()