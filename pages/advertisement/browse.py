# pages/advertisements/browse.py
from nicegui import ui
from utils.auth import get_token
import requests
from typing import List, Dict, Any

class AdvertisementsBrowsePage:
    """Simple advertisements browsing page"""
    
    def __init__(self):
        self.advertisements: List[Dict[str, Any]] = []
        self.BACKEND_URL = "https://advertisement-platform-server-2zhr.onrender.com"
    
    def load_advertisements(self):
        """Load advertisements from backend"""
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        
        try:
            response = requests.get(
                f"{self.BACKEND_URL}/api/advertisements",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                self.advertisements = [ad for ad in response.json() if ad.get('isAvailable', False)]
                self.refresh_advertisement_grid()
            else:
                ui.notify('Failed to load advertisements', type='negative')
                
        except Exception as e:
            ui.notify(f'Error loading advertisements: {str(e)}', type='negative')
    
    def create_advertisement_grid(self):
        """Create the advertisements grid"""
        self.adverts_container = ui.grid(columns=2).classes("w-full gap-6")
        self.refresh_advertisement_grid()
    
    def refresh_advertisement_grid(self):
        """Refresh the advertisement grid display"""
        if hasattr(self, 'adverts_container'):
            self.adverts_container.clear()
            
            with self.adverts_container:
                if not self.advertisements:
                    with ui.column().classes("col-span-2 text-center py-12"):
                        ui.icon('search_off', size='xl', color='gray')
                        ui.label('No advertisements available').classes("text-xl text-gray-600")
                    return
                
                for advert in self.advertisements:
                    self.create_advertisement_card(advert)
    
    def create_advertisement_card(self, advert: Dict[str, Any]):
        """Create an advertisement card for browsing"""
        with ui.card().classes("w-full cursor-pointer hover:shadow-lg transition-all").on_click(lambda ad=advert: ui.navigate.to(f"/advertisement/{ad.get('id')}")):
            # Image
            if advert.get('image'):
                ui.image(f"data:image/jpeg;base64,{advert['image']}").classes("w-full h-48 object-cover")
            else:
                with ui.column().classes("w-full h-48 bg-gray-100 flex items-center justify-center"):
                    ui.icon('restaurant', size='xl', color='gray')
            
            # Content
            with ui.column().classes("p-4"):
                ui.label(advert.get('name', 'Unnamed')).classes("font-bold text-lg text-gray-800 line-clamp-1")
                ui.label(advert.get('category', 'Unknown')).classes("text-gray-500 text-sm mb-2")
                
                # Price and quick info
                with ui.row().classes("items-center justify-between"):
                    ui.label(f"GHS {advert.get('price', 0):.2f}").classes("text-green-600 font-bold")
                    
                    if advert.get('preparationTime'):
                        ui.badge(f"{advert.get('preparationTime')}min", color='blue')
                
                # Short description
                if advert.get('description'):
                    ui.label(advert.get('description')).classes("text-gray-600 text-sm line-clamp-2 mt-2")
    
    def render(self):
        """Render the browse page"""
        with ui.column().classes("w-full min-h-screen bg-gray-50 p-8"):
            # Header
            ui.label('Browse Advertisements').classes("text-4xl font-bold text-gray-800 mb-2")
            ui.label('Discover amazing food offerings from local vendors').classes("text-lg text-gray-600 mb-8")
            
            # Advertisements grid
            self.create_advertisement_grid()
        
        # Load data
        self.load_advertisements()

@ui.page("/advertisements")
def advertisements_browse_page():
    """Advertisements browse page"""
    page = AdvertisementsBrowsePage()
    page.render()