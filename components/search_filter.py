# components/search_filter.py
from nicegui import ui
from typing import Dict, Any, List, Optional
import datetime

class SearchFilterComponent:
    """Reusable search and filter component for advertisements"""
    
    def __init__(self, on_search_callback=None, on_filter_callback=None):
        self.on_search_callback = on_search_callback
        self.on_filter_callback = on_filter_callback
        self.components: Dict[str, Any] = {}
        self.filters: Dict[str, Any] = {}
    
    def create_search_bar(self, placeholder="Search advertisements..."):
        """Create search input with debounced search"""
        with ui.row().classes("w-full items-center gap-4 mb-4"):
            # Search input
            self.components['search_input'] = ui.input(
                placeholder=placeholder,
                on_change=self._on_search_change
            ).props('outlined dense').classes("flex-1")
            
            # Search button
            ui.button('Search', on_click=self._trigger_search, icon='search').props('outlined')
            
            # Clear filters button
            ui.button('Clear', on_click=self._clear_filters, icon='clear').props('outlined')
    
    def create_advanced_filters(self, categories: List[str]):
        """Create advanced filter options"""
        with ui.expansion('Advanced Filters', icon='filter_list').classes("w-full mb-4"):
            with ui.grid(columns=2).classes("w-full gap-4 p-4"):
                # Category filter
                with ui.column().classes("space-y-2"):
                    ui.label('Category').classes("font-semibold")
                    self.components['category_filter'] = ui.select(
                        options=['All'] + categories,
                        value='All',
                        on_change=lambda e: self._update_filter('category', e.value if e.value != 'All' else None)
                    ).props('outlined dense').classes("w-full")
                
                # Price range filter
                with ui.column().classes("space-y-2"):
                    ui.label('Price Range (GHS)').classes("font-semibold")
                    with ui.row().classes("items-center gap-2 w-full"):
                        self.components['min_price'] = ui.number(
                            placeholder='Min',
                            min=0,
                            max=10000,
                            on_change=lambda: self._update_price_filter()
                        ).props('outlined dense').classes("flex-1")
                        ui.label('to').classes("text-gray-500")
                        self.components['max_price'] = ui.number(
                            placeholder='Max',
                            min=0,
                            max=10000,
                            on_change=lambda: self._update_price_filter()
                        ).props('outlined dense').classes("flex-1")
                
                # Dietary preferences
                with ui.column().classes("space-y-2"):
                    ui.label('Dietary').classes("font-semibold")
                    self.components['dietary_filter'] = ui.select(
                        options=['Any', 'Vegetarian', 'Vegan', 'Gluten-Free', 'Dairy-Free'],
                        value='Any',
                        on_change=lambda e: self._update_filter('dietary', e.value if e.value != 'Any' else None)
                    ).props('outlined dense').classes("w-full")
                
                # Spiciness level
                with ui.column().classes("space-y-2"):
                    ui.label('Spiciness').classes("font-semibold")
                    self.components['spiciness_filter'] = ui.select(
                        options=['Any', 'Not Spicy', 'Mild', 'Medium', 'Hot', 'Very Hot'],
                        value='Any',
                        on_change=lambda e: self._update_filter('spiciness', e.value if e.value != 'Any' else None)
                    ).props('outlined dense').classes("w-full")
    
    def _on_search_change(self, e):
        """Handle search input change with debounce"""
        self.filters['search'] = e.value
        self._trigger_search()
    
    def _update_filter(self, filter_type: str, value: Any):
        """Update specific filter"""
        if value:
            self.filters[filter_type] = value
        else:
            self.filters.pop(filter_type, None)
        self._trigger_filter()
    
    def _update_price_filter(self):
        """Update price range filter"""
        min_price = self.components['min_price'].value
        max_price = self.components['max_price'].value
        
        if min_price is not None or max_price is not None:
            self.filters['price_range'] = {
                'min': min_price,
                'max': max_price
            }
        else:
            self.filters.pop('price_range', None)
        
        self._trigger_filter()
    
    def _trigger_search(self):
        """Trigger search callback"""
        if self.on_search_callback:
            self.on_search_callback(self.filters.get('search', ''))
    
    def _trigger_filter(self):
        """Trigger filter callback"""
        if self.on_filter_callback:
            self.on_filter_callback(self.filters)
    
    def _clear_filters(self):
        """Clear all filters"""
        # Reset UI components
        for key, component in self.components.items():
            if hasattr(component, 'value'):
                if key == 'search_input':
                    component.value = ''
                elif key in ['category_filter', 'dietary_filter', 'spiciness_filter']:
                    component.value = 'All' if key == 'category_filter' else 'Any'
                elif key in ['min_price', 'max_price']:
                    component.value = None
        
        # Clear filters
        self.filters = {}
        
        # Trigger callbacks
        self._trigger_search()
        self._trigger_filter()
    
    def get_current_filters(self) -> Dict[str, Any]:
        """Get current filter state"""
        return self.filters.copy()