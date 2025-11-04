from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import (
    Integer, String, ForeignKey, Date, Boolean, func, CheckConstraint
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from db.database import Base


tipo_usuario_enum = ENUM(
    'aluno',
    'professor',
    name='tipo_usuario',
    schema='biblioteca',
    create_type=False
)


class Autor(Base):
    __tablename__ = "autores"
    __table_args__ = {"schema": "biblioteca"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)

    livros = relationship(
        "Livro",
        secondary="biblioteca.livros_autores",
        back_populates="autores",
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Autor(nome='{self.nome}')>"


class Livro(Base):
    __tablename__ = "livros"
    __table_args__ = {"schema": "biblioteca"}

    isbn: Mapped[str] = mapped_column(String(20), primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    editora: Mapped[str] = mapped_column(String(100), nullable=False)
    ano_publicacao: Mapped[int] = mapped_column(Integer, nullable=False)

    autores = relationship(
        "Autor",
        secondary="biblioteca.livros_autores",
        back_populates="livros",
        passive_deletes=True
    )

    exemplares = relationship(
        "Exemplar",
        back_populates="livro",
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Livro(titulo='{self.titulo}', isbn='{self.isbn}')>"


class LivroAutor(Base):
    __tablename__ = "livros_autores"
    __table_args__ = {"schema": "biblioteca"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    livro_isbn: Mapped[str] = mapped_column(ForeignKey("biblioteca.livros.isbn", ondelete="CASCADE"), nullable=False)
    autor_id: Mapped[int] = mapped_column(ForeignKey("biblioteca.autores.id", ondelete="CASCADE"), nullable=False)


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "biblioteca"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=False)
    tipo: Mapped[str] = mapped_column(tipo_usuario_enum, nullable=False)

    emprestimos = relationship(
        "Emprestimo",
        back_populates="usuario",
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_identity": "usuario",
        "polymorphic_on": tipo,
    }


class Aluno(Usuario):
    __tablename__ = "alunos"
    __table_args__ = {"schema": "biblioteca"}

    id: Mapped[int] = mapped_column(
        ForeignKey("biblioteca.usuarios.id", ondelete="CASCADE"),
        primary_key=True
    )
    curso: Mapped[str] = mapped_column(String(100), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "aluno",
    }


class Professor(Usuario):
    __tablename__ = "professores"
    __table_args__ = {"schema": "biblioteca"}

    id: Mapped[int] = mapped_column(
        ForeignKey("biblioteca.usuarios.id", ondelete="CASCADE"),
        primary_key=True
    )
    departamento: Mapped[str] = mapped_column(String(100), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "professor",
    }


class Exemplar(Base):
    __tablename__ = "exemplares"
    __table_args__ = {"schema": "biblioteca"}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    livro_isbn: Mapped[str] = mapped_column(
        ForeignKey("biblioteca.livros.isbn", ondelete="CASCADE"),
        nullable=False
    )
    codigo_exemplar: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    disponivel: Mapped[bool] = mapped_column(Boolean, default=True)

    livro = relationship("Livro", back_populates="exemplares")
    emprestimos = relationship(
        "Emprestimo",
        back_populates="exemplar",
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Exemplar(codigo='{self.codigo_exemplar}', livro='{self.livro_isbn}')>"


class Emprestimo(Base):
    __tablename__ = "emprestimos"
    __table_args__ = (
        CheckConstraint("data_prevista >= data_emprestimo", name="chk_data_prevista"),
        {"schema": "biblioteca"}
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("biblioteca.usuarios.id", ondelete="CASCADE"),
        nullable=False
    )
    exemplar_id: Mapped[int] = mapped_column(
        ForeignKey("biblioteca.exemplares.id", ondelete="CASCADE"),
        nullable=False
    )

    data_emprestimo: Mapped[Date] = mapped_column(Date, nullable=False, server_default=func.current_date())
    data_prevista: Mapped[Date] = mapped_column(Date, nullable=False)
    data_devolucao: Mapped[Date] = mapped_column(Date, nullable=True)

    usuario = relationship("Usuario", back_populates="emprestimos")
    exemplar = relationship("Exemplar", back_populates="emprestimos")

    def __repr__(self):
        return f"<Emprestimo(usuario={self.usuario_id}, exemplar={self.exemplar_id})>"
