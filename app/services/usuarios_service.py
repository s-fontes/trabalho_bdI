from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
from db.database import SessionLocal
from db.models import Usuario, Aluno, Professor


class UsuarioService:
    """Serviço responsável por operações CRUD de usuários (alunos e professores)."""

    @staticmethod
    def listar():
        try:
            with SessionLocal() as db:
                usuarios = (
                    db.query(Usuario)
                    .options(joinedload('*'))
                    .order_by(Usuario.nome)
                    .all()
                )
                for u in usuarios:
                    _ = getattr(u, "curso", None)
                    _ = getattr(u, "departamento", None)
                return usuarios
        except SQLAlchemyError as e:
            print(f"Erro ao listar usuários: {e}")
            return []

    @staticmethod
    def cadastrar(nome: str, email: str, cpf: str, tipo: str, extra: str):
        with SessionLocal() as db:
            if db.query(Usuario).filter_by(cpf=cpf).first():
                return f"Já existe um usuário com o CPF {cpf}."

            if tipo == "aluno":
                novo = Aluno(nome=nome, email=email, cpf=cpf, curso=extra)
            elif tipo == "professor":
                novo = Professor(nome=nome, email=email, cpf=cpf, departamento=extra)
            else:
                return "Tipo de usuário inválido."

            db.add(novo)
            db.commit()
            return f"{tipo.capitalize()} '{nome}' cadastrado com sucesso."

    @staticmethod
    def editar(usuario_id: int, nome: str, email: str, tipo: str, extra: str):
        with SessionLocal() as db:
            usuario = db.get(Usuario, usuario_id)
            if not usuario:
                return "Usuário não encontrado."

            usuario.nome = nome
            usuario.email = email

            if tipo == "aluno" and isinstance(usuario, Aluno):
                usuario.curso = extra
            elif tipo == "professor" and isinstance(usuario, Professor):
                usuario.departamento = extra

            db.commit()
            return f"{tipo.capitalize()} '{nome}' atualizado com sucesso."

    @staticmethod
    def excluir(usuario_id: int):
        with SessionLocal() as db:
            usuario = db.get(Usuario, usuario_id)
            if not usuario:
                return "Usuário não encontrado."

            nome = usuario.nome
            db.delete(usuario)
            db.commit()
            return f"Usuário '{nome}' excluído com sucesso."
