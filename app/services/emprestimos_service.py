from datetime import date, timedelta
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from db.database import SessionLocal
from db.models import Emprestimo, Exemplar, Usuario
from core.logger import logger


class EmprestimoService:
    """Serviço de gerenciamento de empréstimos e devoluções."""

    @staticmethod
    def listar():
        """Lista todos os empréstimos, com relações carregadas."""
        try:
            with SessionLocal() as db:
                emprestimos = (
                    db.query(Emprestimo)
                    .options(
                        joinedload(Emprestimo.usuario),
                        joinedload(Emprestimo.exemplar).joinedload(Exemplar.livro),
                    )
                    .order_by(Emprestimo.data_emprestimo.desc())
                    .all()
                )
                logger.info("Listagem de empréstimos concluída (%d registros).", len(emprestimos))
                return emprestimos
        except SQLAlchemyError as e:
            logger.exception("Erro ao listar empréstimos: %s", e)
            return []

    @staticmethod
    def emprestar(usuario_id: int, exemplar_id: int, prazo_dias: int) -> str:
        """Cria um novo empréstimo."""
        try:
            with SessionLocal() as db:
                usuario = db.get(Usuario, usuario_id)
                exemplar = db.get(Exemplar, exemplar_id)

                if not usuario:
                    logger.warning("Usuário não encontrado (ID %d).", usuario_id)
                    return "Usuário não encontrado."
                if not exemplar:
                    logger.warning("Exemplar não encontrado (ID %d).", exemplar_id)
                    return "Exemplar não encontrado."
                if not exemplar.disponivel:
                    logger.info("Exemplar '%s' já está emprestado.", exemplar.codigo_exemplar)
                    return f"O exemplar '{exemplar.codigo_exemplar}' já está emprestado."

                hoje = date.today()
                data_prevista = hoje + timedelta(days=prazo_dias)

                emprestimo = Emprestimo(
                    usuario_id=usuario_id,
                    exemplar_id=exemplar_id,
                    data_emprestimo=hoje,
                    data_prevista=data_prevista,
                )

                exemplar.disponivel = False
                db.add(emprestimo)
                db.commit()

                logger.info(
                    "Empréstimo criado: Usuário '%s' (ID %d), Exemplar '%s' (ID %d), Devolve até %s.",
                    usuario.nome, usuario_id, exemplar.codigo_exemplar, exemplar_id, data_prevista.isoformat()
                )

                return f"Empréstimo registrado para '{usuario.nome}' com o exemplar '{exemplar.codigo_exemplar}'."
        except SQLAlchemyError as e:
            logger.exception("Erro ao registrar empréstimo: %s", e)
            return "Erro ao registrar empréstimo."

    @staticmethod
    def devolver(emprestimo_id: int) -> str:
        """Realiza a devolução de um empréstimo ativo."""
        try:
            with SessionLocal() as db:
                emprestimo = db.get(Emprestimo, emprestimo_id)
                if not emprestimo:
                    logger.warning("Tentativa de devolução de empréstimo inexistente (ID %d).", emprestimo_id)
                    return "Empréstimo não encontrado."
                if emprestimo.data_devolucao:
                    logger.info("Empréstimo (ID %d) já foi devolvido anteriormente.", emprestimo_id)
                    return "Este empréstimo já foi devolvido."

                emprestimo.data_devolucao = date.today()

                exemplar = db.get(Exemplar, emprestimo.exemplar_id)
                exemplar.disponivel = True

                db.commit()

                logger.info(
                    "Devolução concluída: Empréstimo ID %d, Exemplar '%s' (ID %d).",
                    emprestimo_id, exemplar.codigo_exemplar, exemplar.id
                )

                return f"Exemplar '{exemplar.codigo_exemplar}' devolvido com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao processar devolução (Empréstimo ID %d): %s", emprestimo_id, e)
            return "Erro ao processar devolução."
