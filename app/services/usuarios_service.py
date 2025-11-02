from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from db.database import SessionLocal
from db.models import Usuario, Aluno, Professor
from core.logger import logger


class UsuarioService:
    """Serviço responsável por operações CRUD de usuários (alunos e professores)."""

    @staticmethod
    def listar():
        """Retorna todos os usuários (alunos e professores), ordenados por nome."""
        try:
            with SessionLocal() as session:
                usuarios = (
                    session.query(Usuario)
                    .options(joinedload("*"))
                    .order_by(Usuario.nome)
                    .all()
                )
                for u in usuarios:
                    _ = getattr(u, "curso", None)
                    _ = getattr(u, "departamento", None)

                logger.info("Listagem de usuários concluída com sucesso (%d registros).", len(usuarios))
                return usuarios
        except SQLAlchemyError as e:
            logger.exception("Erro ao listar usuários: %s", e)
            return []

    @staticmethod
    def cadastrar(nome: str, email: str, cpf: str, tipo: str, extra: str) -> str:
        """Cadastra um novo aluno ou professor."""
        try:
            with SessionLocal() as session:
                if session.query(Usuario).filter_by(cpf=cpf).first():
                    logger.info("Tentativa de cadastro com CPF duplicado: %s", cpf)
                    return f"Já existe um usuário com o CPF {cpf}."

                if tipo == "aluno":
                    novo_usuario = Aluno(nome=nome, email=email, cpf=cpf, curso=extra)
                elif tipo == "professor":
                    novo_usuario = Professor(nome=nome, email=email, cpf=cpf, departamento=extra)
                else:
                    logger.warning("Tipo de usuário inválido: %s", tipo)
                    return "Tipo de usuário inválido. Use 'aluno' ou 'professor'."

                session.add(novo_usuario)
                session.commit()

                logger.info("%s '%s' cadastrado com sucesso (CPF %s).", tipo.capitalize(), nome, cpf)
                return f"{tipo.capitalize()} '{nome}' cadastrado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao cadastrar %s: %s", tipo, e)
            return f"Erro ao cadastrar {tipo}."

    @staticmethod
    def editar(usuario_id: int, nome: str, email: str, tipo: str, extra: str) -> str:
        """Edita os dados de um usuário (aluno ou professor)."""
        try:
            with SessionLocal() as session:
                usuario = session.get(Usuario, usuario_id)
                if not usuario:
                    logger.warning("Usuário não encontrado (ID %d) para edição.", usuario_id)
                    return "Usuário não encontrado."

                usuario.nome = nome.strip()
                usuario.email = email.strip()

                if tipo == "aluno" and isinstance(usuario, Aluno):
                    usuario.curso = extra.strip()
                elif tipo == "professor" and isinstance(usuario, Professor):
                    usuario.departamento = extra.strip()

                session.commit()

                logger.info("%s '%s' (ID %d) atualizado com sucesso.", tipo.capitalize(), nome, usuario_id)
                return f"{tipo.capitalize()} '{nome}' atualizado com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao editar usuário (ID %d): %s", usuario_id, e)
            return "Erro ao editar usuário."

    @staticmethod
    def excluir(usuario_id: int) -> str:
        """Exclui um usuário pelo ID."""
        try:
            with SessionLocal() as session:
                usuario = session.get(Usuario, usuario_id)
                if not usuario:
                    logger.warning("Usuário não encontrado para exclusão (ID %d).", usuario_id)
                    return "Usuário não encontrado."

                nome = usuario.nome
                session.delete(usuario)
                session.commit()

                logger.info("Usuário '%s' (ID %d) excluído com sucesso.", nome, usuario_id)
                return f"Usuário '{nome}' excluído com sucesso."
        except SQLAlchemyError as e:
            logger.exception("Erro ao excluir usuário (ID %d): %s", usuario_id, e)
            return "Erro ao excluir usuário."
