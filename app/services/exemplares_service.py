from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from db.database import SessionLocal
from db.models import Exemplar, Livro
from core.logger import logger


class ExemplarService:
    @staticmethod
    def listar():
        try:
            with SessionLocal() as db:
                exemplares = (
                    db.query(Exemplar)
                    .options(joinedload(Exemplar.livro))
                    .order_by(Exemplar.id)
                    .all()
                )
                logger.info("Listagem de exemplares concluída (%d registros).", len(exemplares))
                return exemplares
        except SQLAlchemyError as e:
            logger.exception("Erro ao listar exemplares: %s", e)
            return []

    @staticmethod
    def cadastrar(livro_isbn: str, codigo_exemplar: str, disponivel: bool = True) -> str:
        codigo_exemplar = codigo_exemplar.strip() if codigo_exemplar else ""

        try:
            with SessionLocal() as db:
                livro = db.get(Livro, livro_isbn)
                if not livro:
                    logger.warning("Tentativa de cadastro com ISBN inexistente: '%s'.", livro_isbn)
                    return f"Livro com ISBN '{livro_isbn}' não encontrado."

                if not codigo_exemplar:
                    logger.warning("Código de exemplar vazio no cadastro.")
                    return "O código do exemplar é obrigatório."

                if db.query(Exemplar).filter_by(codigo_exemplar=codigo_exemplar).first():
                    logger.info("Código de exemplar duplicado: '%s'.", codigo_exemplar)
                    return f"O código '{codigo_exemplar}' já está em uso."

                exemplar = Exemplar(
                    livro_isbn=livro_isbn,
                    codigo_exemplar=codigo_exemplar,
                    disponivel=disponivel,
                )

                db.add(exemplar)
                db.commit()

                logger.info(
                    "Exemplar '%s' cadastrado com sucesso para o livro ISBN '%s'.",
                    codigo_exemplar, livro_isbn
                )

                return f"Exemplar '{codigo_exemplar}' cadastrado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao cadastrar exemplar: %s", e)
            return "Erro ao cadastrar exemplar."

    @staticmethod
    def editar(exemplar_id: int, livro_isbn: str, codigo_exemplar: str, disponivel: bool = True) -> str:
        codigo_exemplar = codigo_exemplar.strip() if codigo_exemplar else ""

        try:
            with SessionLocal() as db:
                exemplar = db.get(Exemplar, exemplar_id)
                if not exemplar:
                    logger.warning("Tentativa de editar exemplar inexistente (ID %d).", exemplar_id)
                    return "Exemplar não encontrado."

                livro = db.get(Livro, livro_isbn)
                if not livro:
                    logger.warning("Livro não encontrado ao editar exemplar (ISBN '%s').", livro_isbn)
                    return f"Livro com ISBN '{livro_isbn}' não encontrado."

                if not codigo_exemplar:
                    logger.warning("Tentativa de edição com código vazio (ID %d).", exemplar_id)
                    return "O código do exemplar é obrigatório."

                duplicado = (
                    db.query(Exemplar)
                    .filter(
                        Exemplar.codigo_exemplar == codigo_exemplar,
                        Exemplar.id != exemplar_id,
                    )
                    .first()
                )
                if duplicado:
                    logger.info("Código de exemplar duplicado na edição: '%s'.", codigo_exemplar)
                    return f"Já existe outro exemplar com o código '{codigo_exemplar}'."

                exemplar.livro_isbn = livro_isbn
                exemplar.codigo_exemplar = codigo_exemplar
                exemplar.disponivel = disponivel

                db.commit()

                logger.info(
                    "Exemplar (ID %d) atualizado com sucesso. Novo código: '%s', ISBN: '%s', Disponível: %s.",
                    exemplar_id, codigo_exemplar, livro_isbn, disponivel
                )

                return f"Exemplar '{codigo_exemplar}' atualizado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao editar exemplar (ID %d): %s", exemplar_id, e)
            return "Erro ao editar exemplar."

    @staticmethod
    def excluir(exemplar_id: int) -> str:
        try:
            with SessionLocal() as db:
                exemplar = db.get(Exemplar, exemplar_id)
                if not exemplar:
                    logger.warning("Tentativa de exclusão de exemplar inexistente (ID %d).", exemplar_id)
                    return "Exemplar não encontrado."

                codigo = exemplar.codigo_exemplar
                db.delete(exemplar)
                db.commit()

                logger.info("Exemplar '%s' (ID %d) excluído com sucesso.", codigo, exemplar_id)
                return f"Exemplar '{codigo}' excluído com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao excluir exemplar (ID %d): %s", exemplar_id, e)
            return "Erro ao excluir exemplar."
