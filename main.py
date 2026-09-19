#-------------------------------------------------------------------------------------------------#
import tkinter as tk
from tkinter import messagebox, ttk

# VETOR (Lista 1D) armazenando os nomes dos perfis
perfis = ["Solo", "Duo", "Família"]

# MATRIZ TRIDIMENSIONAL (Lista de Matrizes 2D) com as listas padrão
listas_padrao = [
    # 0 - Matriz Solo
    [
        ["Arroz", "1kg"],
        ["Feijão", "1kg"],
        ["Macarrão", "500g"],
        ["Ovos", "12 unidades"],
        ["Leite", "2 litros"],
        ["Café", "250g"],
        ["Papel Higiênico", "4 rolos"],
    ],
    # 1 - Matriz Duo
    [
        ["Arroz", "2kg"],
        ["Feijão", "2kg"],
        ["Macarrão", "1kg"],
        ["Ovos", "24 unidades"],
        ["Leite", "4 litros"],
        ["Café", "500g"],
        ["Papel Higiênico", "8 rolos"],
        ["Óleo", "1 unidade"],
    ],
    # 2 - Matriz Família
    [
        ["Arroz", "5kg"],
        ["Feijão", "4kg"],
        ["Macarrão", "2kg"],
        ["Ovos", "30 unidades"],
        ["Leite", "12 litros"],
        ["Café", "1kg"],
        ["Papel Higiênico", "16 rolos"],
        ["Óleo", "3 unidades"],
        ["Sabão em pó", "2kg"],
        ["Carnes", "4kg"],
    ],
]


class SupermercadoApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Supermercado Fácil")
    self.root.geometry("500x620")
    self.root.config(bg="#f0f0f0")

    # Variáveis de controle
    self.matriz_atual = []
    self.nome_perfil = ""

    # Inicia exibindo a tela de seleção de perfis
    self.criar_tela_selecao()

  def limpar_janela(self):
    """Remove todos os elementos da janela atual"""
    for widget in self.root.winfo_children():
      widget.destroy()

  def criar_tela_selecao(self):
    """Tela inicial para escolha do perfil"""
    self.limpar_janela()

    lbl_titulo = tk.Label(
        self.root,
        text="🛒 SUPERMERCADO FÁCIL 🛒",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0",
        fg="#333",
    )
    lbl_titulo.pack(pady=30)

    lbl_sub = tk.Label(
        self.root,
        text="Escolha a categoria que melhor define sua residência:",
        font=("Arial", 11),
        bg="#f0f0f0",
    )
    lbl_sub.pack(pady=10)

    # Botões para cada perfil do vetor
    for i, perfil in enumerate(perfis):
      btn = tk.Button(
          self.root,
          text=f"Perfil: {perfil}",
          font=("Arial", 12),
          bg="#4CAF50",
          fg="white",
          width=22,
          height=2,
          command=lambda idx=i: self.selecionar_perfil(idx),
      )
      btn.pack(pady=10)

  def selecionar_perfil(self, idx):
    """Processa a escolha do perfil e carrega a matriz correspondente"""
    self.nome_perfil = perfis[idx]
    # Copiando a MATRIZ padrão correspondente para a matriz atual
    self.matriz_atual = [linha[:] for linha in listas_padrao[idx]]
    self.criar_tela_principal()

  def criar_tela_principal(self):
    """Tela principal com a lista de compras e opções de gerenciamento"""
    self.limpar_janela()

    # Cabeçalho com o perfil selecionado
    frame_top = tk.Frame(self.root, bg="#f0f0f0")
    frame_top.pack(fill=tk.X, padx=20, pady=10)

    lbl_perfil = tk.Label(
        frame_top,
        text=f"📋 Perfil Ativo: {self.nome_perfil}",
        font=("Arial", 12, "bold"),
        bg="#f0f0f0",
        fg="#2c3e50",
    )
    lbl_perfil.pack(side=tk.LEFT)

    # Tabela (Treeview) para exibir a Matriz (Produto e Quantidade)
    frame_lista = tk.Frame(self.root)
    frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

    self.tree = ttk.Treeview(
        frame_lista, columns=("Produto", "Quantidade"), show="headings", height=10
    )
    self.tree.heading("Produto", text="Produto")
    self.tree.heading("Quantidade", text="Quantidade")
    self.tree.column("Produto", width=250, anchor="w")
    self.tree.column("Quantidade", width=150, anchor="center")

    scrollbar = ttk.Scrollbar(
        frame_lista, orient=tk.VERTICAL, command=self.tree.yview
    )
    self.tree.configure(yscroll=scrollbar.set)

    self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    self.atualizar_tabela()

    # Seção para Adicionar Produto
    frame_add = tk.LabelFrame(
        self.root,
        text=" Adicionar Novo Produto ",
        bg="#f0f0f0",
        font=("Arial", 10, "bold"),
    )
    frame_add.pack(fill=tk.X, padx=20, pady=10)

    tk.Label(frame_add, text="Produto:", bg="#f0f0f0").grid(
        row=0, column=0, sticky="w", padx=10, pady=5
    )
    self.entry_produto = tk.Entry(frame_add, width=22, font=("Arial", 11))
    self.entry_produto.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame_add, text="Quantidade:", bg="#f0f0f0").grid(
        row=1, column=0, sticky="w", padx=10, pady=5
    )
    self.entry_qtd = tk.Entry(frame_add, width=22, font=("Arial", 11))
    self.entry_qtd.grid(row=1, column=1, padx=5, pady=5)

    btn_adicionar = tk.Button(
        frame_add,
        text="Adicionar",
        bg="#2196F3",
        fg="white",
        font=("Arial", 10, "bold"),
        width=12,
        command=self.adicionar_produto_gui,
    )
    btn_adicionar.grid(row=0, column=2, rowspan=2, padx=15, pady=5)

    # Botões de Ação Inferiores (Remover e Finalizar)
    frame_acoes = tk.Frame(self.root, bg="#f0f0f0")
    frame_acoes.pack(fill=tk.X, padx=20, pady=10)

    btn_remover = tk.Button(
        frame_acoes,
        text="Remover Selecionado",
        bg="#f44336",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.remover_produto_gui,
    )
    btn_remover.pack(side=tk.LEFT, padx=5)

    btn_finalizar = tk.Button(
        frame_acoes,
        text="Finalizar e Ver Resumo",
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
        command=self.exibir_resumo_gui,
    )
    btn_finalizar.pack(side=tk.RIGHT, padx=5)

  def atualizar_tabela(self):
    """Atualiza os dados mostrados na tabela com base na matriz atual"""
    for item in self.tree.get_children():
      self.tree.delete(item)
    for produto, quantidade in self.matriz_atual:
      self.tree.insert("", tk.END, values=(produto, quantidade))

  def adicionar_produto_gui(self):
    """Adiciona um item coletado na interface para dentro da matriz"""
    produto = self.entry_produto.get().strip().title()
    quantidade = self.entry_qtd.get().strip()

    if produto and quantidade:
      # Adiciona nova linha na matriz
      self.matriz_atual.append([produto, quantidade])
      self.atualizar_tabela()

      # Limpa os campos
      self.entry_produto.delete(0, tk.END)
      self.entry_qtd.delete(0, tk.END)
      messagebox.showinfo("Sucesso", f"✅ {produto} adicionado com sucesso!")
    else:
      messagebox.showwarning(
          "Aviso", "Preencha tanto o nome do produto quanto a quantidade!"
      )

  def remover_produto_gui(self):
    """Remove o item selecionado na tabela da matriz"""
    selecionado = self.tree.selection()
    if not selecionado:
      messagebox.showwarning(
          "Aviso", "Por favor, selecione um produto na tabela para remover!"
      )
      return

    item = self.tree.item(selecionado)
    produto_nome = item["values"][0]

    # Percorrendo a MATRIZ de trás para frente para remover a ocorrência
    for i in range(len(self.matriz_atual) - 1, -1, -1):
      if self.matriz_atual[i][0] == produto_nome:
        del self.matriz_atual[i]
        break

    self.atualizar_tabela()
    messagebox.showinfo("Sucesso", f"❌ {produto_nome} removido com sucesso!")

  def exibir_resumo_gui(self):
    """Gera uma janela de resumo final igual ao modelo do console"""
    total_itens = len(self.matriz_atual)

    resumo_texto = f"Perfil selecionado: {self.nome_perfil}\n"
    resumo_texto += f"Total de itens distintos: {total_itens}\n\n"
    resumo_texto += "Itens da compra:\n"

    for produto, quantidade in self.matriz_atual:
      resumo_texto += f"-> {produto} (Quantidade: {quantidade})\n"

    resumo_texto += (
        "\nObrigado por usar o Supermercado Fácil! O aplicativo será encerrado."
    )

    messagebox.showinfo("🛒 Resumo da Compra", resumo_texto)
    self.root.destroy()  # Fecha a aplicação


#-------------------------------------------------------------------------------------------------#
if __name__ == "__main__":
  root = tk.Tk()
  app = SupermercadoApp(root)
  root.mainloop()
#-------------------------------------------------------------------------------------------------#
