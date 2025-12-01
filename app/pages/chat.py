import reflex as rx
from app.states.auth_state import AuthState
from app.states.chat_state import ChatState
from app.components.layout_components import app_bar
from app.components.chat_ui import (
    message_bubble,
    chat_input_area,
    landing_view,
    barcode_scanner_modal,
)
from app.components.sidebar import minimal_sidebar, history_drawer
from app.components.medication_sidebar import medication_sidebar
from app.utils.md3_styles import BACKGROUND_DARK, BACKGROUND_COLOR


def chat_page() -> rx.Component:
    return rx.el.div(
        barcode_scanner_modal(),
        rx.cond(AuthState.is_authenticated, minimal_sidebar(), rx.el.div()),
        rx.el.div(
            app_bar(
                "Medical Assistant",
                on_menu_click=ChatState.toggle_sidebar,
                on_medication_click=ChatState.toggle_medication_sidebar,
            ),
            rx.el.div(
                rx.cond(AuthState.is_authenticated, history_drawer(), rx.el.div()),
                rx.cond(
                    ChatState.is_sidebar_open & AuthState.is_authenticated,
                    rx.el.div(
                        class_name="fixed inset-0 bg-black/50 z-40 md:hidden backdrop-blur-sm transition-opacity",
                        on_click=ChatState.close_sidebar,
                    ),
                    rx.el.div(),
                ),
                rx.cond(
                    ChatState.is_home_screen,
                    landing_view(),
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(
                                ChatState.messages,
                                lambda msg, idx: message_bubble(msg, idx),
                            ),
                            rx.cond(
                                ChatState.is_typing,
                                rx.el.div(
                                    rx.el.div(
                                        class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                                    ),
                                    rx.el.div(
                                        class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"
                                    ),
                                    rx.el.div(
                                        class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"
                                    ),
                                    class_name=rx.cond(
                                        ChatState.dark_mode,
                                        "flex gap-1 p-4 bg-[#333333] rounded-r-2xl rounded-tl-2xl w-fit mb-4",
                                        "flex gap-1 p-4 bg-[#F4EDDC] rounded-r-2xl rounded-tl-2xl w-fit mb-4 border border-transparent shadow-sm",
                                    ),
                                ),
                                rx.el.div(),
                            ),
                            rx.el.div(class_name="h-32"),
                            class_name="flex-1 w-full max-w-3xl mx-auto px-4 md:px-0 py-8 overflow-y-auto flex flex-col custom-scrollbar",
                        ),
                        chat_input_area(centered=False),
                        class_name=rx.cond(
                            ChatState.dark_mode,
                            f"flex-1 flex flex-col w-full overflow-hidden bg-[{BACKGROUND_DARK}] relative h-full",
                            "flex-1 flex flex-col w-full overflow-hidden bg-white relative h-full",
                        ),
                    ),
                ),
                rx.cond(
                    ChatState.is_medication_sidebar_open & AuthState.is_authenticated,
                    rx.el.div(
                        class_name="absolute inset-0 bg-black/20 z-20 md:hidden backdrop-blur-sm transition-opacity",
                        on_click=ChatState.close_medication_sidebar,
                    ),
                    rx.el.div(),
                ),
                rx.cond(AuthState.is_authenticated, medication_sidebar(), rx.el.div()),
                class_name="flex-1 flex overflow-hidden w-full relative",
            ),
            class_name="flex flex-col flex-1 h-screen overflow-hidden relative",
        ),
        class_name=rx.cond(
            ChatState.dark_mode,
            f"h-screen flex flex-row font-['Open_Sans'] bg-[{BACKGROUND_DARK}]",
            f"h-screen flex flex-row font-['Open_Sans'] bg-[{BACKGROUND_COLOR}]",
        ),
    )