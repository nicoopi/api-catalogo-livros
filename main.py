# 1. IMPORTAÇÕES: Trazendo as ferramentas que vamos usar
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

URL_BANCO = "sqlite:///./livros.db"
engine = create_engine(URL_BANCO, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LivroDB(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)

Base.metadata.create_all(bind=engine)

# INICIALIZAÇÃO: Criando o aplicativo da nossa API
app = FastAPI(title="API Catálogo de Livros")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# MODELO DE DADOS: O que é um "Livro" para a nossa API?
class Livro(BaseModel):
    id : int
    titulo : str
    autor : str


# 5. ROTAS: Os caminhos que os usuários vão acessar
# Rota para LISTAR os livros (Read)
@app.get("/livros")
def listar_livros(db: Session = Depends(get_db)):
    return db.query(LivroDB).all()

# Rota para ADICIONAR um livro (Create)
@app.post("/livros")
def adicionar_livro(novo_livro: Livro, db: Session = Depends(get_db)):
    livro_banco = LivroDB(
        id=novo_livro.id,
        titulo=novo_livro.titulo,
        autor=novo_livro.autor
    )

    db.add(livro_banco)
    db.commit()
    db.refresh(livro_banco)

    return livro_banco

# Rota para ATUALIZAR um livro (Update)
@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizado: Livro, db: Session = Depends(get_db)):
    livro_salvo = db.query(LivroDB).filter(LivroDB.id == livro_id).first()
    if livro_salvo:
        livro_salvo.titulo = livro_atualizado.titulo
        livro_salvo.autor = livro_atualizado.autor

        db.commit()
        db.refresh(livro_salvo)
        return livro_salvo

    return {"erro": "Livro não encontrado"}

# Rota para DELETAR um livro (Delete)
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro_salvo = db.query(LivroDB).filter(LivroDB.id == livro_id).first()

    if livro_salvo:
        db.delete(livro_salvo)
        db.commit()
        return {"mensagem": "Livro deletado com sucesso"}

    return {"erro": "Livro não encontrado"}