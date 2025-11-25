import reflex as rx
from app.utils.md3_styles import (
    PRIMARY_COLOR,
    PRIMARY_DARK,
    SURFACE_DARK,
    TYPO_BODY_LARGE,
    TYPO_BODY_MEDIUM,
    ELEVATION_1,
    ELEVATION_4,
    TYPO_LABEL_LARGE,
    TEAL_ACCENT,
    SECONDARY_COLOR,
    BACKGROUND_COLOR,
)
from app.states.chat_state import ChatState


def citation_view(citations: list[str]) -> rx.Component:
    return rx.cond(
        citations.length() > 0,
        rx.el.div(
            rx.el.p(
                "Sources",
                class_name=rx.cond(
                    ChatState.dark_mode,
                    "text-[11px] font-bold text-gray-400 mb-1 mt-2 uppercase tracking-wide",
                    "text-[11px] font-bold text-gray-500 mb-1 mt-2 uppercase tracking-wide",
                ),
            ),
            rx.el.div(
                rx.foreach(
                    citations,
                    lambda cite: rx.el.div(
                        rx.icon(
                            "book-open",
                            size=12,
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"text-[{SECONDARY_COLOR}] mr-1.5",
                                "text-gray-600 mr-1.5",
                            ),
                        ),
                        rx.el.span(cite, class_name="truncate"),
                        class_name=rx.cond(
                            ChatState.dark_mode,
                            f"flex items-center text-[11px] text-gray-200 bg-white/10 px-2.5 py-1.5 rounded-md border border-white/10 max-w-full",
                            f"flex items-center text-[11px] text-gray-700 bg-[{SECONDARY_COLOR}]/20 px-2.5 py-1.5 rounded-md border border-[{SECONDARY_COLOR}]/30 max-w-full",
                        ),
                    ),
                ),
                class_name="flex flex-wrap gap-2",
            ),
            class_name=rx.cond(
                ChatState.dark_mode,
                "border-t border-white/10 mt-3 pt-2",
                "border-t border-gray-100 mt-3 pt-2",
            ),
        ),
        rx.el.div(),
    )


def message_bubble(message: dict, index: int) -> rx.Component:
    is_user = message["role"] == "user"
    bg_color = rx.cond(
        is_user,
        rx.cond(
            ChatState.dark_mode, f"bg-[{PRIMARY_COLOR}]/80", f"bg-[{PRIMARY_COLOR}]"
        ),
        rx.cond(
            ChatState.dark_mode,
            f"bg-[{SURFACE_DARK}] border border-white/10",
            f"bg-[#F4EDDC] border border-transparent shadow-sm",
        ),
    )
    text_color = rx.cond(
        is_user,
        "text-white",
        rx.cond(ChatState.dark_mode, "text-gray-100", "text-gray-800"),
    )
    align_class = rx.cond(is_user, "justify-end", "justify-start")
    rounded_class = rx.cond(
        is_user, "rounded-2xl rounded-br-sm", "rounded-2xl rounded-bl-sm"
    )
    show_citations = rx.cond(~is_user, citation_view(message["citations"]), rx.el.div())
    audio_icon_color = rx.cond(ChatState.dark_mode, "text-gray-300", "text-gray-600")
    audio_active_color = rx.cond(
        ChatState.dark_mode, f"text-[{TEAL_ACCENT}]", f"text-[{TEAL_ACCENT}]"
    )
    wave_color = rx.cond(
        ChatState.dark_mode, f"bg-[{TEAL_ACCENT}]", f"bg-[{TEAL_ACCENT}]"
    )
    hover_bg = rx.cond(ChatState.dark_mode, "hover:bg-white/10", "hover:bg-black/5")
    audio_controls = rx.cond(
        ~is_user,
        rx.el.div(
            rx.el.button(
                rx.cond(
                    ChatState.playing_message_index == index,
                    rx.icon("circle_pause", size=18, class_name=audio_active_color),
                    rx.icon("volume-2", size=18, class_name=audio_icon_color),
                ),
                on_click=lambda: ChatState.toggle_playback(index),
                class_name=f"p-1.5 rounded-full {hover_bg} transition-colors flex items-center justify-center",
            ),
            rx.cond(
                ChatState.playing_message_index == index,
                rx.el.div(
                    rx.el.div(
                        class_name=f"w-0.5 h-3 {wave_color} mx-0.5 rounded-full animate-wave",
                        style={"animation-delay": "0s"},
                    ),
                    rx.el.div(
                        class_name=f"w-0.5 h-5 {wave_color} mx-0.5 rounded-full animate-wave",
                        style={"animation-delay": "0.1s"},
                    ),
                    rx.el.div(
                        class_name=f"w-0.5 h-3 {wave_color} mx-0.5 rounded-full animate-wave",
                        style={"animation-delay": "0.2s"},
                    ),
                    class_name="flex items-center h-6 ml-2",
                ),
                rx.el.div(),
            ),
            class_name=rx.cond(
                ChatState.dark_mode,
                "flex items-center mt-2 border-t border-white/10 pt-2 w-fit",
                "flex items-center mt-2 border-t border-black/5 pt-2 w-fit",
            ),
        ),
        rx.el.div(),
    )
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                message["content"],
                class_name=f"{TYPO_BODY_LARGE} {text_color} whitespace-pre-wrap",
            ),
            show_citations,
            audio_controls,
            rx.el.span(
                message["timestamp"],
                class_name=f"text-[10px] opacity-60 block text-right mt-1 {text_color}",
            ),
            class_name=f"max-w-full sm:max-w-[85%] px-5 py-4 {bg_color} {rounded_class} {ELEVATION_1} overflow-hidden",
        ),
        class_name=f"flex w-full mb-6 {align_class} animate-fade-in",
    )


