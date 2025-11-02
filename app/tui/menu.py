from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, Static
from textual.containers import Vertical, Center

from tui.autores import AutoresScreen
from tui.livros import LivrosScreen
from tui.exemplares import ExemplaresScreen
from tui.usuarios import UsuariosScreen
from tui.emprestimos import EmprestimosScreen
from tui.base_view import BaseScreen


class MenuScreen(BaseScreen):
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
                    Button("Autores", id="autores"),
                    Button("Livros", id="livros"),
                    Button("Exemplares", id="exemplares"),
                    Button("Usuários", id="usuarios"),
                    Button("Empréstimos", id="emprestimos"),
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
            case "usuarios":
                self.app.push_screen(UsuariosScreen())
            case "emprestimos":
                self.app.push_screen(EmprestimosScreen())
            case "sair":
                self.app.exit()


class Biblioteca(App):
    def on_mount(self):
        self.push_screen(MenuScreen())


if __name__ == "__main__":
    Biblioteca().run()
