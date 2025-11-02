from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Horizontal, Vertical
from textual import on

from tui.base_view import BaseScreen
from tui.dialogs import ConfirmDialog
from services.usuarios_service import UsuarioService
from tui.usuarios.usuario_cadastro_dialog import UsuarioCadastroDialog


class UsuariosScreen(BaseScreen):
    """Tela CRUD de usuários (alunos e professores)."""

    CSS = BaseScreen.CSS + """
    #titulo {
        text-align: center;
        color: white;
        padding: 1;
    }

    #botoes {
        align: center middle;
        padding: 1;
    }

    #botoes Button {
        margin: 0 1;
        width: 16;
    }

    #tabela_usuarios {
        border: round #666666;
        height: 70%;
        margin: 1 2;
        background: #1a1a1a;
    }
    """

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Gerenciamento de Usuários", id="titulo"),
            Horizontal(
                Button("Cadastrar", id="btn_cadastrar"),
                Button("Editar", id="btn_editar"),
                Button("Excluir", id="btn_excluir"),
                Button("Voltar", id="btn_voltar"),
                id="botoes",
            ),
            DataTable(id="tabela_usuarios"),
        )
        yield Footer()

    # ---------------------------------------------------------
    # CICLO DE VIDA
    # ---------------------------------------------------------
    def on_mount(self):
        tabela = self.query_one("#tabela_usuarios", DataTable)
        tabela.add_columns("ID", "Nome", "Email", "CPF", "Tipo", "Curso/Departamento")
        tabela.cursor_type = "row"
        self.listar_usuarios()
        self._update_actions()

    # ---------------------------------------------------------
    # UTILITÁRIOS
    # ---------------------------------------------------------
    def _update_actions(self):
        tabela = self.query_one("#tabela_usuarios", DataTable)
        estado_vazio = tabela.row_count == 0
        self.query_one("#btn_excluir", Button).disabled = estado_vazio
        self.query_one("#btn_editar", Button).disabled = estado_vazio

    def listar_usuarios(self):
        tabela = self.query_one("#tabela_usuarios", DataTable)
        tabela.clear()

        for u in UsuarioService.listar():
            tipo = u.tipo.capitalize()
            extra = getattr(u, "curso", getattr(u, "departamento", "-"))
            tabela.add_row(str(u.id), u.nome, u.email, u.cpf, tipo, extra)

        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()

        self._update_actions()

    # ---------------------------------------------------------
    # AÇÕES DE BOTÕES
    # ---------------------------------------------------------
    @on(Button.Pressed, "#btn_cadastrar")
    def abrir_cadastro(self):
        self.app.push_screen(UsuarioCadastroDialog(self.cadastrar_usuario))

    def cadastrar_usuario(self, dados: dict):
        msg = UsuarioService.cadastrar(
            dados["nome"],
            dados["email"],
            dados["cpf"],
            dados["tipo"],
            dados["extra"],
        )
        self.app.notify(msg)
        if "sucesso" in msg.lower():
            self.listar_usuarios()
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_editar")
    def abrir_edicao(self):
        tabela = self.query_one("#tabela_usuarios", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há usuários para editar.")
            return

        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um usuário na tabela.")
            return

        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return

        usuario_id = int(row[0])
        dados_existentes = {
            "id": usuario_id,
            "nome": row[1],
            "email": row[2],
            "cpf": row[3],
            "tipo": row[4].lower(),
            "extra": row[5],
        }

        self.app.push_screen(
            UsuarioCadastroDialog(
                lambda d: self.editar_usuario(usuario_id, d),
                dados_existentes=dados_existentes,
            )
        )

    def editar_usuario(self, usuario_id: int, dados: dict):
        msg = UsuarioService.editar(
            usuario_id,
            dados["nome"],
            dados["email"],
            dados["tipo"],
            dados["extra"],  # ✅ faltava esse parâmetro antes
        )
        self.app.notify(msg)
        if "sucesso" in msg.lower():
            self.listar_usuarios()
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_excluir")
    def abrir_exclusao(self):
        tabela = self.query_one("#tabela_usuarios", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Não há usuários para excluir.")
            return

        cursor_row = tabela.cursor_row
        if cursor_row is None:
            self.app.notify("Selecione um usuário na tabela.")
            return

        row = tabela.get_row_at(cursor_row)
        if not row:
            self.app.notify("Seleção inválida. Atualize a lista.")
            return

        usuario_id = int(row[0])
        nome = row[1]
        self.app.push_screen(
            ConfirmDialog(f"Deseja excluir '{nome}'?", lambda: self.excluir_usuario(usuario_id))
        )

    def excluir_usuario(self, usuario_id: int):
        msg = UsuarioService.excluir(usuario_id)
        self.app.notify(msg)
        self.listar_usuarios()

    @on(Button.Pressed, "#btn_voltar")
    def voltar(self):
        self.app.pop_screen()