def chat_input_area() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.cond(
                ChatState.is_recording,
                rx.el.div(
                    rx.el.span(
                        "Listening...",
                        class_name="text-[#B00020] font-medium mr-3 animate-pulse",
                    ),
                    rx.el.div(
                        class_name="w-1 h-3 bg-[#B00020] mx-0.5 rounded-full animate-wave",
                        style={"animation-delay": "0s"},
                    ),
                    rx.el.div(
                        class_name="w-1 h-5 bg-[#B00020] mx-0.5 rounded-full animate-wave",
                        style={"animation-delay": "0.1s"},
                    ),
                    rx.el.div(
                        class_name="w-1 h-3 bg-[#B00020] mx-0.5 rounded-full animate-wave",
                        style={"animation-delay": "0.2s"},
                    ),
                    class_name="absolute inset-0 bg-white/95 z-10 flex items-center justify-center rounded-full backdrop-blur-sm border border-[#B00020]/20",
                ),
                rx.el.div(),
            ),
            rx.el.input(
                placeholder="Ask anything...",
                name="message",
                class_name=rx.cond(
                    ChatState.dark_mode,
                    f"flex-1 bg-[#2D2D2D] border-none focus:ring-0 focus:outline-none text-gray-100 {TYPO_BODY_LARGE} px-4 py-3 rounded-full placeholder-gray-400",
                    f"flex-1 bg-transparent border-none focus:ring-0 focus:outline-none text-gray-800 {TYPO_BODY_LARGE} px-4 py-3 rounded-full placeholder-gray-400",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(
                        ChatState.is_scanning,
                        rx.icon(
                            "loader",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"text-[{TEAL_ACCENT}] animate-spin",
                                f"text-[{TEAL_ACCENT}] animate-spin",
                            ),
                            size=20,
                        ),
                        rx.icon(
                            "barcode",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"text-[{TEAL_ACCENT}]",
                                f"text-[{TEAL_ACCENT}]",
                            ),
                            size=20,
                        ),
                    ),
                    on_click=ChatState.scan_barcode,
                    type="button",
                    disabled=ChatState.is_scanning,
                    title="Scan Barcode",
                    class_name="p-2 rounded-full hover:bg-gray-100 transition-colors",
                ),
                rx.el.button(
                    rx.cond(
                        ChatState.is_recording,
                        rx.icon("mic-off", class_name="text-white", size=20),
                        rx.icon(
                            "mic",
                            class_name=rx.cond(
                                ChatState.dark_mode,
                                f"text-[{TEAL_ACCENT}]",
                                f"text-[{TEAL_ACCENT}]",
                            ),
                            size=20,
                        ),
                    ),
                    on_click=ChatState.toggle_recording,
                    type="button",
                    class_name=rx.cond(
                        ChatState.is_recording,
                        f"p-2 rounded-full bg-[#B00020] hover:bg-[#d90026] transition-colors ml-1 animate-pulse-red",
                        f"p-2 rounded-full hover:bg-gray-100 transition-colors ml-1",
                    ),
                ),
                rx.el.button(
                    rx.icon("arrow-right", class_name="text-white", size=20),
                    type="submit",
                    class_name=f"p-2 rounded-full bg-[{TEAL_ACCENT}] flex items-center justify-center hover:opacity-90 transition-colors ml-2",
                ),
                class_name="flex items-center pr-1",
            ),
            class_name=rx.cond(
                ChatState.dark_mode,
                f"w-full max-w-3xl mx-auto flex items-center bg-[#1E1E1E] rounded-full p-1.5 border border-white/10 {ELEVATION_4} relative",
                f"w-full max-w-3xl mx-auto flex items-center bg-white rounded-full p-1.5 border border-gray-200 {ELEVATION_4} relative",
            ),
        ),
        on_submit=ChatState.handle_submit,
        reset_on_submit=True,
        class_name=rx.cond(
            ChatState.dark_mode,
            "w-full px-4 pb-8 pt-4 bg-gradient-to-t from-[#121212] via-[#121212] to-transparent sticky bottom-0",
            f"w-full px-4 pb-8 pt-4 bg-gradient-to-t from-white via-white to-transparent sticky bottom-0",
        ),
    )