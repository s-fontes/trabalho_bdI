from sqlalchemy.orm import joinedload
from core.logger import logger
from db.database import SessionLocal
from db.models import Livro, Autor
from sqlalchemy.exc import SQLAlchemyError

class LivroService:
    """Serviço responsável pelas operações de CRUD de livros (com autores carregados)."""

    @staticmethod
    def listar():
        """Retorna todos os livros cadastrados, ordenados por título e com autores carregados."""
        try:
            with SessionLocal() as session:
                livros = (
                    session.query(Livro)
                    .options(joinedload(Livro.autores))  # ✅ evita DetachedInstanceError
                    .order_by(Livro.titulo)
                    .all()
                )
                logger.info("Listagem de livros concluída com sucesso (%d registros).", len(livros))
                return livros
        except SQLAlchemyError as e:
            logger.error("Falha ao listar livros: %s", e)
            return []

    @staticmethod
    def cadastrar(isbn: str, titulo: str, editora: str, ano_publicacao: int, ids_autores: list[int] = None) -> str:
        if not isbn or not titulo or not editora or not ano_publicacao:
            logger.warning("Tentativa de cadastro com campos obrigatórios ausentes.")
            return "Todos os campos (ISBN, título, editora, ano) são obrigatórios."

        try:
            with SessionLocal() as session:
                existente = session.get(Livro, isbn)
                if existente:
                    logger.info("Livro '%s' (%s) já cadastrado.", titulo, isbn)
                    return f"Livro '{titulo}' já cadastrado."

                novo_livro = Livro(
                    isbn=isbn.strip(),
                    titulo=titulo.strip(),
                    editora=editora.strip(),
                    ano_publicacao=ano_publicacao,
                )

                if ids_autores:
                    autores = session.query(Autor).filter(Autor.id.in_(ids_autores)).all()
                    novo_livro.autores = autores

                session.add(novo_livro)
                session.commit()
                logger.info("Livro '%s' (%s) cadastrado com sucesso.", titulo, isbn)
                return f"Livro '{titulo}' cadastrado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao cadastrar livro: %s", e)
            return "Erro ao cadastrar livro."

    @staticmethod
    def editar(isbn: str, titulo: str = None, editora: str = None, ano_publicacao: int = None, ids_autores: list[int] = None) -> str:
        try:
            with SessionLocal() as session:
                livro = session.get(Livro, isbn)
                if not livro:
                    logger.warning("Tentativa de edição de livro inexistente (ISBN %s).", isbn)
                    return "Livro não encontrado."

                if titulo:
                    livro.titulo = titulo.strip()
                if editora:
                    livro.editora = editora.strip()
                if ano_publicacao:
                    livro.ano_publicacao = ano_publicacao

                if ids_autores is not None:
                    autores = session.query(Autor).filter(Autor.id.in_(ids_autores)).all()
                    livro.autores = autores

                session.commit()
                logger.info("Livro '%s' (ISBN %s) atualizado com sucesso.", livro.titulo, isbn)
                return f"Livro '{livro.titulo}' atualizado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao editar livro (ISBN %s): %s", isbn, e)
            return "Erro ao editar livro."

    @staticmethod
    def excluir(isbn: str) -> str:
        try:
            with SessionLocal() as session:
                livro = session.get(Livro, isbn)
                if not livro:
                    logger.warning("Tentativa de exclusão de livro inexistente (ISBN %s).", isbn)
                    return "Livro não encontrado."

                titulo = livro.titulo
                session.delete(livro)
                session.commit()
                logger.info("Livro '%s' (ISBN %s) excluído com sucesso.", titulo, isbn)
                return f"Livro '{titulo}' excluído com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao excluir livro (ISBN %s): %s", isbn, e)
            return "Erro ao excluir livro."
