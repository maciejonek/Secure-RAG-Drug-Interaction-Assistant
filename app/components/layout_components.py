import reflex as rx
from app.utils.md3_styles import (
    PRIMARY_COLOR,
    ELEVATION_8,
    TYPO_TITLE_LARGE,
    ELEVATION_1,
    SURFACE_COLOR,
    SURFACE_DARK,
    BACKGROUND_DARK,
    TYPO_BODY_MEDIUM,
    TEXT_LIGHT_MEDIUM,
    TEXT_DARK_MEDIUM,
    TEXT_LIGHT_HIGH,
    TEXT_DARK_HIGH,
    TEAL_ACCENT,
)
from app.states.auth_state import AuthState
from app.states.chat_state import ChatState


def app_bar(
    title: str,
    on_menu_click: rx.event.EventType = None,
    on_medication_click: rx.event.EventType = None,
) -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.button(
                        rx.icon("menu", size=24),
                        on_click=on_menu_click,
                        class_name=rx.cond(
                            ChatState.dark_mode,
                            "mr-4 md:hidden text-gray-200",
                            "mr-4 md:hidden text-gray-600",
                        ),
                    ),
                    rx.el.div(),
                ),
                rx.el.h1(
                    title,
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        f"{TYPO_TITLE_LARGE} text-white",
                        f"{TYPO_TITLE_LARGE} text-[{PRIMARY_COLOR}] font-semibold",
                    ),
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        ChatState.dark_mode,
                        rx.icon("sun", class_name="text-white", size=22),
                        rx.icon("moon", class_name="text-gray-600", size=22),
                    ),
                    on_click=ChatState.toggle_dark_mode,
                    title="Toggle Dark Mode",
                    class_name="p-2 rounded-full hover:bg-gray-200/50 dark:hover:bg-white/10 transition-colors mr-1",
                ),
                rx.cond(
                    AuthState.is_authenticated & (on_medication_click != None),
                    rx.el.button(
                        rx.icon(
                            "pill",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                "text-white",
                                f"text-[{TEAL_ACCENT}]",
                            ),
                            size=22,
                        ),
                        on_click=on_medication_click,
                        title="Toggle Medications",
                        class_name="p-2 rounded-full hover:bg-gray-200/50 dark:hover:bg-white/10 transition-colors mr-1",
                    ),
                    rx.el.div(),
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.button(
                        rx.icon(
                            "log-out",
                            class_name="text-gray-500 dark:text-gray-400",
                            size=22,
                        ),
                        on_click=AuthState.logout,
                        title="Logout",
                        class_name="p-2 rounded-full hover:bg-gray-200/50 dark:hover:bg-white/10 transition-colors",
                    ),
                    rx.el.a(
                        rx.el.button(
                            "Log in",
                            class_name=f"bg-[{TEAL_ACCENT}] text-white text-sm px-4 py-2 rounded-full font-medium hover:opacity-90 transition-opacity",
                        ),
                        href="/login",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center w-full max-w-full px-6",
        ),
        class_name=rx.cond(
            ChatState.dark_mode,
            f"w-full h-[60px] bg-[#1E1E1E]/95 backdrop-blur flex items-center sticky top-0 z-50 shrink-0 border-b border-white/10",
            f"w-full h-[60px] bg-white/80 backdrop-blur flex items-center sticky top-0 z-50 shrink-0",
        ),
    )


def md3_card(children: list[rx.Component], class_name: str = "") -> rx.Component:
    return rx.el.div(
        *children,
        class_name=rx.cond(
            ChatState.dark_mode,
            f"bg-[{SURFACE_DARK}] rounded-[16px] {ELEVATION_1} border border-white/10 {class_name}",
            f"bg-white rounded-[16px] shadow-md border border-gray-100 {class_name}",
        ),
    )


def form_field(
    label: str,
    placeholder: str,
    value: rx.Var,
    on_change: rx.event.EventType,
    type_: str = "text",
    error: rx.Var = None,
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name=rx.cond(
                ChatState.dark_mode,
                f"block {TYPO_BODY_MEDIUM} {TEXT_DARK_HIGH} mb-2 ml-1",
                f"block {TYPO_BODY_MEDIUM} text-gray-700 mb-2 ml-1",
            ),
        ),
        rx.el.input(
            on_change=on_change,
            placeholder=placeholder,
            type=type_,
            class_name=rx.cond(
                ChatState.dark_mode,
                f"w-full px-4 py-3 rounded-lg border border-gray-600 bg-white/5 focus:border-[#D0BCFF] focus:ring-1 focus:ring-[#D0BCFF] focus:outline-none transition-colors duration-200 {TEXT_DARK_HIGH} placeholder-gray-500",
                f"w-full px-4 py-3 rounded-lg border border-gray-200 bg-white focus:border-[{TEAL_ACCENT}] focus:ring-1 focus:ring-[{TEAL_ACCENT}] focus:outline-none transition-colors duration-200 text-gray-800",
            ),
            default_value=value,
        ),
        rx.cond(
            error,
            rx.el.p(
                error,
                class_name=rx.cond(
                    ChatState.dark_mode,
                    "text-[#F2B8B5] text-xs mt-1 ml-1",
                    "text-[#B00020] text-xs mt-1 ml-1",
                ),
            ),
            rx.el.div(),
        ),
        class_name="mb-4 w-full",
    )