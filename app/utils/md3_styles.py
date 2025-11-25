import reflex as rx

PRIMARY_COLOR = "#C97664"
PRIMARY_DARK = "#E6B3A8"
ON_PRIMARY_COLOR = "#FFFFFF"
ON_PRIMARY_DARK = "#381E72"
SECONDARY_COLOR = "#A8BBA5"
SECONDARY_DARK = "#4A4458"
TEAL_ACCENT = "#6C9BAA"
BACKGROUND_COLOR = "#F4EDDC"
BACKGROUND_DARK = "#121212"
SURFACE_COLOR = "#FFFFFF"
SURFACE_DARK = "#1E1E1E"
SURFACE_VARIANT_DARK = "#49454F"
ERROR_COLOR = "#B00020"
ERROR_DARK = "#F2B8B5"
TEXT_LIGHT_HIGH = "text-gray-800"
TEXT_DARK_HIGH = "text-gray-100"
TEXT_LIGHT_MEDIUM = "text-gray-500"
TEXT_DARK_MEDIUM = "text-gray-400"
ELEVATION_1 = "shadow-sm"
ELEVATION_4 = "shadow-md"
ELEVATION_8 = "shadow-lg"
TYPO_DISPLAY_LARGE = "text-[57px] leading-[64px] font-normal"
TYPO_HEADLINE_LARGE = "text-[32px] leading-[40px] font-normal"
TYPO_TITLE_LARGE = "text-[22px] leading-[28px] font-medium"
TYPO_BODY_LARGE = "text-[16px] leading-[24px] font-normal tracking-[0.5px]"
TYPO_BODY_MEDIUM = "text-[14px] leading-[20px] font-normal tracking-[0.25px]"
TYPO_LABEL_LARGE = "text-[14px] leading-[20px] font-medium tracking-[0.1px]"


def md3_button_styles(is_primary: bool = True) -> str:
    base_style = "px-6 py-2.5 rounded-full font-medium transition-all duration-200 flex items-center justify-center cursor-pointer "
    if is_primary:
        return (
            base_style
            + f"bg-[{PRIMARY_COLOR}] text-white hover:opacity-90 hover:{ELEVATION_4} {ELEVATION_1}"
        )
    return (
        base_style
        + f"bg-transparent text-[{PRIMARY_COLOR}] border border-[{PRIMARY_COLOR}] hover:bg-[{PRIMARY_COLOR}]/5"
    )


def md3_input_styles() -> str:
    return f"w-full px-4 py-3 rounded-lg border border-gray-200 bg-white focus:border-[{TEAL_ACCENT}] focus:ring-1 focus:ring-[{TEAL_ACCENT}] focus:outline-none transition-colors duration-200 text-gray-800 shadow-sm"