from textual.app import ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Vertical, Horizontal
from textual import on

from tui.base_view import BaseForm
from tui.livros.livro_select_view import LivroSelectScreen


class ExemplarCadastroDialog(BaseForm):
    def __init__(self, on_submit, dados_existentes: dict | None = None):
        super().__init__()
        self.on_submit = on_submit
        self.dados = dados_existentes or {}
        self.modo_edicao = bool(dados_existentes)
        self.livro_isbn = self.dados.get("livro_isbn")
        self.livro_titulo = self.dados.get("livro_titulo")

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(
                "Editar Exemplar" if self.modo_edicao else "Cadastrar Novo Exemplar",
                id="titulo_sub",
            ),

            Horizontal(
                Button("Selecionar Livro", id="selecionar_livro"),
                Static(
                    self._descricao_livro(),
                    id="lbl_livro",
                ),
            ),

            Static("Código do Exemplar:", id="lbl_codigo"),
            Input(
                value=self.dados.get("codigo_exemplar", ""),
                placeholder="Ex: EX001",
                id="codigo_exemplar",
            ),

            Horizontal(
                Button("Cancelar", id="cancelar"),
                Button("Salvar", id="salvar", variant="success"),
            ),
            id="popup_content",
        )

    def _descricao_livro(self) -> str:
        if not self.livro_isbn:
            return "(Nenhum livro selecionado)"
        titulo = self.livro_titulo or ""
        return f"{titulo} ({self.livro_isbn})" if titulo else self.livro_isbn

    @on(Button.Pressed, "#selecionar_livro")
    def abrir_lista_livros(self):
        def receber_livro(isbn, titulo):
            self.livro_isbn = isbn
            self.livro_titulo = titulo
            self.query_one("#lbl_livro", Static).update(self._descricao_livro())
            self.app.notify(f"Livro selecionado: {titulo}")

        self.app.push_screen(LivroSelectScreen(on_select=receber_livro))

    @on(Button.Pressed, "#salvar")
    def salvar(self):
        codigo_exemplar = self.query_one("#codigo_exemplar", Input).value.strip()

        if not self.livro_isbn:
            self.app.notify("Selecione um livro.")
            return
        if not codigo_exemplar:
            self.app.notify("Informe o código do exemplar.")
            return

        self.dados.update(
            {
                "livro_isbn": self.livro_isbn,
                "livro_titulo": self.livro_titulo,
                "codigo_exemplar": codigo_exemplar,
            }
        )

        self.on_submit(self.dados)
        self.app.pop_screen()

    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        self.app.pop_screen()
