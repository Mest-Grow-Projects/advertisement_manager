from nicegui import ui
from components.footer import show_footer

def show_home_page():
    # Load Google Fonts and modern custom styles
    ui.add_head_html('''
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            html, body {
                margin: 0;
                padding: 0;
                height: 100%;
                width: 100%;
                overflow-x: hidden;
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                scroll-behavior: smooth;
            }
            
            .hero-section {
                min-height: 100vh;
                width: 100%;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #077d16 75%, #065a11 100%);
                position: relative;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }
            
            .hero-section::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="a" cx="50%" cy="50%"><stop offset="0%" stop-color="%23ffffff" stop-opacity="0.1"/><stop offset="100%" stop-color="%23ffffff" stop-opacity="0"/></radialGradient></defs><circle cx="200" cy="200" r="100" fill="url(%23a)"/><circle cx="800" cy="300" r="150" fill="url(%23a)"/><circle cx="400" cy="700" r="120" fill="url(%23a)"/></svg>');
                pointer-events: none;
            }
            
            .section-bg {
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
            }
            
            .glass-card {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
            }
            
            .card-hover {
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .card-hover:hover {
                transform: translateY(-12px) scale(1.02);
                box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.15);
            }
            
            .gradient-text {
                background: linear-gradient(135deg, #077d16, #10b981, #34d399);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .floating-animation {
                animation: float 6s ease-in-out infinite;
            }
            
            @keyframes float {
                0%, 100% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
            }
            
            .pulse-glow {
                animation: pulse-glow 2s ease-in-out infinite alternate;
            }
            
            @keyframes pulse-glow {
                from { box-shadow: 0 0 20px rgba(7, 125, 22, 0.3); }
                to { box-shadow: 0 0 40px rgba(7, 125, 22, 0.6); }
            }
            
            .modern-button {
                background: linear-gradient(135deg, #077d16, #10b981);
                border: none;
                position: relative;
                overflow: hidden;
            }
            
            .modern-button::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
                transition: left 0.5s;
            }
            
            .modern-button:hover::before {
                left: 100%;
            }
        </style>
    ''')

    # === HERO SECTION ===
    with ui.element("div").classes("hero-section w-full flex flex-col items-center justify-center text-center px-6 relative"):
        # Background carousel with multiple food images
        with ui.carousel(animated=True, arrows=True, navigation=True).classes("absolute inset-0 z-0").props('height=100%'):
            # Carousel images from Pixabay
            ui.image("https://cdn.pixabay.com/photo/2019/04/26/07/14/store-4156934_1280.jpg").classes("w-full h-full")
            ui.image("https://cdn.pixabay.com/photo/2017/12/09/08/18/pizza-3007395_1280.jpg").classes("w-full h-full object-cover")
            ui.image("https://cdn.pixabay.com/photo/2016/11/29/05/45/architecture-1867187_1280.jpg").classes("w-full h-full object-cover")
            ui.image("https://cdn.pixabay.com/photo/2017/01/26/02/06/platter-2009590_1280.jpg").classes("w-full h-full object-cover")
            ui.image("https://cdn.pixabay.com/photo/2018/07/14/15/27/cafe-3537801_1280.jpg").classes("w-full h-full object-cover")

        # Dark overlay for better text readability
        with ui.element("div").classes("absolute inset-0 bg-black bg-opacity-50 z-5"):
            pass
        
        with ui.column().classes("w-full max-w-5xl items-center relative z-10"):
            ui.label("BiteBridge").classes(
                "text-4xl md:text-6xl font-bold text-white mb-4 drop-shadow-2xl tracking-tight"
            ).style("font-family: 'Inter', sans-serif;")
            
            ui.label("Discover Amazing Restaurants & Delicious Food").classes(
                "text-lg md:text-2xl text-white mb-4 font-medium tracking-wide"
            )
            ui.label("Connect with the best restaurants in your area and explore mouth-watering dishes crafted by passionate chefs").classes(
                "text-base md:text-lg text-gray-200 mb-8 max-w-3xl leading-relaxed font-normal"
            )
            
            # Modern CTA Buttons
            with ui.row().classes("gap-6 flex-wrap justify-center"):
                ui.button("Explore Restaurants", on_click=lambda: ui.navigate.to('/view_advert')).classes(
                    "px-8 py-3 text-lg font-semibold text-white bg-gradient-to-r from-emerald-500 to-green-600 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 hover:from-emerald-600 hover:to-green-700"
                )
                ui.button("Join as Vendor", on_click=lambda: ui.navigate.to('/sign-in')).classes(
                    "px-8 py-3 text-lg font-bold text-white bg-gradient-to-r from-emerald-500 to-green-600 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 hover:from-emerald-600 hover:to-green-700"
                )

    # === FEATURES SECTION ===
    with ui.element("div").classes("section-bg w-full py-32 px-6"):
        with ui.column().classes("w-full max-w-7xl mx-auto"):
            with ui.element("div").classes("text-center mb-20 w-full flex flex-col items-center"):
                ui.label("Why Choose BiteBridge?").classes("text-3xl md:text-4xl font-black text-gray-900 mb-6 gradient-text text-center")
                ui.label("Your gateway to culinary excellence and seamless dining experiences").classes("text-lg md:text-xl text-gray-600 font-light max-w-3xl mx-auto leading-relaxed text-center")
            
            with ui.row().classes("w-full justify-center gap-10 flex-wrap"):
                # Feature 1 - Enhanced with glass effect
                with ui.card().classes("w-96 p-10 text-center card-hover glass-card rounded-3xl border-0"):
                    ui.label("Smart Discovery").classes("text-2xl font-bold text-gray-900 mb-6")
                    ui.label("AI-powered search that learns your preferences and suggests the perfect restaurants and dishes tailored just for you").classes("text-gray-700 leading-relaxed text-base")
                
                # Feature 2
                with ui.card().classes("w-96 p-10 text-center card-hover glass-card rounded-3xl border-0"):
                    ui.label("Quality Guaranteed").classes("text-2xl font-bold text-gray-900 mb-6")
                    ui.label("Every restaurant is personally verified by our team and continuously rated by our community for exceptional quality").classes("text-gray-700 leading-relaxed text-base")
                
                # Feature 3
                with ui.card().classes("w-96 p-10 text-center card-hover glass-card rounded-3xl border-0"):
                    ui.label("Vendor Success").classes("text-2xl font-bold text-gray-900 mb-6")
                    ui.label("Powerful tools for restaurant owners to showcase their cuisine, manage orders, and grow their business effortlessly").classes("text-gray-700 leading-relaxed text-base")

    # === POPULAR CATEGORIES ===
    with ui.element("div").classes("w-full py-24 px-6 bg-white"):
        with ui.column().classes("w-full max-w-6xl mx-auto"):
            with ui.element("div").classes("text-center mb-16 w-full flex flex-col items-center"):
                ui.label("Popular Categories").classes("text-2xl md:text-3xl font-bold text-gray-900 mb-4 text-center")
                ui.label("Discover culinary adventures across diverse cuisines and flavors").classes("text-base md:text-lg text-gray-600 font-normal max-w-2xl mx-auto leading-relaxed text-center")
            
            with ui.row().classes("w-full justify-center gap-8 flex-nowrap"):
                categories = [
                    {"name": "Fast Food", "image": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200&fit=crop&auto=format&q=80"},
                    {"name": "Asian", "image": "https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=300&h=200&fit=crop&auto=format&q=80"},
                    {"name": "Desserts", "image": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=300&h=200&fit=crop&auto=format&q=80"},
                    {"name": "Beverages", "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=300&h=200&fit=crop&auto=format&q=80"},
                    {"name": "Healthy", "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=300&h=200&fit=crop&auto=format&q=80"}
                ]
                
                for category in categories:
                    with ui.card().classes("flex-1 cursor-pointer card-hover bg-white rounded-2xl border border-gray-100 shadow-lg overflow-hidden min-w-0"):
                        ui.image(category["image"]).classes("w-full h-28 object-cover")
                        with ui.card_section().classes("p-3"):
                            ui.label(category["name"]).classes("text-base font-semibold text-gray-900 text-center")

    # === FEATURED RESTAURANTS ===
    with ui.element("div").classes("section-bg w-full py-32 px-6"):
        with ui.column().classes("w-full max-w-7xl mx-auto"):
            with ui.element("div").classes("text-center mb-20"):
                ui.label("Featured Restaurants").classes("text-5xl md:text-6xl font-black text-gray-900 mb-6")
                ui.label("Handpicked culinary gems loved by our community").classes("text-xl md:text-2xl text-gray-600 font-light max-w-3xl mx-auto leading-relaxed")
            
            with ui.row().classes("w-full justify-center gap-10 flex-wrap"):
                # Sample restaurants with enhanced styling
                restaurants = [
                    {
                        "name": "Mama's Kitchen",
                        "cuisine": "Italian Cuisine",
                        "rating": "4.8",
                        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500&h=400&fit=crop&auto=format&q=80",
                        "description": "Authentic Italian dishes crafted with traditional recipes and the finest ingredients"
                    },
                    {
                        "name": "Spice Garden",
                        "cuisine": "Asian Fusion",
                        "rating": "4.9",
                        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500&h=400&fit=crop&auto=format&q=80",
                        "description": "Bold flavors and innovative dishes that blend the best of Asian culinary traditions"
                    },
                    {
                        "name": "Green Bowl",
                        "cuisine": "Healthy Food",
                        "rating": "4.7",
                        "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=500&h=400&fit=crop&auto=format&q=80",
                        "description": "Fresh, organic, and nutritious meals that nourish your body and delight your taste buds"
                    }
                ]
                
                for restaurant in restaurants:
                    with ui.card().classes("w-96 card-hover glass-card overflow-hidden rounded-3xl border-0 shadow-2xl"):
                        ui.image(restaurant["image"]).classes("w-full h-64 object-cover")
                        with ui.card_section().classes("p-8"):
                            ui.label(restaurant["name"]).classes("text-2xl font-bold text-gray-900 mb-3")
                            ui.label(restaurant["cuisine"]).classes("text-green-600 font-semibold mb-4 text-lg")
                            with ui.row().classes("items-center gap-3 mb-4"):
                                ui.label("⭐").classes("text-yellow-500 text-xl")
                                ui.label(restaurant["rating"]).classes("font-bold text-gray-800 text-lg")
                                ui.label("• Excellent").classes("text-gray-600 font-medium")
                            ui.label(restaurant["description"]).classes("text-gray-700 leading-relaxed")

    # === STATS SECTION ===
    with ui.element("div").classes("w-full py-20 px-6 bg-gradient-to-br from-slate-900 via-green-900 to-emerald-900 text-white"):
        with ui.column().classes("w-full max-w-4xl mx-auto"):
            ui.label("BiteBridge by the Numbers").classes("text-2xl md:text-3xl font-bold text-center mb-12")
            
            with ui.row().classes("w-full justify-center gap-8 flex-nowrap"):
                stats = [
                    {"number": "500+", "label": "Restaurants"},
                    {"number": "10K+", "label": "Customers"},
                    {"number": "4.9★", "label": "Rating"}
                ]
                
                for stat in stats:
                    with ui.column().classes("items-center bg-white bg-opacity-95 p-6 rounded-2xl flex-1 min-w-0 shadow-lg"):
                        ui.label(stat["number"]).classes("text-3xl font-bold mb-2 text-black")
                        ui.label(stat["label"]).classes("text-sm text-gray-700 font-medium")

    # === CTA SECTION ===
    with ui.element("div").classes("w-full py-20 px-6 bg-gradient-to-r from-green-600 via-emerald-600 to-teal-600 text-white text-center relative overflow-hidden"):
        with ui.column().classes("w-full max-w-3xl mx-auto relative z-10"):
            with ui.element("div").classes("w-full flex flex-col items-center"):
                ui.label("Ready to Get Started?").classes("text-3xl md:text-4xl font-bold mb-6 text-center")
                ui.label("Join thousands of food lovers and restaurant owners creating amazing culinary experiences on BiteBridge").classes("text-base md:text-lg mb-10 text-green-100 font-normal max-w-2xl mx-auto leading-relaxed text-center")
            
            with ui.element("div").classes("w-full flex justify-center"):
                with ui.row().classes("gap-6 flex-wrap"):
                    ui.button("Browse Restaurants", on_click=lambda: ui.navigate.to('/view_advert')).classes(
                        "px-8 py-3 text-lg font-semibold text-white bg-gradient-to-r from-emerald-500 to-green-600 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 hover:from-emerald-600 hover:to-green-700"
                    )
                    ui.button("Start Selling", on_click=lambda: ui.navigate.to('/sign-in')).classes(
                        "px-8 py-3 text-lg font-bold text-white bg-gradient-to-r from-emerald-500 to-green-600 rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105 hover:from-emerald-600 hover:to-green-700"
                    )

    # === FOOTER ===
    show_footer()