from textual.app import ComposeResult
from textual.widgets import Button, Static, Select
from textual.containers import Vertical, Horizontal
from textual import on

from tui.dialogs import BaseDialog
from services.usuarios_service import UsuarioService
from services.exemplares_service import ExemplarService


class EmprestimoCadastroDialog(BaseDialog):
    """Diálogo para registrar um novo empréstimo."""

    def __init__(self, on_submit):
        super().__init__()
        self.titulo_texto = "Novo Empréstimo"
        self.on_submit = on_submit

    def compose(self) -> ComposeResult:
        # opções de usuários e exemplares disponíveis
        usuarios_opts = [(u.nome, str(u.id)) for u in UsuarioService.listar()]
        exemplares_opts = [
            (f"{ex.codigo_exemplar} - {ex.livro.titulo}", str(ex.id))
            for ex in ExemplarService.listar()
            if ex.disponivel
        ]

        # seletor de prazo (1 a 15 dias, padrão 7)
        prazos_opts = [(f"{d} dias", str(d)) for d in range(1, 16)]

        yield Vertical(
            Static(self.titulo_texto, id="titulo_sub"),
            Select(options=usuarios_opts, id="usuario", prompt="Selecione o usuário"),
            Select(options=exemplares_opts, id="exemplar", prompt="Selecione o exemplar disponível"),
            Select(options=prazos_opts, id="prazo", prompt="Selecione o prazo (padrão: 7 dias)", value="7"),
            Horizontal(
                Button("Cancelar", id="cancelar"),
                Button("Confirmar", id="salvar", variant="success"),
            ),
            id="popup_content",
        )

    # ---------------------------------------------------------
    # AÇÕES DE BOTÕES
    # ---------------------------------------------------------
    @on(Button.Pressed, "#cancelar")
    def cancelar(self):
        """Fecha o diálogo sem salvar."""
        self.app.pop_screen()

    @on(Button.Pressed, "#salvar")
    def salvar(self):
        """Valida os campos e envia os dados ao callback."""
        usuario_id = self.query_one("#usuario", Select).value
        exemplar_id = self.query_one("#exemplar", Select).value
        prazo_valor = self.query_one("#prazo", Select).value

        if not usuario_id or not exemplar_id:
            self.app.notify("Selecione um usuário e um exemplar disponíveis.")
            return

        try:
            prazo_dias = int(prazo_valor or 7)
        except ValueError:
            prazo_dias = 7

        self.on_submit({
            "usuario_id": int(usuario_id),
            "exemplar_id": int(exemplar_id),
            "prazo_dias": prazo_dias,
        })
        self.app.pop_screen()
