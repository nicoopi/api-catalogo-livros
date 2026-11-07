# 1. IMPORTAÇÕES: Trazendo as ferramentas que vamos usar
from fastapi import FastAPI
from pydantic import BaseModel

# 2. INICIALIZAÇÃO: Criando o aplicativo da nossa API
app = FastAPI(title="API Catálogo de Livros")

# 3. MODELO DE DADOS: O que é um "Livro" para a nossa API?
class Livro(BaseModel):
    id : int
    titulo : str
    autor : str

# 4. BANCO DE DADOS: Onde vamos guardar os dados temporariamente
banco_de_dados = []

# 5. ROTAS: Os caminhos que os usuários vão acessar
# Rota para LISTAR os livros (Read)
@app.get("/livros")
def listar_livros():
    return banco_de_dados

# Rota para ADICIONAR um livro (Create)
@app.post("/livros")
def adicionar_livro(novo_livro: Livro):
    banco_de_dados.append(novo_livro)
    return novo_livro

# Rota para ATUALIZAR um livro (Update)
@app.put("/livros/{livro_id}")
def atualizar_livro(livro_id: int, livro_atualizado: Livro):
    for indice, livro_salvo in enumerate(banco_de_dados):
        if livro_id == livro_salvo.id:
            banco_de_dados[indice] = livro_atualizado
            return livro_atualizado

# Rota para DELETAR um livro (Delete)
@app.delete("/livros/{livro_id}")
def deletar_livro(livro_id: int):
    for livro_salvo in banco_de_dados:
        if livro_id == livro_salvo.id:
            banco_de_dados.remove(livro_salvo)
            return {"mensagem": "Livro deletado com sucesso"}