from datetime import date
from textual.widgets import Header, Footer, Button, Static, DataTable
from textual.containers import Horizontal, Vertical
from textual import on

from tui.base_view import BaseScreen
from tui.dialogs import ConfirmDialog
from tui.emprestimos.emprestimo_cadastro_dialog import EmprestimoCadastroDialog
from services.emprestimos_service import EmprestimoService


class EmprestimosScreen(BaseScreen):
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
        width: 18;
    }

    #tabela_emprestimos {
        border: round #666666;
        height: 70%;
        margin: 1 2;
        background: #1a1a1a;
    }
    """

    def compose(self):
        yield Header()
        yield Vertical(
            Static("Gerenciamento de Empréstimos", id="titulo"),
            Horizontal(
                Button("Novo Empréstimo", id="btn_emprestar", variant="success"),
                Button("Registrar Devolução", id="btn_devolver", variant="primary"),
                Button("Voltar", id="btn_voltar", variant="default"),
                id="botoes",
            ),
            DataTable(id="tabela_emprestimos"),
        )
        yield Footer()

    def on_mount(self):
        tabela = self.query_one("#tabela_emprestimos", DataTable)
        tabela.add_columns(
            "ID", "Usuário", "Exemplar", "Livro",
            "Data Empréstimo", "Prevista", "Devolução", "Situação"
        )
        tabela.cursor_type = "row"
        self.listar_emprestimos()
        self._update_actions()

    def _update_actions(self):
        tabela = self.query_one("#tabela_emprestimos", DataTable)
        vazio = tabela.row_count == 0
        self.query_one("#btn_devolver", Button).disabled = vazio

    def listar_emprestimos(self):
        tabela = self.query_one("#tabela_emprestimos", DataTable)
        tabela.clear()
        hoje = date.today()

        for e in EmprestimoService.listar():
            usuario = e.usuario.nome if e.usuario else "(Desconhecido)"
            exemplar = e.exemplar.codigo_exemplar if e.exemplar else "-"
            livro = e.exemplar.livro.titulo if e.exemplar and e.exemplar.livro else "-"
            data_emp = e.data_emprestimo.strftime("%d/%m/%Y")
            data_prev = e.data_prevista.strftime("%d/%m/%Y")
            data_devol = e.data_devolucao.strftime("%d/%m/%Y") if e.data_devolucao else "-"

            if e.data_devolucao:
                situacao = "✅ Devolvido"
            elif e.data_prevista < hoje:
                situacao = "🔴 Atrasado"
            else:
                situacao = "🔵 Emprestado"

            tabela.add_row(
                str(e.id), usuario, exemplar, livro, data_emp, data_prev, data_devol,situacao
            )

        if tabela.row_count:
            tabela.cursor_coordinate = (0, 0)
            tabela.focus()

        self._update_actions()

    @on(Button.Pressed, "#btn_emprestar")
    def abrir_cadastro(self):
        self.app.push_screen(EmprestimoCadastroDialog(self.emprestar))

    def emprestar(self, dados: dict):
        msg = EmprestimoService.emprestar(
            dados["usuario_id"],
            dados["exemplar_id"],
            dados["prazo_dias"],
        )
        self.app.notify(msg)
        self.listar_emprestimos()

    @on(Button.Pressed, "#btn_devolver")
    def registrar_devolucao(self):
        tabela = self.query_one("#tabela_emprestimos", DataTable)
        if tabela.row_count == 0:
            self.app.notify("Nenhum empréstimo disponível.")
            return
        row = tabela.get_row_at(tabela.cursor_row)
        if not row:
            self.app.notify("Selecione um empréstimo válido.")
            return
        emprestimo_id = int(row[0])
        self.app.push_screen(
            ConfirmDialog(
                "Registrar devolução deste exemplar?",
                lambda: self.devolver_emprestimo(emprestimo_id),
            )
        )

    def devolver_emprestimo(self, emprestimo_id: int):
        msg = EmprestimoService.devolver(emprestimo_id)
        self.app.notify(msg)
        self.listar_emprestimos()

    @on(Button.Pressed, "#btn_voltar")
    def voltar(self):
        self.app.pop_screen()
