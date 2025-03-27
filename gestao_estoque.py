import sqlite3
from tabulate import tabulate
codigo_sequencial = 1
conn = sqlite3.connect('estoque.db')
cursor = conn.cursor()

def gerador_codigo():
  global codigo_sequencial
  codigo_sequencial += 1
  
def plotar_menu():
  while True:
    try:
      opcao = int(input('''
      1 - Cadastrar produto
      2 - Listar produtos
      3 - Remover produto
      4 - Atualizar produto
      5 - Sair\nDigite aqui -->:  '''))
      if opcao:
        return opcao
    except ValueError:
      print('Digite um número válido!')
      
def criar_tabela():
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos(
              ID_PRODUTO INTEGER PRIMARY KEY,
              nome TEXT NOT NULL,
              estoque INTEGER NOT NULL
            )
    ''')
    conn.commit()

def adicionar_produto(nome, estoque):
    gerador_codigo()
    cursor.execute('''
            INSERT INTO produtos(ID_PRODUTO, nome, estoque)
            VALUES(?,?,?)
    ''', (codigo_sequencial, nome, estoque))
    conn.commit()
def listar_produtos():
  cursor.execute('SELECT * FROM produtos')
  produtos = cursor.fetchall()
  if produtos:
    print(tabulate(produtos, headers=["Código", "Nome", "Estoque"], tablefmt="grid"))
  else:
    print("Nenhum produto cadastrado.")
def remover_produto(codigo):
  cursor.execute("DELETE FROM produtos WHERE ID_PRODUTO=?", (codigo))
  conn.commit()

def atualizar_produto(codigo, nome, estoque):
  cursor.execute("UPDATE produtos SET nome=?, estoque=? WHERE ID_PRODUTO=?", (nome, estoque, codigo))
  conn.commit()

def main():
  while True:
    opcao = plotar_menu()
    match opcao:
      case 1:
        while True:
          try:
            nome_item = str(input("Digite o nome do produto: ")).title()
            if nome_item:
              estoque_item = int(input("Digite a quantidade do produto: "))
              if estoque_item:
                adicionar_produto(nome_item, estoque_item)
                break
            else:
              print("Inválido!")
          except Exception as e:
            print(e)
      case 2:
        listar_produtos()
      case 3:
        listar_produtos()
        excluir = int(input("Digite o código do produto que deseja excluir: "))
        if excluir:
          remover_produto(excluir)
          print("Produto excluído com sucesso!")
      case 4:
        listar_produtos()
        atualizar = int(input("Digite o código do produto que deseja atualizar: "))
        if atualizar:
          nome_atualizar = str(input("Digite o novo nome do produto: ")).title()
          estoque_atualizar = int(input("Digite a nova quantidade do produto: "))
          if nome_atualizar and estoque_atualizar:
            atualizar_produto(atualizar, nome_atualizar, estoque_atualizar)
            print("Produto atualizado com sucesso!")
      case 5:
        print("Saindo..")
        break
      case _:
        print("Opção inválida!")
if __name__ == "__main__":
  criar_tabela()
  main()
  conn.close()
