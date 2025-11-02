from textual.screen import Screen
from textual.widgets import Button, Static, Input
from textual.containers import Vertical, Horizontal, Center
from textual.app import ComposeResult


class BaseDialog(Screen):
    """Base visual para caixas de diálogo reutilizáveis."""

    CSS = """
    Screen {
        align: center middle;
        background: rgba(0,0,0,0.6);
    }

    #dialog {
        border: round #777777;
        background: #1e1e1e;
        width: 50%;
        padding: 2;
    }

    #title, #message {
        text-align: center;
        color: white;
        padding: 1;
    }

    Input {
        width: 90%;
        margin: 1 0;
    }

    Button {
        min-width: 12;
        margin: 1;
        background: #333333;
        color: white;
    }

    Button:hover {
        background: #444444;
    }
    """


class ConfirmDialog(BaseDialog):
    """Janela de confirmação genérica (exclusão, saída, etc)."""

    def __init__(self, mensagem: str, on_confirm):
        super().__init__()
        self.mensagem = mensagem
        self.on_confirm = on_confirm

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static(self.mensagem, id="message"),
                Horizontal(
                    Button("Cancelar", id="cancelar"),
                    Button("Confirmar", id="confirmar"),
                ),
                id="dialog",
            )
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "confirmar":
            self.on_confirm()
        self.app.pop_screen()


class InputDialog(BaseDialog):
    """Janela de entrada de texto simples."""

    def __init__(self, titulo: str, placeholder: str, on_submit):
        super().__init__()
        self.titulo = titulo
        self.placeholder = placeholder
        self.on_submit = on_submit

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static(self.titulo, id="title"),
                Input(placeholder=self.placeholder, id="input_field"),
                Horizontal(
                    Button("Cancelar", id="cancelar"),
                    Button("Salvar", id="salvar"),
                ),
                id="dialog",
            )
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "salvar":
            valor = self.query_one("#input_field", Input).value.strip()
            if valor:
                self.on_submit(valor)
        self.app.pop_screen()


class EditDialog(BaseDialog):
    """Janela de edição com valor inicial."""

    def __init__(self, item_id: int, valor_atual: str, on_submit):
        super().__init__()
        self.item_id = item_id
        self.valor_atual = valor_atual
        self.on_submit = on_submit

    def compose(self) -> ComposeResult:
        yield Center(
            Vertical(
                Static("Editar registro", id="title"),
                Input(value=self.valor_atual, id="input_edit"),
                Horizontal(
                    Button("Cancelar", id="cancelar"),
                    Button("Salvar", id="salvar"),
                ),
                id="dialog",
            )
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "salvar":
            novo_valor = self.query_one("#input_edit", Input).value.strip()
            if novo_valor:
                self.on_submit(self.item_id, novo_valor)
        self.app.pop_screen()
