import reflex as rx
from app.states.chat_state import ChatState
from app.utils.md3_styles import (
    PRIMARY_COLOR,
    PRIMARY_DARK,
    TYPO_LABEL_LARGE,
    TYPO_BODY_MEDIUM,
    TYPO_TITLE_LARGE,
    SURFACE_COLOR,
    SURFACE_DARK,
    ELEVATION_1,
    TEXT_LIGHT_HIGH,
    TEXT_DARK_HIGH,
    SECONDARY_COLOR,
    TEAL_ACCENT,
    BACKGROUND_COLOR,
)


def medication_item(med_name: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "pill",
                size=16,
                class_name=rx.cond(
                    ChatState.dark_mode,
                    f"text-[{PRIMARY_DARK}] mr-3",
                    f"text-[{SECONDARY_COLOR}] mr-3",
                ),
            ),
            rx.el.span(
                med_name,
                class_name=rx.cond(
                    ChatState.dark_mode,
                    f"{TYPO_BODY_MEDIUM} {TEXT_DARK_HIGH} font-medium truncate",
                    f"{TYPO_BODY_MEDIUM} text-gray-800 font-medium truncate",
                ),
            ),
            class_name="flex items-center flex-1 overflow-hidden",
        ),
        rx.el.button(
            rx.icon(
                "x",
                size=16,
                class_name=rx.cond(
                    ChatState.dark_mode,
                    "text-gray-400 hover:text-[#F2B8B5]",
                    "text-gray-400 hover:text-[#B00020]",
                ),
            ),
            on_click=lambda: ChatState.remove_medication(med_name),
            class_name=rx.cond(
                ChatState.dark_mode,
                "p-1.5 rounded-full hover:bg-white/10 transition-colors ml-2",
                "p-1.5 rounded-full hover:bg-red-50 transition-colors ml-2",
            ),
        ),
        class_name=rx.cond(
            ChatState.dark_mode,
            "flex items-center justify-between w-full px-3 py-2.5 bg-[#2D2D2D] rounded-lg border border-white/10 mb-2 hover:bg-white/5 transition-all",
            f"flex items-center justify-between w-full px-3 py-2.5 bg-white rounded-lg border border-[{SECONDARY_COLOR}]/30 mb-2 hover:shadow-sm transition-all",
        ),
    )


def medication_sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Medications",
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        f"{TYPO_TITLE_LARGE} text-white",
                        f"{TYPO_TITLE_LARGE} text-[#1D192B]",
                    ),
                ),
                rx.el.button(
                    rx.icon("x", size=24, class_name="text-gray-500"),
                    on_click=ChatState.close_medication_sidebar,
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        "md:hidden p-1 rounded-full hover:bg-white/10",
                        "md:hidden p-1 rounded-full hover:bg-gray-200",
                    ),
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.el.div(
                rx.el.p(
                    "Active medications in context.",
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        "text-xs text-gray-400 mb-4",
                        "text-xs text-gray-500 mb-4",
                    ),
                ),
                rx.el.div(
                    rx.foreach(ChatState.current_medications, medication_item),
                    class_name="flex-1 overflow-y-auto custom-scrollbar min-h-0 mb-4 pr-1",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Add medication...",
                        on_change=ChatState.set_new_medication_input,
                        class_name=rx.cond(
                            ChatState.dark_mode,
                            "w-full px-3 py-2 rounded-lg border border-gray-600 bg-[#2D2D2D] text-white text-sm focus:border-[#D0BCFF] focus:ring-0 focus:outline-none mb-2",
                            f"w-full px-3 py-2 rounded-lg border border-gray-300 text-sm focus:border-[{TEAL_ACCENT}] focus:ring-0 focus:outline-none mb-2",
                        ),
                        default_value=ChatState.new_medication_input,
                    ),
                    rx.el.button(
                        rx.icon("plus", size=16, class_name="mr-1.5"),
                        "Add",
                        on_click=ChatState.add_medication,
                        class_name=f"w-full flex items-center justify-center bg-[{TEAL_ACCENT}] text-white text-sm font-medium py-2 rounded-lg hover:opacity-90 transition-colors shadow-sm",
                    ),
                    class_name=rx.cond(
                        ChatState.dark_mode,
                        "mt-auto pt-4 border-t border-white/10",
                        "mt-auto pt-4 border-t border-gray-200",
                    ),
                ),
                class_name="flex flex-col h-full overflow-hidden",
            ),
            class_name="flex flex-col w-full h-full p-5",
        ),
        class_name=rx.cond(
            ChatState.is_medication_sidebar_open,
            rx.cond(
                ChatState.dark_mode,
                f"w-[280px] md:w-[300px] bg-[#1E1E1E] h-full border-l border-white/10 shrink-0 transition-all duration-300 ease-in-out overflow-hidden absolute md:relative z-30 shadow-2xl md:shadow-none right-0 top-0",
                f"w-[280px] md:w-[300px] bg-[{BACKGROUND_COLOR}] h-full border-l border-[#A8BBA5]/20 shrink-0 transition-all duration-300 ease-in-out overflow-hidden absolute md:relative z-30 shadow-2xl md:shadow-none right-0 top-0",
            ),
            rx.cond(
                ChatState.dark_mode,
                "w-0 bg-[#1E1E1E] h-full shrink-0 transition-all duration-300 ease-in-out overflow-hidden border-none absolute md:relative right-0 top-0",
                "w-0 bg-[#F3EDF7] h-full shrink-0 transition-all duration-300 ease-in-out overflow-hidden border-none absolute md:relative right-0 top-0",
            ),
        ),
    )