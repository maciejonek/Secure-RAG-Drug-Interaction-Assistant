import reflex as rx
from app.pages.auth import login_page, register_page
from app.pages.chat import chat_page
from app.states.auth_state import AuthState

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap",
            rel="stylesheet",
        ),
    ],
    stylesheets=["/animations.css"],
)
app.add_page(login_page, route="/")
app.add_page(register_page, route="/register")
app.add_page(chat_page, route="/chat", on_load=AuthState.check_login)