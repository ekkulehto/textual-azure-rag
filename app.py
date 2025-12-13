import os
from dotenv import load_dotenv
from pyfiglet import figlet_format
from textual.app import App, ComposeResult
from textual.widgets import TextArea, Footer, Header, Static, Button
from textual.containers import HorizontalGroup, VerticalGroup

load_dotenv()

AZURE_ENDPOINT = os.getenv('AZURE_ENDPOINT')
API_KEY = os.getenv('API_KEY ')
DEPLOYMENT_NAME = os.getenv('DEPLOYMENT_NAME')
API_VERSION = os.getenv('API_VERSION')


class ChatContainer(VerticalGroup):
    pass

class Logo(Static):
    def __init__(self) -> None:
        text = figlet_format("GymRAG", font="larry3d")
        super().__init__(text, id="logo")


class UserTextArea(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield TextArea(placeholder="What do you want to know?", id="input")
        # yield Button("Send", id="send", variant="success")


class Chatbot(App):
    CSS_PATH = "style.tcss"

    def compose(self) -> ComposeResult:
        yield Footer(show_command_palette=False)
        yield Header()
        yield Logo()
        yield UserTextArea()


if __name__ == "__main__":
    app = Chatbot()
    app.run()
