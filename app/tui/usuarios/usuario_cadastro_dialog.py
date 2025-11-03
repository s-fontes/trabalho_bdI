from textual.app import ComposeResult
from textual.widgets import Button, Input, Static, Select
from textual.containers import Vertical, Horizontal
from textual import on

from tui.base_view import BaseForm


class UsuarioCadastroDialog(BaseForm):
    def __init__(self, on_submit, dados_existentes: dict | None = None):
        super().__init__()
        self.on_submit = on_submit
        self.dados = dados_existentes or {}
        self.editando = bool(dados_existentes)
        self.tipo_atual = self.dados.get("tipo", "aluno")

    def compose(self) -> ComposeResult:
        titulo = "Editar Usuário" if self.editando else "Cadastro de Usuário"

        yield Vertical(
            Static(titulo, id="titulo_sub"),
            Input(value=self.dados.get("nome", ""), placeholder="Nome completo", id="nome"),
            Input(value=self.dados.get("email", ""), placeholder="E-mail", id="email"),
            Input(value=self.dados.get("cpf", ""), placeholder="CPF", id="cpf"),
            Select(
                options=[("Aluno", "aluno"), ("Professor", "professor")],
                value=self.tipo_atual,
                id="tipo",
                disabled=self.editando,
            ),
            Input(
                value=self.dados.get("extra", ""),
                placeholder=self._placeholder_extra(self.tipo_atual),
                id="extra",
            ),
            Horizontal(
                Button("Cancelar", id="cancelar"),
                Button("Salvar", id="salvar", variant="success"),
            ),
            id="popup_content",
        )

    def _placeholder_extra(self, tipo: str) -> str:
        """Retorna o placeholder apropriado conforme o tipo selecionado."""
        return "Curso do aluno" if tipo == "aluno" else "Departamento do professor"

    @on(Select.Changed, "#tipo")
    def ao_mudar_tipo(self, event: Select.Changed):
        """Atualiza o placeholder do campo extra ao trocar o tipo."""
        tipo = event.value
        campo_extra = self.query_one("#extra", Input)
        campo_extra.placeholder = self._placeholder_extra(tipo)
        campo_extra.refresh()

    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#salvar")
    def salvar(self):
        nome = self.query_one("#nome", Input).value.strip()
        email = self.query_one("#email", Input).value.strip()
        cpf = self.query_one("#cpf", Input).value.strip()
        tipo = self.query_one("#tipo", Select).value
        extra = self.query_one("#extra", Input).value.strip()

        if not nome or not email or not cpf or not tipo or not extra:
            self.app.notify("Todos os campos são obrigatórios.")
            return

        self.dados.update(
            {
                "nome": nome,
                "email": email,
                "cpf": cpf,
                "tipo": tipo,
                "extra": extra,
            }
        )

        self.on_submit(self.dados)
