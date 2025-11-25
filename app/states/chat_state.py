import reflex as rx
import asyncio
import datetime


class ChatState(rx.State):
    """Handles chat messages and interaction logic."""

    input_text: str = ""
    is_typing: bool = False
    is_sidebar_open: bool = False
    active_chat_id: str = "1"
    is_recording: bool = False
    is_scanning: bool = False
    playing_message_index: int = -1
    is_medication_sidebar_open: bool = False
    new_medication_input: str = ""
    dark_mode: bool = False
    current_medications: list[str] = [
        "Aspirin 81mg",
        "Lisinopril 10mg",
        "Metformin 500mg",
    ]
    messages: list[dict[str, str | list[str]]] = [
        {
            "role": "agent",
            "content": "Hello! I am your Medical Drug Interaction Assistant. Ask me about any potential drug interactions or side effects.",
            "timestamp": "Now",
            "citations": [],
        }
    ]
    conversations: list[dict[str, str]] = [
        {
            "id": "1",
            "title": "Aspirin Interactions",
            "date": "10:30 AM",
            "preview": "What are the interactions for Aspirin?",
        },
        {
            "id": "2",
            "title": "Antibiotics Check",
            "date": "Yesterday",
            "preview": "Can I take Amoxicillin with milk?",
        },
        {
            "id": "3",
            "title": "Metformin Side Effects",
            "date": "Oct 24",
            "preview": "Is nausea common with Metformin?",
        },
        {
            "id": "4",
            "title": "Lisinopril Dosage",
            "date": "Oct 22",
            "preview": "Standard starting dose for hypertension?",
        },
    ]

    @rx.event
    def toggle_sidebar(self):
        self.is_sidebar_open = not self.is_sidebar_open
        if self.is_sidebar_open:
            self.is_medication_sidebar_open = False

    @rx.event
    def close_sidebar(self):
        self.is_sidebar_open = False

    @rx.event
    def toggle_medication_sidebar(self):
        self.is_medication_sidebar_open = not self.is_medication_sidebar_open
        if self.is_medication_sidebar_open:
            self.is_sidebar_open = False

    @rx.event
    def close_medication_sidebar(self):
        self.is_medication_sidebar_open = False

    @rx.event
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    @rx.event
    def set_new_medication_input(self, value: str):
        self.new_medication_input = value

    @rx.event
    def add_medication(self):
        if self.new_medication_input.strip():
            self.current_medications.append(self.new_medication_input.strip())
            self.new_medication_input = ""

    @rx.event
    def remove_medication(self, med: str):
        self.current_medications.remove(med)

    @rx.event
    async def scan_barcode(self):
        self.is_scanning = True
        yield
        await asyncio.sleep(2.0)
        self.current_medications.append("Atorvastatin 20mg")
        self.is_scanning = False

    @rx.event
    def toggle_recording(self):
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.playing_message_index = -1

    @rx.event
    def toggle_playback(self, index: int):
        if self.playing_message_index == index:
            self.playing_message_index = -1
        else:
            self.playing_message_index = index
            self.is_recording = False

    @rx.event
    def set_input_text(self, value: str):
        self.input_text = value

    @rx.event
    def select_chat(self, chat_id: str):
        self.active_chat_id = chat_id
        if chat_id == "2":
            self.messages = [
                {
                    "role": "user",
                    "content": "Can I take Amoxicillin with milk?",
                    "timestamp": "Yesterday",
                },
                {
                    "role": "agent",
                    "content": "Calcium in milk can bind to some antibiotics, preventing absorption. It is generally recommended to avoid dairy products 2 hours before and after taking antibiotics.",
                    "timestamp": "Yesterday",
                    "citations": [
                        "Clinical Pharmacology 2024",
                        "Mayo Clinic Guidelines",
                    ],
                },
            ]
        else:
            self.messages = [
                {
                    "role": "agent",
                    "content": f"Loaded conversation {chat_id}. This is mock data for demonstration.",
                    "timestamp": "Now",
                    "citations": [],
                }
            ]

    @rx.event
    def new_chat(self):
        self.active_chat_id = ""
        self.messages = [
            {
                "role": "agent",
                "content": "Starting a new consultation. How can I help you today?",
                "timestamp": "Now",
                "citations": [],
            }
        ]

    @rx.event
    def delete_chat(self, chat_id: str):
        self.conversations = [c for c in self.conversations if c["id"] != chat_id]
        if self.active_chat_id == chat_id:
            self.new_chat()

    @rx.event
    def rename_chat(self, chat_id: str):
        for chat in self.conversations:
            if chat["id"] == chat_id:
                chat["title"] = f"Renamed: {chat['title']}"
        self.conversations = self.conversations

    @rx.event
    async def send_message(self):
        """Sends a user message and simulates an agent response."""
        if not self.input_text.strip():
            return
        user_msg = self.input_text
        timestamp = datetime.datetime.now().strftime("%H:%M")
        self.messages.append(
            {
                "role": "user",
                "content": user_msg,
                "timestamp": timestamp,
                "citations": [],
            }
        )
        self.input_text = ""
        self.is_typing = True
        yield
        await asyncio.sleep(1.5)
        agent_response = f"I've received your query about '{user_msg}'. Based on medical databases, here is some preliminary information. Always consult a doctor."
        citations = [
            "Medical Drug Database (2024)",
            "FDA Interaction Guide",
            "Journal of Clinical Medicine",
        ]
        self.messages.append(
            {
                "role": "agent",
                "content": agent_response,
                "timestamp": datetime.datetime.now().strftime("%H:%M"),
                "citations": citations,
            }
        )
        self.is_typing = False

    @rx.event
    def handle_submit(self, form_data: dict):
        """Wrapper to handle form submission (Enter key)."""
        self.input_text = form_data.get("message", "")
        return ChatState.send_message()