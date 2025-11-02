from db.database import SessionLocal
from db.models import Autor
from sqlalchemy.exc import SQLAlchemyError
from core.logger import logger


class AutorService:
    """Serviço responsável pelas operações de CRUD de autores."""

    @staticmethod
    def listar():
        """Retorna todos os autores cadastrados, ordenados por ID."""
        try:
            with SessionLocal() as session:
                autores = session.query(Autor).order_by(Autor.id).all()
                logger.info("Listagem de autores concluída com sucesso (%d registros).", len(autores))
                return autores
        except SQLAlchemyError as e:
            logger.error("Falha ao listar autores: %s", e)
            return []

    @staticmethod
    def cadastrar(nome: str) -> str:
        """Cadastra um novo autor, retornando uma mensagem de status."""
        nome = nome.strip() if nome else ""
        if not nome:
            logger.warning("Tentativa de cadastro com nome vazio.")
            return "O nome do autor não pode estar vazio."

        try:
            with SessionLocal() as session:
                existente = session.query(Autor).filter_by(nome=nome).first()
                if existente:
                    logger.info("Autor '%s' já existe.", nome)
                    return f"Autor '{nome}' já cadastrado."

                novo_autor = Autor(nome=nome)
                session.add(novo_autor)
                session.commit()
                logger.info("Autor '%s' cadastrado com sucesso (ID %d).", nome, novo_autor.id)
                return f"Autor '{nome}' cadastrado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao cadastrar autor: %s", e)
            return "Erro ao cadastrar autor."

    @staticmethod
    def editar(autor_id: int, novo_nome: str) -> str:
        """Edita o nome de um autor existente."""
        novo_nome = novo_nome.strip() if novo_nome else ""
        if not novo_nome:
            logger.warning("Tentativa de edição com nome vazio.")
            return "O novo nome não pode estar vazio."

        try:
            with SessionLocal() as session:
                autor = session.get(Autor, autor_id)
                if not autor:
                    logger.warning("Tentativa de edição de autor inexistente (ID %d).", autor_id)
                    return "Autor não encontrado."

                nome_ja_usado = session.query(Autor).filter(
                    Autor.nome == novo_nome,
                    Autor.id != autor_id
                ).first()

                if nome_ja_usado:
                    logger.info("Tentativa de renomear para nome já existente: '%s'.", novo_nome)
                    return f"Já existe um autor com o nome '{novo_nome}'."

                autor.nome = novo_nome
                session.commit()
                logger.info("Autor (ID %d) atualizado para '%s'.", autor_id, novo_nome)
                return f"Autor atualizado para '{novo_nome}' com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao editar autor (ID %d): %s", autor_id, e)
            return "Erro ao editar autor."

    @staticmethod
    def excluir(autor_id: int) -> str:
        """Exclui um autor pelo ID, retornando uma mensagem de status."""
        try:
            with SessionLocal() as session:
                autor = session.get(Autor, autor_id)
                if not autor:
                    logger.warning("Tentativa de exclusão de autor inexistente (ID %d).", autor_id)
                    return "Autor não encontrado."

                nome_autor = autor.nome
                session.delete(autor)
                session.commit()
                logger.info("Autor '%s' (ID %d) excluído com sucesso.", nome_autor, autor_id)
                return f"Autor '{nome_autor}' excluído com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao excluir autor (ID %d): %s", autor_id, e)
            return "Erro ao excluir autor."
