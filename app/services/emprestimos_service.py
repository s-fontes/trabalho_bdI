from datetime import date, timedelta
from sqlalchemy.orm import joinedload
from db.database import SessionLocal
from db.models import Emprestimo, Exemplar, Usuario


class EmprestimoService:
    """Serviço de gerenciamento de empréstimos e devoluções."""

    @staticmethod
    def listar():
        """Lista todos os empréstimos, com relações carregadas."""
        with SessionLocal() as db:
            return (
                db.query(Emprestimo)
                .options(
                    joinedload(Emprestimo.usuario),
                    joinedload(Emprestimo.exemplar).joinedload(Exemplar.livro),
                )
                .order_by(Emprestimo.data_emprestimo.desc())
                .all()
            )

    @staticmethod
    def emprestar(usuario_id: int, exemplar_id: int, prazo_dias: int):
        """Cria um novo empréstimo."""
        with SessionLocal() as db:
            usuario = db.get(Usuario, usuario_id)
            exemplar = db.get(Exemplar, exemplar_id)

            if not usuario or not exemplar:
                return "Usuário ou exemplar não encontrado."
            if not exemplar.disponivel:
                return f"O exemplar '{exemplar.codigo_exemplar}' já está emprestado."

            hoje = date.today()

            emprestimo = Emprestimo(
                usuario_id=usuario_id,
                exemplar_id=exemplar_id,
                data_emprestimo=hoje,
                data_prevista=hoje + timedelta(days=prazo_dias),
            )

            exemplar.disponivel = False
            db.add(emprestimo)
            db.commit()
            return f"Empréstimo registrado para '{usuario.nome}' com o exemplar '{exemplar.codigo_exemplar}'."

    @staticmethod
    def devolver(emprestimo_id: int):
        """Realiza a devolução de um empréstimo ativo."""
        with SessionLocal() as db:
            emprestimo = db.get(Emprestimo, emprestimo_id)
            if not emprestimo:
                return "Empréstimo não encontrado."
            if emprestimo.data_devolucao:
                return "Este empréstimo já foi devolvido."

            emprestimo.data_devolucao = date.today()

            exemplar = db.get(Exemplar, emprestimo.exemplar_id)
            exemplar.disponivel = True

            db.commit()
            return f"Exemplar '{exemplar.codigo_exemplar}' devolvido com sucesso."
