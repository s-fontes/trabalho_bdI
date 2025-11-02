from textual.app import ComposeResult
from textual.widgets import Button, Input, Static
from textual.containers import Vertical, Horizontal
from textual import on

from tui.autores import AutoresSelectScreen
from tui.base_view import BaseForm


class LivroCadastroDialog(BaseForm):
    """Formulário para cadastro e edição de livros.
    Mantém consistência visual com os outros diálogos.
    """

    def __init__(self, on_submit, dados_existentes: dict | None = None):
        super().__init__()
        self.on_submit = on_submit
        self.dados = dados_existentes or {}
        self.autores_selecionados = set(self.dados.get("ids_autores", []))
        self.modo_edicao = bool(dados_existentes)
        self.autores_texto = self._autores_texto()

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static(
                "Editar Livro" if self.modo_edicao else "Cadastrar Novo Livro",
                id="titulo_sub",
            ),

            Static("ISBN:", id="lbl_isbn"),
            Input(value=self.dados.get("isbn", ""), placeholder="Digite o ISBN", id="isbn"),

            Static("Título:", id="lbl_titulo"),
            Input(value=self.dados.get("titulo", ""), placeholder="Digite o título", id="titulo"),

            Static("Editora:", id="lbl_editora"),
            Input(value=self.dados.get("editora", ""), placeholder="Digite a editora", id="editora"),

            Static("Ano de Publicação:", id="lbl_ano"),
            Input(value=str(self.dados.get("ano", "")), placeholder="Ex: 2025", id="ano"),

            Horizontal(
                Button("Selecionar Autores", id="selecionar_autores"),
                Static(self.autores_texto, id="lbl_autores"),
            ),

            Horizontal(
                Button("Cancelar", id="cancelar"),
                Button("Salvar", id="salvar", variant="success"),
            ),
            id="popup_content",
        )

    # ---------------------------------------------------------
    # UTILITÁRIOS
    # ---------------------------------------------------------
    def _autores_texto(self) -> str:
        if not self.autores_selecionados:
            return "(Nenhum autor selecionado)"
        return ", ".join(self.dados.get("autores_nomes", [])) or "(Autores selecionados)"

    @on(Button.Pressed, "#selecionar_autores")
    def abrir_selecao_autores(self):
        def receber_autores(autores):
            self.autores_selecionados = {a[0] for a in autores}
            nomes = [a[1] for a in autores]
            self.dados["autores_nomes"] = nomes
            self.query_one("#lbl_autores", Static).update(self._autores_texto())
            self.app.notify(f"Autores selecionados: {', '.join(nomes) if nomes else '(nenhum)'}")

        self.app.push_screen(
            AutoresSelectScreen(
                on_select=receber_autores,
                autores_selecionados=self.autores_selecionados,
            )
        )

    @on(Button.Pressed, "#salvar")
    def salvar(self):
        isbn = self.query_one("#isbn", Input).value.strip()
        titulo = self.query_one("#titulo", Input).value.strip()
        editora = self.query_one("#editora", Input).value.strip()
        ano = self.query_one("#ano", Input).value.strip()

        if not isbn or not titulo or not editora or not ano:
            self.app.notify("Todos os campos são obrigatórios.")
            return
        if not ano.isdigit():
            self.app.notify("Ano inválido.")
            return

        self.dados.update(
            {
                "isbn": isbn,
                "titulo": titulo,
                "editora": editora,
                "ano": int(ano),
                "ids_autores": list(self.autores_selecionados),
            }
        )

        self.on_submit(self.dados)
        self.app.pop_screen()

    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        self.app.pop_screen()
