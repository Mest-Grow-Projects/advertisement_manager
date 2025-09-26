from nicegui import ui
from utils.auth import api_login, api_signup, set_session
from components.footer import show_footer


@ui.page('/sign-in')
def show_sign_in_page():
    with ui.element('div').style(
        "background-image: url('/assets/dishes-mediterranean-cuisine.jpg');"
        "background-size: cover;"
        "background-position: center;"
        "width: 100vw;"
        "height: 100vh;"
        "display: flex;"
        "justify-content: center;"
        "align-items: center;"
    ):
        with ui.card().classes('w-[600px] max-w-[90%] p-8 shadow-2xl rounded-2xl bg-white/95 backdrop-blur-lg'):
            ui.label('Welcome').classes('text-3xl font-extrabold text-center mb-2 text-green-700')
            ui.label('Sign in or create an account').classes('text-base text-center text-gray-600 mb-6')

            with ui.tabs().classes('w-full') as tabs:
                login_tab = ui.tab('Login')
                signup_tab = ui.tab('Sign Up')

            with ui.tab_panels(tabs, value=login_tab).classes('w-full mt-4'):
                # LOGIN TAB
                with ui.tab_panel(login_tab):
                    email = ui.input('Email').props('outlined dense').classes('w-full mb-4')
                    password = ui.input('Password').props('outlined dense type=password').classes('w-full mb-6')

                    def on_login():
                        if not email.value or not password.value:
                            ui.notify('Please enter email and password', type='warning')
                            return

                        # Show loading indicator
                        loading = ui.spinner(size='lg').classes('mt-4')
                        
                        try:
                            success, msg, token, user_id, role, name = api_login(email.value, password.value)
                            loading.visible = False

                            if not success:
                                ui.notify(msg, type='negative')
                                return

                            set_session(token=token, role=role, user_id=user_id, name=name)
                            ui.notify('Logged in successfully', type='positive')

                            if role == 'vendor':
                                ui.navigate.to('/vendor/dashboard')
                            else:
                                ui.navigate.to('/view_advert')
                        except Exception as e:
                            loading.visible = False
                            ui.notify(f'Login failed: {str(e)}', type='negative')

                    ui.button('Login', on_click=on_login).classes(
                        'w-full text-white rounded-lg'
                    ).style('background-color: #077d16 !important; hover:background-color: #065a11 !important;')

                # SIGN UP TAB
                with ui.tab_panel(signup_tab):
                    name = ui.input('Full Name').props('outlined dense').classes('w-full mb-4')
                    email_su = ui.input('Email').props('outlined dense').classes('w-full mb-4')
                    password_su = ui.input('Password').props('outlined dense type=password').classes('w-full mb-4')
                    role = ui.select(['user', 'vendor'], value='user', label='Role').props('outlined dense').classes('w-full mb-6')

                    def on_signup():
                        if not name.value or not email_su.value or not password_su.value or not role.value:
                            ui.notify('All fields are required', type='warning')
                            return

                        # Show loading indicator
                        loading = ui.spinner(size='lg').classes('mt-4')
                        
                        try:
                            success, msg, token, user_id = api_signup(name.value, email_su.value, password_su.value, role.value)
                            loading.visible = False

                            if not success:
                                ui.notify(msg, type='negative')
                                return

                            # Auto login after successful signup
                            set_session(token=token, role=role.value, user_id=user_id, name=name.value)
                            ui.notify('Account created successfully', type='positive')

                            if role.value == 'vendor':
                                ui.navigate.to('/vendor/dashboard')
                            else:
                                ui.navigate.to('/view_advert')
                        except Exception as e:
                            loading.visible = False
                            ui.notify(f'Signup failed: {str(e)}', type='negative')

                    ui.button('Create Account', on_click=on_signup).classes(
                        'w-full text-white rounded-lg'
                    ).style('background-color: #077d16 !important; hover:background-color: #065a11 !important;')

            # JavaScript to check URL and switch to signup tab if needed
            ui.run_javascript('''
                if (window.location.search.includes('tab=signup')) {
                    // Find the signup tab and click it
                    setTimeout(() => {
                        const tabs = document.querySelectorAll('[data-tab-name="Sign Up"]');
                        if (tabs.length > 0) {
                            tabs[0].click();
                        }
                    }, 100);
                }
            ''')

    # Add footer
    show_footer()
