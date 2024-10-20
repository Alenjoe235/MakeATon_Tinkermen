import flet as ft
import flet.map as map
import asyncio
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class PatrolBot:
    def __init__(self, api_key):
        genai.configure(api_key="AIzaSyA28ESjc0LhklwQ3M-F2KaLNOD9fZGpYLQ")
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.system_prompt = """
        You are PatrolBot, an AI assistant specialized in supporting law enforcement officers. Your role is to:

        1. Provide information about patrol strategies and best practices
        2. Answer questions about police procedures and protocols
        3. Assist with report writing and documentation
        4. Offer tactical suggestions for various situations
        5. Help with resource allocation and patrol planning
        6. Share relevant crime statistics and patterns
        7. Provide guidance on community policing approaches
        8. Assist with incident response planning

        Keep responses professional, clear, and concise. Always prioritize officer and public safety.
        Remember you are an AI assistant and should not make final decisions on critical matters.
        """
        self.chat.send_message(self.system_prompt)

    def get_response(self, user_input):
        response = self.chat.send_message(user_input)
        return response.text

def main(page: ft.Page):
    # Set initial page properties
    page.title = "Login Page"
    page.window_width = 1000
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#000000"

    def create_chat_interface(nav_rail):
        chat_area = ft.ListView(
            expand=True,
            spacing=10,
            auto_scroll=True,
            height=page.window_height - 100
        )

        def add_message(sender, message):
            chat_area.controls.append(
                ft.Container(
                    content=ft.Text(
                        f"{sender}: {message}",
                        color="white"
                    ),
                    bgcolor="#424242" if sender == "You" else "#1E1E1E",
                    border_radius=10,
                    padding=10,
                    width=300,
                    alignment=ft.alignment.center_right if sender == "You" else ft.alignment.center_left,
                )
            )
            page.update()

        api_key = os.getenv("GOOGLE_API_KEY_2")
        patrolbot = PatrolBot(api_key)

        def send_message(e):
            if not user_input.value:
                return
            user_message = user_input.value
            add_message("You", user_message)
            user_input.value = ""
            page.update()

            response = patrolbot.get_response(user_message)
            add_message("PatrolBot", response)

        user_input = ft.TextField(
            hint_text="Type your message here...",
            expand=True,
            on_submit=send_message,
            bgcolor="#323232",
            color="white",
            cursor_color="white"
        )

        send_button = ft.IconButton(
            icon=ft.icons.SEND,
            on_click=send_message,
            icon_color="white"
        )

        chat_column = ft.Column(
            controls=[
                ft.Text(
                    "PatrolBot : AI Assistant",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="white"
                ),
                chat_area,
                ft.Row(
                    controls=[user_input, send_button],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            ],
            expand=True,
            spacing=20
        )

        main_container = ft.Container(
            content=chat_column,
            padding=20,
            expand=True,
            bgcolor="#000000"
        )

        main_row = ft.Row(
            controls=[
                nav_rail,
                main_container
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )

        # Initial greeting
        add_message("PatrolBot", "Hello! I'm PatrolBot, your law enforcement assistant. How can I help you with your patrol duties today?")

        return main_row

    async def show_loading_screen():
        page.controls.clear()

        logo = ft.Image(
            src=r"C:\Users\jojithomas pta\Downloads\warrior-removebg.png",
            width=700,
            height=700,
        )

        loading_container = ft.Container(
            content=logo,
            alignment=ft.alignment.center,
            bgcolor="#000000",
            expand=True,
            animate_opacity=2000,
            opacity=0
        )

        page.add(loading_container)
        await page.update_async()

        loading_container.opacity = 1
        await page.update_async()
        await asyncio.sleep(2)
        loading_container.opacity = 0
        await page.update_async()
        await asyncio.sleep(3)
        show_login_page()

    def show_login_page():
        page.controls.clear()

        # Left side with logo
        logo = ft.Image(
            src=r"C:\Users\jojithomas pta\Downloads\warrior-removebg.png",
            width=700,
            height=700,
        )

        left_container = ft.Container(
            content=ft.Column(
                [logo],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#000000",  # Dark grey
            expand=True,
            alignment=ft.alignment.center,
        )

        # Right side with login form
        welcome_text = ft.Text(
            value="Welcome", 
            size=30, 
            weight="bold",
            color="white",
            text_align=ft.TextAlign.CENTER
        )

        username_field = ft.TextField(
            label="Username/Email:",
            width=300,
            bgcolor="#323232",
            color="white",
            label_style=ft.TextStyle(color="white"),
        )

        password_field = ft.TextField(
            label="Password:",
            password=True,
            can_reveal_password=True,
            width=300,
            bgcolor="#323232",
            color="white",
            label_style=ft.TextStyle(color="white"),
        )

        def login_clicked(e):
            print(f"Login clicked! Username: {username_field.value}, Password: {password_field.value}")
            show_home_page()

        login_button = ft.ElevatedButton(
            text="Login", 
            width=150, 
            on_click=login_clicked,
            color="white",
            bgcolor="#DD0009",
        )

        right_container = ft.Container(
            content=ft.Column(
                [
                    welcome_text,
                    ft.Container(height=20),
                    username_field,
                    ft.Container(height=10),
                    password_field,
                    ft.Container(height=20),
                    login_button,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#000000",  # Black
            expand=True,
            alignment=ft.alignment.center,
        )

        # Main row to hold both containers
        main_row = ft.Row(
            controls=[left_container, right_container],
            expand=True,
        )

        page.add(main_row)
        page.update()

    def show_home_page():
        nav_rail = create_navigation_rail()

        map_config = map.MapConfiguration(
            initial_center=map.MapLatitudeLongitude(37.7749, -122.4194),
            initial_zoom=15,
        )

        crime_heatmap = map.Map(
            expand=True, 
            configuration=map_config,
            layers=[
                map.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                )
            ]
        )

        main_row = ft.Row(
            controls=[
                nav_rail,
                crime_heatmap,
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )

        page.controls.clear()
        page.add(main_row)
        page.update()

    def create_navigation_rail():
        nav_rail = ft.NavigationRail(
            selected_index=0,
            on_change=navigate_to_page,
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.MAP, label="Crime Heatmap"),
                ft.NavigationRailDestination(icon=ft.icons.ADD_ALERT_SHARP, label="Crime Prediction Alerts"),
                ft.NavigationRailDestination(icon=ft.icons.CHAT, label="PatrolBot"),
                ft.NavigationRailDestination(icon=ft.icons.REPORT, label="Reports and Analytics"),
            ],
            bgcolor=ft.colors.GREY_900,
            group_alignment=0.0,
        )
        return nav_rail

    def navigate_to_page(e):
        if e.control.selected_index == 0:
            show_home_page()
        elif e.control.selected_index == 1:
            show_blank_page("Crime Prediction Alerts")
        elif e.control.selected_index == 2:
            show_patrol_bot()
        elif e.control.selected_index == 3:
            show_blank_page("Reports and Analytics")

    def show_patrol_bot():
        nav_rail = create_navigation_rail()
        chat_interface = create_chat_interface(nav_rail)
        
        page.controls.clear()
        page.add(chat_interface)
        page.update()

    def show_blank_page(title):
        nav_rail = create_navigation_rail()
        
        title_text = ft.Text(
            value=title,
            size=30,
            weight="bold",
            color="white",
            text_align=ft.TextAlign.CENTER
        )
        
        back_button = ft.ElevatedButton(
            text="Back to Home",
            on_click=lambda e: show_home_page(),
            bgcolor="#DD0009",
            color="white"
        )

        main_row = ft.Row(
           controls=[
               nav_rail,
               ft.Column(
                   controls=[title_text, back_button],
                   alignment=ft.MainAxisAlignment.CENTER
               ),
           ],
           alignment=ft.MainAxisAlignment.START,
           expand=True,
        )

        page.controls.clear()
        page.add(main_row)
        page.update()

    page.add(
        ft.Text("", opacity=0)
    )
    asyncio.run(show_loading_screen())

ft.app(target=main)