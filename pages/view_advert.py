from nicegui import ui
import requests
from utils.api import base_url
from components.footer import show_footer
from utils.auth import get_role, get_user_id, get_token

# AI Search Engine Class
class AISearchEngine:
    def __init__(self):
        self.synonyms = {
            'cheap': ['affordable', 'budget', 'inexpensive'],
            'expensive': ['pricey', 'costly', 'high end'],
            'quick': ['fast', 'speedy'],
            'romantic': ['intimate', 'cozy'],
            'family': ['kids', 'children'],
        }
        
        self.price_ranges = {
            'cheap': (0, 15),
            'affordable': (10, 25),
            'moderate': (20, 40),
            'expensive': (35, 1000),
        }
    
    def expand_query(self, query):
        if not query or len(query.strip()) < 2:
            return [query.lower()] if query else ['']
        
        query = query.lower().strip()
        expanded_queries = [query]
        
        for term, synonyms in self.synonyms.items():
            if term in query:
                for synonym in synonyms:
                    new_query = query.replace(term, synonym)
                    expanded_queries.append(new_query)
        
        return list(set(expanded_queries))
    
    def intelligent_search(self, query, adverts):
        if not query or len(query.strip()) < 2:
            return adverts
        
        original_query = query.lower().strip()
        expanded_queries = self.expand_query(original_query)
        
        scored_results = []
        
        for advert in adverts:
            score = 0
            advert_text = f"{advert.get('name', '')} {advert.get('description', '')}".lower()
            
            if original_query in advert_text:
                score += 10
            
            for expanded_query in expanded_queries:
                if expanded_query in advert_text:
                    score += 5
            
            query_words = set(original_query.split())
            advert_words = set(advert_text.split())
            common_words = query_words.intersection(advert_words)
            score += len(common_words) * 2
            
            if score > 0:
                scored_results.append((score, advert))
        
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [result[1] for result in scored_results]

