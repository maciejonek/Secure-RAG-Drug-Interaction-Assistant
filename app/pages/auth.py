import reflex as rx
from app.states.auth_state import AuthState
from app.states.chat_state import ChatState
from app.components.layout_components import app_bar, md3_card, form_field
from app.utils.md3_styles import (
    TYPO_HEADLINE_LARGE,
    TYPO_BODY_MEDIUM,
    md3_button_styles,
    BACKGROUND_DARK,
    BACKGROUND_COLOR,
    TEXT_DARK_HIGH,
    TEXT_LIGHT_HIGH,
    TEXT_DARK_MEDIUM,
    TEXT_LIGHT_MEDIUM,
    PRIMARY_COLOR,
)


def login_page() -> rx.Component:
    return rx.el.div(
        app_bar("Medical RAG - Login"),
        rx.el.div(
            md3_card(
                [
                    rx.el.div(
                        rx.el.h2(
                            "Welcome Back",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"{TYPO_HEADLINE_LARGE} {TEXT_DARK_HIGH} mb-2 text-center",
                                f"{TYPO_HEADLINE_LARGE} {TEXT_LIGHT_HIGH} mb-2 text-center",
                            ),
                        ),
                        rx.el.p(
                            "Sign in to access medical insights",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"{TYPO_BODY_MEDIUM} {TEXT_DARK_MEDIUM} mb-8 text-center",
                                f"{TYPO_BODY_MEDIUM} {TEXT_LIGHT_MEDIUM} mb-8 text-center",
                            ),
                        ),
                        rx.cond(
                            AuthState.auth_error != "",
                            rx.el.div(
                                rx.icon(
                                    "badge_alert", class_name="text-white mr-2", size=18
                                ),
                                rx.el.span(AuthState.auth_error),
                                class_name="bg-[#B00020] text-white px-4 py-3 rounded-lg mb-6 flex items-center text-sm",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.form(
                            form_field(
                                "Username",
                                "Enter your username",
                                AuthState.username,
                                AuthState.set_username,
                            ),
                            form_field(
                                "Password",
                                "Enter your password",
                                AuthState.password,
                                AuthState.set_password,
                                type_="password",
                            ),
                            rx.el.button(
                                "Sign In",
                                type="submit",
                                class_name=f"w-full mt-4 {md3_button_styles(True)}",
                            ),
                            on_submit=AuthState.login,
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Don't have an account? ",
                                class_name=rx.cond(
                                    ChatState.dark_mode,
                                    "text-gray-300",
                                    "text-gray-600",
                                ),
                            ),
                            rx.el.a(
                                "Register",
                                href="/register",
                                class_name=f"text-[{PRIMARY_COLOR}] font-semibold hover:underline cursor-pointer",
                            ),
                            class_name=f"mt-6 text-center {TYPO_BODY_MEDIUM}",
                        ),
                    )
                ],
                class_name="w-full max-w-md p-10 m-4",
            ),
            class_name=rx.cond(
                ChatState.dark_mode,
                f"flex-1 flex items-center justify-center w-full bg-[{BACKGROUND_DARK}]",
                f"flex-1 flex items-center justify-center w-full bg-[{BACKGROUND_COLOR}]",
            ),
        ),
        class_name="min-h-screen flex flex-col font-['Open_Sans']",
    )


def register_page() -> rx.Component:
    return rx.el.div(
        app_bar("Medical RAG - Register"),
        rx.el.div(
            md3_card(
                [
                    rx.el.div(
                        rx.el.h2(
                            "Create Account",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"{TYPO_HEADLINE_LARGE} {TEXT_DARK_HIGH} mb-2 text-center",
                                f"{TYPO_HEADLINE_LARGE} {TEXT_LIGHT_HIGH} mb-2 text-center",
                            ),
                        ),
                        rx.el.p(
                            "Join to consult our medical agent",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"{TYPO_BODY_MEDIUM} {TEXT_DARK_MEDIUM} mb-8 text-center",
                                f"{TYPO_BODY_MEDIUM} {TEXT_LIGHT_MEDIUM} mb-8 text-center",
                            ),
                        ),
                        rx.cond(
                            AuthState.auth_error != "",
                            rx.el.div(
                                rx.icon(
                                    "badge_alert", class_name="text-white mr-2", size=18
                                ),
                                rx.el.span(AuthState.auth_error),
                                class_name="bg-[#B00020] text-white px-4 py-3 rounded-lg mb-6 flex items-center text-sm",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.form(
                            form_field(
                                "Username",
                                "Choose a username",
                                AuthState.username,
                                AuthState.set_username,
                            ),
                            form_field(
                                "Password",
                                "Choose a password (min 6 chars)",
                                AuthState.password,
                                AuthState.set_password,
                                type_="password",
                            ),
                            form_field(
                                "Confirm Password",
                                "Re-enter password",
                                AuthState.confirm_password,
                                AuthState.set_confirm_password,
                                type_="password",
                            ),
                            rx.el.button(
                                "Register",
                                type="submit",
                                class_name=f"w-full mt-4 {md3_button_styles(True)}",
                            ),
                            on_submit=AuthState.register,
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Already have an account? ",
                                class_name=rx.cond(
                                    ChatState.dark_mode,
                                    "text-gray-300",
                                    "text-gray-600",
                                ),
                            ),
                            rx.el.a(
                                "Login",
                                href="/login",
                                class_name=f"text-[{PRIMARY_COLOR}] font-semibold hover:underline cursor-pointer",
                            ),
                            class_name=f"mt-6 text-center {TYPO_BODY_MEDIUM}",
                        ),
                    )
                ],
                class_name="w-full max-w-md p-10 m-4",
            ),
            class_name=rx.cond(
                ChatState.dark_mode,
                f"flex-1 flex items-center justify-center w-full bg-[{BACKGROUND_DARK}]",
                f"flex-1 flex items-center justify-center w-full bg-[{BACKGROUND_COLOR}]",
            ),
        ),
        class_name="min-h-screen flex flex-col font-['Open_Sans']",
    )