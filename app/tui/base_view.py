from textual.screen import Screen
from textual.widgets import Header, Footer
from tui.dialogs import BaseDialog


class BaseForm(BaseDialog):
    CSS = BaseDialog.CSS + """
    Screen {
        align: center middle;
        background: rgba(0,0,0,0.6); /* overlay translúcido */
    }

    #popup_content {
        align: center middle;
        border: round #888888;
        background: #1b1b1b;
        padding: 2;
    }

    Input {
        width: 85%;
        border: round #666666;
        margin: 1 0;
    }

    Button {
        width: 18;
        margin: 1;
        background: #333333;
        color: white;
    }

    Button:hover {
        background: #444444;
    }

    #titulo_sub {
        text-align: center;
        color: white;
        padding: 1;
    }
    """


class BaseScreen(Screen):
    CSS = """
    Screen {
        align: center middle;
        background: #111111;
    }

    Header, Footer {
        background: #222222;
        color: white;
    }

    Button {
        background: #333333;
        color: white;
        min-width: 12;
        margin: 1;
    }

    Button:hover {
        background: #444444;
    }

    DataTable {
        border: round #666666;
        background: #1a1a1a;
        padding: 1;
    }

    Static {
        color: white;
        text-align: center;
    }
    """

    def add_header_footer(self):
        yield Header()
        yield Footer()
