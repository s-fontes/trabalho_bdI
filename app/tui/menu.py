from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical, Center

from tui.autores import AutoresScreen
from tui.livros import LivrosScreen
from tui.exemplares import ExemplaresScreen
from tui.base_view import BaseScreen


class MenuScreen(BaseScreen):
    """Tela principal de menu para navegar entre os módulos."""

    CSS = BaseScreen.CSS + """
    #titulo {
        text-align: center;
        color: white;
        padding: 1;
    }

    #menu {
        align: center middle;
        padding: 2;
    }

    #menu Button {
        width: 25;
        margin: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Center(
            Vertical(
                Static("Sistema de Biblioteca Universitária", id="titulo"),
                Vertical(
                    Button("Gerenciar Autores", id="autores"),
                    Button("Gerenciar Livros", id="livros"),
                    Button("Gerenciar Exemplares", id="exemplares"),
                    Button("Sair", id="sair"),
                    id="menu",
                ),
            )
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case "autores":
                self.app.push_screen(AutoresScreen())
            case "livros":
                self.app.push_screen(LivrosScreen())
            case "exemplares":
                self.app.push_screen(ExemplaresScreen())
            case "sair":
                self.app.exit()


class MenuApp(App):
    def on_mount(self):
        self.push_screen(MenuScreen())


if __name__ == "__main__":
    MenuApp().run()
