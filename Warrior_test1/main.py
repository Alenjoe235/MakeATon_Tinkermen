import flet as ft

def main(page: ft.Page):
    # Set initial page properties
    page.title = "Login Page"
    page.window_width = 800
    page.window_height = 600
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#000000"  # Set background color to black

    # Function to display the login page
    def show_login_page():
        page.controls.clear()

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
        )

        password_field = ft.TextField(
            label="Password:",
            password=True,
            can_reveal_password=True,
            width=300,
            bgcolor="#323232",
            color="white",
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

        page.add(
            welcome_text,
            username_field,
            password_field,
            ft.Container(height=20),
            login_button
        )
        
        page.update()

    # Function to display the home page with WebView
    def show_home_page():
        nav_rail = create_navigation_rail()  # Create navigation rail

        # Create WebView to display the local HTML file using 'url'
        web_view = ft.WebView(
            url="file:///C:/Users/jojithomas%20pta/Pictures/crime_heatmap_estimated.html", 
            expand=True,  # Make it expand to fill available space
        )

        # Create content area with WebView and navigation rail
        main_row = ft.Row(
            controls=[
                nav_rail,
                web_view,
            ],
            alignment=ft.MainAxisAlignment.START,
            expand=True,
        )

        # Clear previous controls and add the main row with WebView
        page.controls.clear()
        page.add(main_row)

        # Update the page to reflect changes
        page.update()

    # Function to create the navigation rail with a logo
    def create_navigation_rail():
        logo_image = ft.Image(
            src=r"C:\Users\jojithomas pta\Downloads\WhatsApp_Image_2024-10-19_at_15.00.36_6d158b36-removebg-preview.png",  # Update this path to your logo file
            width=50,  # Set desired width for the logo
            height=50,  # Set desired height for the logo
            fit=ft.ImageFit.CONTAIN,
        )

        nav_rail = ft.NavigationRail(
            leading=logo_image,  # Add logo as leading widget
            selected_index=0,
            on_change=navigate_to_page,  # Update to use a single function for navigation
            destinations=[
                ft.NavigationRailDestination(icon=ft.icons.MAP, label="Crime Heatmap"),
                ft.NavigationRailDestination(icon=ft.icons.ADD_ALERT_SHARP, label="Crime Prediction Alerts"),
                ft.NavigationRailDestination(icon=ft.icons.PERSON, label="Officer Allocation"),
                ft.NavigationRailDestination(icon=ft.icons.REPORT, label="Reports and Analytics"),
            ],
            bgcolor=ft.colors.GREY_900,
            group_alignment=0.0,
        )
        
        return nav_rail

    # Function to navigate to different pages based on selection
    def navigate_to_page(e):
        if e.control.selected_index == 0:
            show_home_page()  # Show Crime Heatmap (WebView)
        
        elif e.control.selected_index == 1:
            show_blank_page("Crime Prediction Alerts")
        
        elif e.control.selected_index == 2:
            show_blank_page("Officer Allocation")
        
        elif e.control.selected_index == 3:
            show_blank_page("Reports and Analytics")

    # Function to display a blank page with a title while keeping the navigation bar intact
    def show_blank_page(title):
        nav_rail = create_navigation_rail()  # Keep the navigation rail intact
        
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

        # Clear previous controls and add title and back button along with navigation rail
        main_row = ft.Row(
           controls=[
               nav_rail,
               ft.Column(controls=[title_text, back_button], alignment=ft.MainAxisAlignment.CENTER),
           ],
           alignment=ft.MainAxisAlignment.START,
           expand=True,
       )
        page.controls.clear()  # Clear previous controls before adding new ones
        page.add(main_row)     # Add the new main row with navigation rail and content

    page.update()          # Update the page to reflect changes
    
    # Show the login page initially
    show_login_page()

# Launch the Flet app with the main function as target
ft.app(target=main)