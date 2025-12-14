import os
from dotenv import load_dotenv
from textual_pyfiglet import FigletWidget 
from openai import AzureOpenAI

from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll
from textual.widgets import Input, Markdown, Header


from rag_system_prompt import RAG_SYSTEM_PROMPT

load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("SEARCH_KEY")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")
SEMANTIC_CONFIGURATION_NAME = os.getenv("SEMANTIC_CONFIGURATION_NAME")


class ChatMessage(Markdown):
    """One chat message"""

    def update_text(self, new_text: str) -> None:
        self.update(new_text)


class ChatContainer(VerticalScroll):
    """Scrollable chat container."""
    pass


class InputArea(Container):
    """User Input"""

    def compose(self) -> ComposeResult:
        yield Input(
            placeholder="Type your message and press enter...",
            id="prompt",
        )


class GymRAG(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        """Run when the app starts."""
        self.client = AzureOpenAI(
            azure_endpoint=AZURE_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=API_VERSION,
        )

        self.conversation_history = [
            {
                "role": "system",
                "content": RAG_SYSTEM_PROMPT
            }
        ]

        self.first_message_sent = False

    def compose(self) -> ComposeResult:
        """Build the UI."""
        yield Header()
        yield ChatContainer(id="chat-container")
        yield FigletWidget("GymRAG", font="ansi_regular", id="logo")
        yield InputArea(id="input-area")

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """User pressed Enter in the input field."""

        user_input = event.value.strip()
        if not user_input:
            return
        
        if not self.first_message_sent:
            self.first_message_sent = True
            self.screen.add_class("first_message_sent")

        event.input.value = ""

        chat_container = self.query_one("#chat-container", ChatContainer)
        
        # Mount the message to VerticalScroll
        chat_container.mount(
            ChatMessage(user_input, classes="message user")
        )

        self.conversation_history.append(
            {"role": "user", "content": user_input}
        )

        chat_container.scroll_end()



if __name__ == "__main__":
    app = GymRAG()
    app.run()