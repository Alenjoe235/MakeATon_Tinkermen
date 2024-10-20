import flet as ft
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class MentalHealthChatbot:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])
        self.system_prompt = """
        You are a compassionate and professional mental health counselor. Your role is to provide supportive, 
        empathetic responses to users seeking mental health support. Follow these guidelines:

        1. Always maintain a calm, non-judgmental tone.
        2. Use active listening techniques, reflecting back what the user has said.
        3. Offer gentle encouragement and validation of the user's feelings.
        4. Suggest healthy coping strategies when appropriate.
        5. Encourage the user to seek professional help if their issues seem severe.
        6. Never diagnose or prescribe medication.
        7. If the user expresses thoughts of self-harm or suicide, immediately provide crisis hotline information.
        8. Maintain appropriate boundaries - remind the user that you are an AI if they seem to forget.
        9. Keep responses concise (2-3 sentences) unless more detail is necessary.
        10. End each response with a gentle, open-ended question to encourage further discussion.

        Remember, your primary goal is to provide a supportive listening ear and guide users towards 
        professional help when needed.
        """
        self.chat.send_message(self.system_prompt)

    def get_response(self, user_input):
        response = self.chat.send_message(user_input)
        return response.text

def main(page: ft.Page):
    page.title = "Mental Health Chatbot"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 400
    page.window.height = 700
    page.window.resizable = False
    page.bgcolor = "#101010"  # Very dark red background

    api_key = os.getenv("GOOGLE_API_KEY_2")
    chatbot = MentalHealthChatbot(api_key)

    chat_area = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True
    )

    def add_message(sender, message):
        new_message = ft.Container(
            content=ft.Text(f"{sender}: {message}", color="#FFD6D6"),  # Light pink text
            bgcolor="#4A0E0E" if sender == "You" else "#2D0A0A",  # Dark red for user, darker red for counselor
            border_radius=10,
            padding=10,
            width=300,
            alignment=ft.alignment.center_right if sender == "You" else ft.alignment.center_left,
        )
        chat_area.controls.append(new_message)
        page.update()

    def send_message(e):
        if not user_input.value:
            return
        user_message = user_input.value
        add_message("You", user_message)
        user_input.value = ""
        page.update()

        response = chatbot.get_response(user_message)
        add_message("Counselor", response)

    user_input = ft.TextField(
        hint_text="Type your message here...",
        border_color="#8B0000",  # Dark red border
        cursor_color="#8B0000",  # Light pink cursor
        color="#101010",  # Light pink text
        bgcolor="#F0F0F0",  # Dark background
        expand=True,
        on_submit=send_message
    )

    send_button = ft.IconButton(
        icon=ft.icons.SEND,
        icon_color="#FFD6D6",  # Light pink icon
        on_click=send_message
    )

    title = ft.Text(
        "Mental Health Chatbot",
        size=24,
        weight=ft.FontWeight.BOLD,
        color="#FFFFF0",  # Light pink title
    )

    page.add(
        title,
        chat_area,
        ft.Row([user_input, send_button])
    )

    # Initial greeting
    add_message("Counselor", "Hello! I'm here to provide support and listen. How are you feeling today?")

ft.app(target=main)