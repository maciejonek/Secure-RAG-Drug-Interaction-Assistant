import reflex as rx
from app.states.chat_state import ChatState
from app.utils.md3_styles import (
    PRIMARY_COLOR,
    PRIMARY_DARK,
    TYPO_LABEL_LARGE,
    TYPO_BODY_MEDIUM,
    SURFACE_COLOR,
    SURFACE_VARIANT_DARK,
    ELEVATION_1,
    TEXT_LIGHT_HIGH,
    TEXT_DARK_HIGH,
    TEXT_LIGHT_MEDIUM,
    TEXT_DARK_MEDIUM,
    TEAL_ACCENT,
    BACKGROUND_COLOR,
    BACKGROUND_DARK,
)


def nav_icon(
    icon_name: str,
    label: str,
    on_click: rx.event.EventType = None,
    active: bool = False,
) -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.icon(icon_name, size=24, class_name="mx-auto"),
            on_click=on_click,
            title=label,
            class_name=rx.cond(
                ChatState.dark_mode,
                rx.cond(
                    active,
                    f"w-10 h-10 rounded-full bg-[{PRIMARY_COLOR}] text-white flex items-center justify-center transition-colors",
                    "w-10 h-10 rounded-full text-gray-400 hover:bg-white/10 hover:text-white flex items-center justify-center transition-colors",
                ),
                rx.cond(
                    active,
                    f"w-10 h-10 rounded-full bg-[{TEAL_ACCENT}] text-white flex items-center justify-center transition-colors shadow-sm",
                    f"w-10 h-10 rounded-full text-gray-500 hover:bg-[{TEAL_ACCENT}]/10 hover:text-[{TEAL_ACCENT}] flex items-center justify-center transition-colors",
                ),
            ),
        ),
        class_name="flex justify-center mb-4",
    )


def minimal_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.image(
                    src="/placeholder.svg", class_name="w-8 h-8 mb-8 mx-auto opacity-80"
                ),
                nav_icon("home", "Home", ChatState.new_chat),
                nav_icon(
                    "history",
                    "History",
                    ChatState.toggle_sidebar,
                    active=ChatState.is_sidebar_open,
                ),
                class_name="flex flex-col pt-6",
            ),
            rx.el.div(
                nav_icon("settings", "Settings"),
                nav_icon("user", "Profile"),
                class_name="flex flex-col pb-6",
            ),
            class_name="flex flex-col justify-between h-full w-full",
        ),
        class_name=rx.cond(
            ChatState.dark_mode,
            f"w-[60px] h-screen shrink-0 bg-[{BACKGROUND_DARK}] border-r border-white/5 flex flex-col z-40 hidden md:flex",
            f"w-[60px] h-screen shrink-0 bg-[{BACKGROUND_COLOR}] border-r border-[#A8BBA5]/20 flex flex-col z-40 hidden md:flex",
        ),
    )


def sidebar_item(conversation: dict) -> rx.Component:
    is_active = ChatState.active_chat_id == conversation["id"]
    bg_color = rx.cond(
        is_active,
        rx.cond(ChatState.dark_mode, "bg-[#4A4458]", f"bg-[{TEAL_ACCENT}]/10"),
        rx.cond(ChatState.dark_mode, "hover:bg-white/5", "hover:bg-black/5"),
    )
    text_color = rx.cond(
        is_active,
        rx.cond(ChatState.dark_mode, "text-white", f"text-[{TEAL_ACCENT}]"),
        rx.cond(ChatState.dark_mode, "text-gray-300", "text-gray-700"),
    )
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.el.h3(
                    conversation["title"],
                    class_name=f"{TYPO_LABEL_LARGE} truncate {text_color} text-left",
                ),
                rx.el.p(
                    conversation["preview"],
                    class_name=f"{TYPO_BODY_MEDIUM} truncate text-gray-500 text-left text-xs mt-0.5",
                ),
                class_name="flex-1 overflow-hidden",
            ),
            on_click=lambda: ChatState.select_chat(conversation["id"]),
            class_name="flex items-center justify-between w-full text-left",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("trash-2", size=14),
                on_click=lambda: ChatState.delete_chat(conversation["id"]),
                class_name="text-gray-400 hover:text-red-500 p-1 rounded transition-colors",
            ),
            class_name="absolute right-2 top-3 opacity-0 group-hover:opacity-100 transition-opacity",
        ),
        class_name=f"group relative w-full px-4 py-3 rounded-lg mb-1 cursor-pointer transition-colors {bg_color}",
    )


def history_drawer() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "History",
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        "text-lg font-semibold text-white",
                        "text-lg font-semibold text-gray-800",
                    ),
                ),
                rx.el.button(
                    rx.icon("x", size=20),
                    on_click=ChatState.close_sidebar,
                    class_name="text-gray-500 hover:text-gray-800 p-1",
                ),
                class_name="flex items-center justify-between mb-6 px-4 pt-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("plus", size=16, class_name="mr-2"),
                    "New Thread",
                    on_click=ChatState.new_chat,
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        f"w-full flex items-center justify-center bg-[#4A4458] text-white py-2.5 rounded-lg mb-4 hover:bg-white/10 transition-colors text-sm font-medium",
                        f"w-full flex items-center justify-center border border-[{TEAL_ACCENT}] text-[{TEAL_ACCENT}] py-2.5 rounded-lg mb-4 hover:bg-[{TEAL_ACCENT}]/5 transition-colors text-sm font-medium",
                    ),
                ),
                class_name="px-4",
            ),
            rx.el.div(
                rx.foreach(ChatState.conversations, sidebar_item),
                class_name="flex flex-col gap-1 overflow-y-auto flex-1 px-2 custom-scrollbar",
            ),
            class_name="flex flex-col w-full h-full",
        ),
        class_name=rx.cond(
            ChatState.is_sidebar_open,
            rx.cond(
                ChatState.dark_mode,
                f"w-[280px] bg-[#1E1E1E] h-full border-r border-white/10 shrink-0 transition-all duration-300 z-50 shadow-xl fixed md:absolute left-0 md:left-[60px] top-0 bottom-0",
                f"w-[280px] bg-white h-full border-r border-gray-100 shrink-0 transition-all duration-300 z-50 shadow-xl fixed md:absolute left-0 md:left-[60px] top-0 bottom-0",
            ),
            rx.cond(
                ChatState.dark_mode,
                "w-0 bg-[#1E1E1E] h-full border-none shrink-0 transition-all duration-300 overflow-hidden fixed md:absolute left-0 md:left-[60px] top-0 bottom-0",
                "w-0 bg-white h-full border-none shrink-0 transition-all duration-300 overflow-hidden fixed md:absolute left-0 md:left-[60px] top-0 bottom-0",
            ),
        ),
    )