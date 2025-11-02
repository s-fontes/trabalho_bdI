from sqlalchemy.orm import joinedload
from db.database import SessionLocal
from db.models import Exemplar, Livro


class ExemplarService:
    """Serviço de manipulação dos exemplares no banco de dados."""

    @staticmethod
    def listar():
        """Retorna todos os exemplares com o livro associado já carregado."""
        with SessionLocal() as db:
            return (
                db.query(Exemplar)
                .options(joinedload(Exemplar.livro))
                .order_by(Exemplar.id)
                .all()
            )

    @staticmethod
    def cadastrar(livro_isbn: str, codigo_exemplar: str, disponivel: bool = True):
        """Cadastra um novo exemplar vinculado a um livro existente."""
        with SessionLocal() as db:
            # valida o livro
            livro = db.get(Livro, livro_isbn)
            if not livro:
                return f"Livro com ISBN '{livro_isbn}' não encontrado."

            # valida o código
            if not codigo_exemplar.strip():
                return "O código do exemplar é obrigatório."
            if db.query(Exemplar).filter_by(codigo_exemplar=codigo_exemplar).first():
                return f"O código '{codigo_exemplar}' já está em uso."

            ex = Exemplar(
                livro_isbn=livro_isbn,
                codigo_exemplar=codigo_exemplar.strip(),
                disponivel=disponivel,
            )
            db.add(ex)
            db.commit()
            return f"Exemplar '{codigo_exemplar}' cadastrado com sucesso."

    @staticmethod
    def editar(exemplar_id: int, livro_isbn: str, codigo_exemplar: str, disponivel: bool = True):
        """Edita um exemplar existente."""
        with SessionLocal() as db:
            ex = db.get(Exemplar, exemplar_id)
            if not ex:
                return "Exemplar não encontrado."

            livro = db.get(Livro, livro_isbn)
            if not livro:
                return f"Livro com ISBN '{livro_isbn}' não encontrado."

            if not codigo_exemplar.strip():
                return "O código do exemplar é obrigatório."

            duplicado = (
                db.query(Exemplar)
                .filter(
                    Exemplar.codigo_exemplar == codigo_exemplar.strip(),
                    Exemplar.id != exemplar_id,
                )
                .first()
            )
            if duplicado:
                return f"Já existe outro exemplar com o código '{codigo_exemplar}'."

            ex.livro_isbn = livro_isbn
            ex.codigo_exemplar = codigo_exemplar.strip()
            ex.disponivel = disponivel
            db.commit()
            return f"Exemplar '{codigo_exemplar}' atualizado com sucesso."

    @staticmethod
    def excluir(exemplar_id: int):
        """Exclui um exemplar existente."""
        with SessionLocal() as db:
            ex = db.get(Exemplar, exemplar_id)
            if not ex:
                return "Exemplar não encontrado."
            codigo = ex.codigo_exemplar
            db.delete(ex)
            db.commit()
            return f"Exemplar '{codigo}' excluído com sucesso."
