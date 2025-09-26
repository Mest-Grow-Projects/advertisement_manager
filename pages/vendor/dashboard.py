# pages/vendor/dashboard.py
from nicegui import ui
from components.sidebar import show_side_bar
from utils.auth import require_vendor, get_user_id, get_token
import requests
import datetime
from typing import List, Dict, Any

class VendorDashboard:
    def __init__(self):
        self.advertisements = []
        self.filtered_advertisements = []
        self.search_term = ""
        self.current_filters = {}
        self.BACKEND_URL = "https://advertisement-platform-server-2zhr.onrender.com"
    
    def load_advertisements(self):
        """Load all advertisements and filter by vendor ID"""
        token = get_token()
        if not token:
            ui.notify('Please log in to view advertisements', type='warning')
            return
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(
                f"{self.BACKEND_URL}/api/advertisements",
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                all_advertisements = response.json()
                # Filter advertisements by current vendor's ID
                vendor_id = get_user_id()
                self.advertisements = [
                    ad for ad in all_advertisements 
                    if str(ad.get('vendorId')) == str(vendor_id)
                ]
                self.apply_filters()
                ui.notify(f'Loaded {len(self.advertisements)} advertisements', type='positive')
            else:
                ui.notify('Failed to load advertisements', type='negative')
                print(f"API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            ui.notify('Connection error. Please check your internet connection.', type='negative')
        except requests.exceptions.Timeout:
            ui.notify('Request timeout. Please try again.', type='negative')
        except Exception as e:
            ui.notify(f'Error loading advertisements: {str(e)}', type='negative')
            print(f"Error: {e}")
    
    def create_search_section(self):
        """Create search and filter section"""
        with ui.card().classes("w-full mb-6 bg-white shadow-sm"):
            with ui.column().classes("w-full space-y-4 p-4"):
                # Search header
                ui.label('Search & Filter Advertisements').classes("text-xl font-bold text-gray-800")
                
                # Search input
                with ui.row().classes("w-full items-center gap-4"):
                    self.search_input = ui.input(
                        placeholder='Search by title, description, or ingredients...',
                        on_change=lambda e: self.on_search_change(e.value)
                    ).props('outlined dense').classes("flex-1")
                    
                    ui.button('Search', on_click=self.apply_filters, icon='search').props('outlined')
                    ui.button('Clear', on_click=self.clear_filters, icon='clear').props('outlined')
                
                # Quick filters
                with ui.row().classes("w-full items-center gap-4 flex-wrap"):
                    ui.label('Quick Filters:').classes("font-semibold text-gray-700")
                    
                    # Status filter
                    self.status_filter = ui.select(
                        options=['All', 'Active', 'Inactive'],
                        value='All',
                        on_change=lambda e: self.on_filter_change('status', e.value)
                    ).props('outlined dense').classes("min-w-32")
                    
                    # Category filter
                    self.category_filter = ui.select(
                        options=['All Categories'] + self.get_unique_categories(),
                        value='All Categories',
                        on_change=lambda e: self.on_filter_change('category', e.value)
                    ).props('outlined dense').classes("min-w-40")
                    
                    # Price range
                    with ui.row().classes("items-center gap-2"):
                        ui.label('Price (GHS):').classes("text-gray-700")
                        self.min_price = ui.number(
                            placeholder='Min',
                            min=0,
                            format='%.2f',
                            on_change=self.apply_filters
                        ).props('outlined dense').classes("w-24")
                        ui.label('to').classes("text-gray-500")
                        self.max_price = ui.number(
                            placeholder='Max',
                            min=0,
                            format='%.2f',
                            on_change=self.apply_filters
                        ).props('outlined dense').classes("w-24")
    
    def get_unique_categories(self):
        """Get unique categories from advertisements"""
        categories = set()
        for ad in self.advertisements:
            if ad.get('category'):
                categories.add(ad['category'])
        return sorted(list(categories))
    
    def on_search_change(self, search_term):
        """Handle search term change"""
        self.search_term = search_term.lower()
        self.apply_filters()
    
    def on_filter_change(self, filter_type, value):
        """Handle filter changes"""
        if value in ['All', 'All Categories']:
            self.current_filters.pop(filter_type, None)
        else:
            self.current_filters[filter_type] = value
        self.apply_filters()
    
    def apply_filters(self):
        """Apply current filters and search"""
        self.filtered_advertisements = self.advertisements.copy()
        
        # Apply search filter
        if self.search_term:
            self.filtered_advertisements = [
                adv for adv in self.filtered_advertisements
                if (self.search_term in adv.get('name', '').lower() or
                    self.search_term in adv.get('description', '').lower() or
                    self.search_term in adv.get('ingredients', '').lower())
            ]
        
        # Apply status filter
        if 'status' in self.current_filters:
            status_filter = self.current_filters['status']
            if status_filter == 'Active':
                self.filtered_advertisements = [adv for adv in self.filtered_advertisements if adv.get('isAvailable', False)]
            elif status_filter == 'Inactive':
                self.filtered_advertisements = [adv for adv in self.filtered_advertisements if not adv.get('isAvailable', False)]
        
        # Apply category filter
        if 'category' in self.current_filters:
            category_filter = self.current_filters['category']
            self.filtered_advertisements = [
                adv for adv in self.filtered_advertisements 
                if adv.get('category') == category_filter
            ]
        
        # Apply price filter
        min_price = self.min_price.value
        max_price = self.max_price.value
        
        if min_price is not None:
            self.filtered_advertisements = [
                adv for adv in self.filtered_advertisements 
                if adv.get('price', 0) >= min_price
            ]
        
        if max_price is not None:
            self.filtered_advertisements = [
                adv for adv in self.filtered_advertisements 
                if adv.get('price', 0) <= max_price
            ]
        
        # Apply default sorting (newest first)
        self.filtered_advertisements.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        self.refresh_advertisement_list()
    
    def clear_filters(self):
        """Clear all filters"""
        self.search_input.value = ""
        self.search_term = ""
        self.status_filter.value = 'All'
        self.category_filter.value = 'All Categories'
        self.min_price.value = None
        self.max_price.value = None
        self.current_filters = {}
        self.apply_filters()
    
    def create_advertisement_list(self):
        """Create the advertisement list section"""
        with ui.column().classes("w-full"):
            # Results count and sort
            with ui.row().classes("w-full justify-between items-center mb-4 p-4 bg-gray-50 rounded-lg"):
                ui.label(f'Showing {len(self.filtered_advertisements)} of {len(self.advertisements)} advertisements').classes("text-gray-700 font-medium")
                
                # Sort options
                with ui.row().classes("items-center gap-2"):
                    ui.label('Sort by:').classes("text-gray-700")
                    self.sort_select = ui.select(
                        options=['Newest First', 'Oldest First', 'Price: Low to High', 'Price: High to Low', 'Name: A-Z'],
                        value='Newest First',
                        on_change=self.sort_advertisements
                    ).props('outlined dense')
            
            # Advertisements grid
            self.adverts_container = ui.column().classes("w-full space-y-4")
            self.refresh_advertisement_list()
    
    def sort_advertisements(self, e):
        """Sort advertisements based on selection"""
        sort_by = e.value
        
        if sort_by == 'Newest First':
            self.filtered_advertisements.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        elif sort_by == 'Oldest First':
            self.filtered_advertisements.sort(key=lambda x: x.get('createdAt', ''))
        elif sort_by == 'Price: Low to High':
            self.filtered_advertisements.sort(key=lambda x: x.get('price', 0))
        elif sort_by == 'Price: High to Low':
            self.filtered_advertisements.sort(key=lambda x: x.get('price', 0), reverse=True)
        elif sort_by == 'Name: A-Z':
            self.filtered_advertisements.sort(key=lambda x: x.get('name', '').lower())
        
        self.refresh_advertisement_list()
    
    def refresh_advertisement_list(self):
        """Refresh the advertisement list display"""
        if hasattr(self, 'adverts_container'):
            self.adverts_container.clear()
            
            with self.adverts_container:
                if not self.filtered_advertisements:
                    self.show_empty_state()
                else:
                    for advert in self.filtered_advertisements:
                        self.create_advertisement_card(advert)
    
    def show_empty_state(self):
        """Show empty state message"""
        with ui.card().classes("w-full text-center py-12").props('flat'):
            if self.search_term or self.current_filters:
                # No results for current filters
                ui.icon('search_off', size='xl', color='gray').classes("mb-4")
                ui.label('No advertisements match your search criteria').classes("text-xl text-gray-600 mb-2")
                ui.label('Try adjusting your filters or search terms').classes("text-gray-500")
                ui.button('Clear Filters', on_click=self.clear_filters, icon='clear').props('outlined').classes("mt-4")
            else:
                # No advertisements at all
                ui.icon('add_shopping_cart', size='xl', color='gray').classes("mb-4")
                ui.label('No advertisements yet').classes("text-xl text-gray-600 mb-2")
                ui.label('Create your first advertisement to get started').classes("text-gray-500")
                ui.button('Create Advertisement', on_click=lambda: ui.navigate.to('/vendor/add_advert'), icon='add').props('unelevated').classes("mt-4")
    
    def create_advertisement_card(self, advert: Dict[str, Any]):
        """Create an individual advertisement card"""
        with ui.card().classes("w-full hover:shadow-lg transition-shadow duration-300 border-l-4 border-green-500" if advert.get('isAvailable') else "w-full hover:shadow-lg transition-shadow duration-300 border-l-4 border-gray-400"):
            with ui.row().classes("w-full items-start gap-4 p-4"):
                # Image column
                with ui.column().classes("w-24 flex-shrink-0"):
                    if advert.get('image'):
                        ui.image(f"data:image/jpeg;base64,{advert['image']}").classes("w-24 h-24 object-cover rounded-lg")
                    else:
                        with ui.column().classes("w-24 h-24 bg-gray-100 rounded-lg flex items-center justify-center"):
                            ui.icon('restaurant', size='xl', color='gray')
                
                # Content column
                with ui.column().classes("flex-1 space-y-2 min-w-0"):
                    # Header row
                    with ui.row().classes("w-full justify-between items-start"):
                        with ui.column().classes("flex-1 min-w-0"):
                            ui.label(advert.get('name', 'Unnamed Advertisement')).classes("text-xl font-bold text-gray-800 truncate")
                            with ui.row().classes("items-center gap-2 mt-1 flex-wrap"):
                                if advert.get('category'):
                                    ui.badge(advert.get('category'), color='blue').props('rounded')
                                if advert.get('spicinessLevel'):
                                    ui.badge(f"🌶️ {advert.get('spicinessLevel')}", color='orange').props('rounded')
                                ui.badge(
                                    'Active' if advert.get('isAvailable') else 'Inactive',
                                    color='positive' if advert.get('isAvailable') else 'negative'
                                ).props('rounded')
                        
                        ui.label(f"GHS {advert.get('price', 0):.2f}").classes("text-2xl font-bold text-green-600 flex-shrink-0")
                    
                    # Description
                    if advert.get('description'):
                        ui.label(advert.get('description')).classes("text-gray-600 line-clamp-2 text-sm")
                    
                    # Additional info
                    with ui.row().classes("items-center gap-4 text-sm text-gray-500 flex-wrap"):
                        if advert.get('preparationTime'):
                            with ui.row().classes("items-center gap-1"):
                                ui.icon('schedule', size='sm')
                                ui.label(f"{advert.get('preparationTime')} min")
                        if advert.get('ingredients'):
                            with ui.row().classes("items-center gap-1"):
                                ui.icon('list', size='sm')
                                ui.label(f"{len(advert.get('ingredients', '').split(','))} ingredients")
                        if advert.get('dietaryInformation'):
                            with ui.row().classes("items-center gap-1"):
                                ui.icon('nutrition', size='sm')
                                ui.label(advert.get('dietaryInformation'))
                    
                    # Action buttons
                    with ui.row().classes("w-full justify-end gap-2 mt-3"):
                        ui.button('Edit', on_click=lambda ad=advert: self.edit_advertisement(ad), icon='edit').props('outlined dense')
                        ui.button('View', on_click=lambda ad=advert: self.view_advertisement(ad), icon='visibility').props('outlined dense')
                        status_text = 'Deactivate' if advert.get('isAvailable') else 'Activate'
                        status_color = 'negative' if advert.get('isAvailable') else 'positive'
                        ui.button(status_text, on_click=lambda ad=advert: self.toggle_status(ad), icon='toggle_on' if advert.get('isAvailable') else 'toggle_off').props('outlined dense').classes(f'text-{status_color}')
    
    def edit_advertisement(self, advert: Dict[str, Any]):
        """Edit advertisement"""
        advert_id = advert.get('id')
        if advert_id:
            ui.navigate.to(f"/vendor/edit_advert/{advert_id}")
        else:
            ui.notify('Cannot edit advertisement: ID not found', type='warning')
    
    def view_advertisement(self, advert: Dict[str, Any]):
        """View advertisement details"""
        advert_id = advert.get('id')
        if advert_id:
            ui.navigate.to(f"/advertisement/{advert_id}")
        else:
            ui.notify('Cannot view advertisement: ID not found', type='warning')
    
    def toggle_status(self, advert: Dict[str, Any]):
        """Toggle advertisement status"""
        token = get_token()
        if not token:
            ui.notify('Please log in to update advertisement', type='warning')
            return
        
        new_status = not advert.get('isAvailable', False)
        advert_id = advert.get('id')
        
        if not advert_id:
            ui.notify('Cannot update advertisement: ID not found', type='warning')
            return
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.patch(
                f"{self.BACKEND_URL}/api/advertisements/{advert_id}",
                json={"isAvailable": new_status},
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                ui.notify(f'Advertisement {"activated" if new_status else "deactivated"} successfully', type='positive')
                # Update local state
                advert['isAvailable'] = new_status
                self.apply_filters()  # Re-apply filters to refresh view
            else:
                ui.notify('Failed to update advertisement status', type='negative')
                print(f"Update error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            ui.notify('Connection error. Please check your internet connection.', type='negative')
        except requests.exceptions.Timeout:
            ui.notify('Request timeout. Please try again.', type='negative')
        except Exception as e:
            ui.notify(f'Error updating status: {str(e)}', type='negative')
    
    def create_statistics_cards(self):
        """Create statistics cards"""
        total_ads = len(self.advertisements)
        active_ads = sum(1 for adv in self.advertisements if adv.get('isAvailable'))
        total_value = sum(adv.get('price', 0) for adv in self.advertisements if adv.get('isAvailable'))
        avg_price = total_value / active_ads if active_ads > 0 else 0
        
        with ui.grid(columns=4).classes("w-full gap-6 mb-8"):
            # Total advertisements
            with ui.card().classes("p-6 text-center bg-gradient-to-br from-blue-50 to-blue-100 border border-blue-200"):
                ui.icon('inventory_2', color='primary', size='xl').classes("mb-2")
                ui.label('Total Ads').classes("text-blue-700 font-medium")
                ui.label(str(total_ads)).classes("text-3xl font-bold text-blue-900")
            
            # Active advertisements
            with ui.card().classes("p-6 text-center bg-gradient-to-br from-green-50 to-green-100 border border-green-200"):
                ui.icon('check_circle', color='positive', size='xl').classes("mb-2")
                ui.label('Active Ads').classes("text-green-700 font-medium")
                ui.label(str(active_ads)).classes("text-3xl font-bold text-green-900")
            
            # Total value
            with ui.card().classes("p-6 text-center bg-gradient-to-br from-purple-50 to-purple-100 border border-purple-200"):
                ui.icon('attach_money', color='secondary', size='xl').classes("mb-2")
                ui.label('Total Value').classes("text-purple-700 font-medium")
                ui.label(f"GHS {total_value:.2f}").classes("text-3xl font-bold text-purple-900")
            
            # Average price
            with ui.card().classes("p-6 text-center bg-gradient-to-br from-orange-50 to-orange-100 border border-orange-200"):
                ui.icon('analytics', color='orange', size='xl').classes("mb-2")
                ui.label('Avg Price').classes("text-orange-700 font-medium")
                ui.label(f"GHS {avg_price:.2f}").classes("text-3xl font-bold text-orange-900")
    
    def render(self):
        """Render the dashboard"""
        if not require_vendor():
            return
        
        with ui.column().classes("w-full min-h-screen bg-gray-50"):
            with ui.row().classes("w-full h-full"):
                # Sidebar
                with ui.column().classes("bg-gray-800 text-white min-h-screen w-64"):
                    show_side_bar()
                
                # Main content
                with ui.column().classes("flex-1 p-8 overflow-auto"):
                    # Header
                    with ui.column().classes("w-full mb-8"):
                        ui.label('My Advertisement Dashboard').classes("text-4xl font-bold text-gray-800 mb-2")
                        ui.label('Manage and track your restaurant advertisements').classes("text-lg text-gray-600")
                    
                    # Statistics cards
                    self.create_statistics_cards()
                    
                    # Search and filter section
                    self.create_search_section()
                    
                    # Advertisement list
                    self.create_advertisement_list()
        
        # Load initial data
        self.load_advertisements()

@ui.page("/vendor/dashboard")
def vendor_dashboard_page():
    """Vendor dashboard page"""
    dashboard = VendorDashboard()
    dashboard.render()