def show_view_advert_page():
    try:
        response = requests.get(f"{base_url}/food/all", timeout=15)
        if 200 <= response.status_code < 300:
            json_data = response.json()
            restaurants = json_data.get("data", [])
        else:
            ui.notify('Failed to load adverts', type='negative')
            restaurants = []
    except Exception as e:
        ui.notify(f'Error loading adverts: {e}', type='negative')
        restaurants = []

    # Green themed page header
    with ui.column().classes('w-full items-center mb-6'):
        ui.label("🍽️ Discover Restaurants").classes("text-3xl font-bold text-green-800 mb-2")
        ui.label("Find your perfect dining experience").classes("text-lg text-green-600")

    # Initialize AI search engine
    ai_engine = AISearchEngine()

    # Define functions first
    def render_cards():
        results_container.clear()
        query = (search_box.value or "").lower()
        min_val = min_price.value or 0
        max_val = max_price.value or 1000
        
        # Use AI search for meaningful queries
        if query.strip() and len(query.strip()) > 1:
            filtered = ai_engine.intelligent_search(query, restaurants)
            search_info.text = f"🤖 Found {len(filtered)} results for '{query}'"
        else:
            filtered = restaurants
            search_info.text = f"🍴 Showing all {len(filtered)} restaurants"
        
        # Apply price filter
        final_filtered = []
        for r in filtered:
            price = r.get('price', 0)
            if min_val <= price <= max_val:
                final_filtered.append(r)
        
        if not final_filtered:
            with results_container:
                with ui.column().classes('w-full text-center py-12 items-center'):
                    ui.icon('search_off', size='xl', color='green').classes('text-green-400 mb-4')
                    ui.label("No restaurants match your search").classes("text-xl text-green-700 font-semibold mb-2")
                    ui.label("Try adjusting your search terms or price range").classes("text-green-600 mb-4")
                    ui.button("Reset Filters", on_click=reset_filters, icon='refresh') \
                     .props('outlined') \
                     .classes('bg-green-500 text-white hover:bg-green-600')
            return
        
        for r in final_filtered:
            with results_container:
                with ui.card().classes("w-80 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200 shadow-lg hover:shadow-xl hover:border-green-300 transition-all duration-300 transform hover:-translate-y-1 rounded-2xl p-4"):
                    # Image section
                    if r.get("image"):
                        ui.image(r["image"]).classes("rounded-xl h-40 w-full object-cover mb-4 shadow-md")
                    else:
                        with ui.element('div').classes('h-40 w-full bg-gradient-to-br from-green-200 to-emerald-300 rounded-xl flex items-center justify-center mb-4 shadow-md'):
                            ui.icon('restaurant', size='xl', color='white')
                    
                    # Content section
                    with ui.column().classes('w-full'):
                        # Name and price row
                        with ui.row().classes('w-full justify-between items-start mb-2'):
                            ui.label(r["name"]).classes("text-xl font-bold text-green-900 truncate flex-1")
                            ui.label(f"${r.get('price', 'N/A')}").classes("text-2xl font-bold text-green-600 bg-green-100 px-3 py-1 rounded-full")
                        
                        # Description
                        desc = r["description"][:80] + "..." if len(r.get("description", "")) > 80 else r.get("description", "")
                        ui.label(desc).classes("text-green-700 text-sm mb-4 leading-relaxed")
                        
                        # View Details button
                        ui.button("View Details", on_click=lambda advert=r: show_advert_modal(advert), icon='visibility') \
                         .classes("w-full bg-gradient-to-r from-green-500 to-emerald-500 text-white font-semibold py-3 rounded-xl hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg") \
                         .props('unelevated')

    def set_search(suggestion):
        search_box.value = suggestion
        render_cards()

    def reset_filters():
        search_box.value = ""
        min_price.value = 0
        max_price.value = 100
        render_cards()

    # Green themed search and filter section
    with ui.card().classes("w-full mb-8 bg-gradient-to-r from-green-50 to-emerald-100 border-2 border-green-200 rounded-2xl shadow-xl"):
        with ui.column().classes('w-full p-6'):
            # Search header
            with ui.row().classes('w-full items-center justify-between mb-4'):
                with ui.row().classes('items-center gap-3'):
                    ui.icon('search', color='green', size='lg')
                    ui.label('Smart Restaurant Search').classes('text-2xl font-bold text-green-900')
                ui.badge('AI Powered', color='positive').props('outline')
            
            # Search input with green styling
            search_box = ui.input(placeholder="🔍 Try: 'cheap pizza', 'romantic dinner', 'family places'...") \
                .props("outlined dense clearable rounded item-aligned bg-white") \
                .classes("w-full mb-4 border-green-300 focus:border-green-500")
            
            # Quick suggestions with green buttons
            with ui.column().classes('w-full mb-4'):
                ui.label('💡 Quick Suggestions:').classes('text-green-800 font-medium mb-2')
                with ui.row().classes('w-full gap-2 flex-wrap'):
                    suggestions = ['💰 Budget meals', '💕 Romantic', '👨‍👩‍👧‍👦 Family friendly', '⚡ Quick lunch', '🌱 Vegetarian']
                    for suggestion in suggestions:
                        ui.button(suggestion, on_click=lambda s=suggestion.split(' ')[1]: set_search(s)) \
                         .props('flat dense') \
                         .classes('bg-green-200 text-green-800 hover:bg-green-300 px-3 py-2 rounded-full font-medium')
            
            # Price filter section
            with ui.card().classes('w-full bg-white border-green-200 rounded-xl p-4'):
                ui.label('💰 Price Range Filter').classes('text-green-800 font-semibold mb-3')
                with ui.row().classes('w-full items-center justify-between gap-4'):
                    with ui.column().classes('items-center'):
                        ui.label('Min Price').classes('text-green-700 text-sm font-medium')
                        min_price = ui.number(value=0, min=0, max=1000) \
                         .props('outlined dense') \
                         .classes('w-24 border-green-300 text-green-800')
                    
                    ui.icon('arrow_forward', color='green')
                    
                    with ui.column().classes('items-center'):
                        ui.label('Max Price').classes('text-green-700 text-sm font-medium')
                        max_price = ui.number(value=100, min=0, max=1000) \
                         .props('outlined dense') \
                         .classes('w-24 border-green-300 text-green-800')
                    
                    ui.button("Reset Filters", on_click=reset_filters, icon='autorenew') \
                     .props('outlined') \
                     .classes('bg-white text-green-600 border-green-400 hover:bg-green-50')

    # Search info with green styling
    search_info = ui.label().classes('text-green-700 text-center w-full mb-6 text-lg font-medium')

    # Results container
    results_container = ui.row().classes("justify-center gap-8 flex-wrap")

    def show_advert_modal(advert):
        current_role = get_role()
        current_user_id = get_user_id()
        
        with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl bg-gradient-to-br from-green-50 to-emerald-100 border-2 border-green-200 rounded-2xl shadow-2xl'):
            # Header with gradient background
            with ui.column().classes('w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white p-6 rounded-t-2xl'):
                with ui.row().classes('w-full items-center justify-between'):
                    ui.label(advert.get('name', 'Untitled')).classes('text-2xl font-bold text-white')
                    ui.button(icon='close', on_click=dialog.close).props('flat round dense color="white"')
                
                # Quick info bar
                with ui.row().classes('w-full items-center gap-4 mt-2 flex-wrap'):
                    ui.label(f"${advert.get('price', 'N/A')}").classes('text-xl font-bold bg-white/20 px-4 py-2 rounded-full')
                    if advert.get('category'):
                        ui.label(advert['category']).classes('bg-white/20 px-4 py-2 rounded-full text-sm')
            
            # Main content
            with ui.scroll_area().classes('w-full h-full max-h-[70vh] p-6'):
                with ui.grid(columns=1).classes('w-full gap-6 lg:grid-cols-3'):
                    # Left column - Main details
                    with ui.column().classes('lg:col-span-2 space-y-4'):
                        # Image
                        if advert.get('image'):
                            ui.image(advert['image']).classes('w-full h-64 object-cover rounded-xl shadow-lg')
                        else:
                            with ui.element('div').classes('w-full h-64 bg-gradient-to-br from-green-200 to-emerald-300 rounded-xl flex items-center justify-center'):
                                ui.icon('restaurant', size='xl', color='white')
                        
                        # Description card
                        with ui.card().classes('w-full bg-white border-green-200 p-6 rounded-xl shadow-sm'):
                            ui.label('📖 Description').classes('font-semibold text-lg text-green-800 mb-3')
                            ui.label(advert.get('description', 'No description available')).classes('text-green-700 leading-relaxed')
                    
                    # Right column - Related adverts
                    with ui.column().classes('space-y-4'):
                        ui.label('💫 You Might Also Like').classes('font-semibold text-lg text-green-800 border-b-2 border-green-200 pb-2')
                        
                        related = get_related_adverts(advert)
                        if related:
                            for related_advert in related:
                                with ui.card().classes('p-4 bg-white border-green-200 hover:border-green-400 hover:shadow-lg transition-all cursor-pointer group rounded-xl') \
                                 .on('click', lambda ad=related_advert: (dialog.close(), show_advert_modal(ad))):
                                    
                                    with ui.row().classes('items-center gap-3'):
                                        if related_advert.get('image'):
                                            ui.image(related_advert['image']).classes('w-16 h-16 object-cover rounded-lg')
                                        else:
                                            with ui.element('div').classes('w-16 h-16 bg-green-200 rounded-lg flex items-center justify-center'):
                                                ui.icon('fastfood', color='green')
                                        
                                        with ui.column().classes('flex-grow'):
                                            ui.label(related_advert.get('name', 'Untitled')).classes('font-semibold text-green-900 group-hover:text-green-600')
                                            ui.label(f"${related_advert.get('price', 'N/A')}").classes('text-green-600 font-bold')
                                    
                                    ui.button("View Details", icon='visibility') \
                                     .props('flat dense') \
                                     .classes('w-full mt-2 text-green-600 hover:bg-green-50')
                        else:
                            ui.label('✨ More options coming soon!').classes('text-green-600 text-center py-4')
            
            # Action buttons with green styling
            with ui.row().classes('w-full justify-between items-center p-4 border-t border-green-200 bg-white rounded-b-2xl'):
                with ui.row().classes('items-center gap-2'):
                    ui.button('💖 Save', icon='favorite', on_click=lambda: ui.notify('Saved to favorites!', type='positive')) \
                     .props('outlined') \
                     .classes('text-green-600 border-green-400 hover:bg-green-50')
                    
                    ui.button('📤 Share', icon='share', on_click=lambda: ui.notify('Share link copied!', type='positive')) \
                     .props('outlined') \
                     .classes('text-green-600 border-green-400 hover:bg-green-50')
                
                with ui.row().classes('items-center gap-2'):
                    if current_role == 'vendor':
                        ui.button('✏️ Edit', icon='edit', on_click=lambda: (
                            dialog.close(),
                            ui.navigate.to(f"/vendor/edit_advert/{advert.get('id')}")
                        )).props('outlined color="positive"').classes('px-4')
                        
                        # Delete button
                        def confirm_delete():
                            with ui.dialog() as confirm_dialog, ui.card().classes('w-full max-w-sm bg-white border-2 border-green-200 rounded-2xl p-4'):
                                ui.label('🗑️ Confirm Delete').classes('text-lg font-bold text-green-800 mb-3')
                                ui.label(f'Delete "{advert.get("name", "this advert")}"?').classes('text-green-700 mb-2')
                                ui.label('This action cannot be undone.').classes('text-red-600 text-sm mb-4')
                                
                                with ui.row().classes('w-full justify-end gap-2'):
                                    ui.button('Cancel', on_click=confirm_dialog.close, icon='cancel') \
                                     .props('outlined') \
                                     .classes('text-green-600 border-green-400')
                                    
                                    def delete_advert():
                                        token = get_token()
                                        headers = {"Authorization": f"Bearer {token}"} if token else {}
                                        try:
                                            resp = requests.delete(f"{base_url}/food/{advert.get('id')}", headers=headers, timeout=15)
                                            if 200 <= resp.status_code < 300:
                                                ui.notify('✅ Advert deleted successfully', type='positive')
                                                confirm_dialog.close()
                                                dialog.close()
                                                render_cards()
                                            else:
                                                ui.notify(f"❌ Delete failed: {resp.text}", type='negative')
                                        except Exception as e:
                                            ui.notify(f"❌ Delete error: {e}", type='negative')
                                    
                                    ui.button('Delete', on_click=delete_advert, icon='delete') \
                                     .props('flat') \
                                     .classes('bg-red-500 text-white hover:bg-red-600')
                            
                            confirm_dialog.open()
                        
                        ui.button('🗑️ Delete', on_click=confirm_delete, icon='delete') \
                         .props('outlined') \
                         .classes('text-red-600 border-red-400 hover:bg-red-50')
                    
                    ui.button('Close', on_click=dialog.close, icon='close') \
                     .props('outlined') \
                     .classes('text-green-600 border-green-400 hover:bg-green-50')
        
        dialog.open()

    def get_related_adverts(current_advert, count=3):
        current_price = current_advert.get('price', 0)
        current_category = current_advert.get('category', 'General')
        
        related = []
        for r in restaurants:
            if r.get('id') == current_advert.get('id'):
                continue
                
            score = 0
            if r.get('category') == current_category:
                score += 2
            
            price_diff = abs(r.get('price', 0) - current_price)
            if price_diff <= 5:
                score += 2
            elif price_diff <= 15:
                score += 1
                
            if score > 0:
                related.append((score, r))
        
        related.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in related[:count]]

    # Initial render
    render_cards()

    # Event handlers
    search_box.on('input', lambda e: render_cards())
    min_price.on('change', lambda: render_cards())
    max_price.on('change', lambda: render_cards())
    
    # Add green themed footer
    show_footer()

    # Add green themed CSS
    ui.add_head_html('''
    <style>
        .green-gradient-bg {
            background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        }
        .green-card-hover {
            transition: all 0.3s ease;
        }
        .green-card-hover:hover {
            transform: translateY(-2px);
            box-shadow: 0 20px 25px -5px rgba(16, 185, 129, 0.1), 0 10px 10px -5px rgba(16, 185, 129, 0.04);
        }
    </style>
    ''')