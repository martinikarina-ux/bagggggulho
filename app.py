# 📦 Importa a biblioteca padrão para criação de interfaces gráficas
import tkinter as tk
# ⚠️ Importa o módulo de caixas de mensagem para exibir alertas de erro
from tkinter import messagebox
# 📅 Importa o módulo de data para registrar os momentos dos cálculos
from datetime import datetime
# 📂 Importa o módulo json para salvar e ler o histórico em um arquivo local
import json
# 🗺️ Importa o módulo os para verificar a existência de arquivos no sistema
import os

# 📂 Define o arquivo de armazenamento no mesmo diretório do app.py
HISTORICO_ARQUIVO = "brat_imc_history.json"

# 💾 Função responsável por salvar uma nova medição no arquivo JSON local
def salvar_no_historico(imc, status, emoji):
    historico = []
    
    # 👀 Verifica se o histórico já existe para não sobrescrever do zero
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except:
            historico = []

    # 📦 Cria o dicionário com os dados estruturados da medição atual (incluindo o emoji!)
    novo_item = {
        "imc": imc,
        "status": f"{emoji} {status}",
        "data": datetime.now().strftime("%d/%m")
    }

    # 🔀 Adiciona o novo registro no início da lista 
    historico.insert(0, novo_item)
    
    # 🛑 Limita o armazenamento para guardar apenas os últimos 5 registros
    if len(historico) > 5:
        historico.pop()

    # 💾 Grava os dados atualizados de volta no arquivo
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)
    
    # 🔄 Atualiza o painel do histórico na tela
    atualizar_tela_historico()

# 📂 Função que lê o arquivo local e desenha os dados na tela do aplicativo
def atualizar_tela_historico():
    historico = []
    if os.path.exists(HISTORICO_ARQUIVO):
        try:
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except:
            historico = []

    # 🧼 Desbloqueia, limpa e atualiza a caixa de texto
    caixa_historico.config(state=tk.NORMAL)
    caixa_historico.delete("1.0", tk.END)

    if not historico:
        caixa_historico.insert(tk.END, "🌫️ histórico vazio... nenhum pico registrado ainda.\n")
    else:
        for item in historico:
            # 🧾 Monta uma linha compacta e cheia de atitude para o painel
            linha = f" 🗓️ {item['data']} ➡️ imc: {item['imc']} | {item['status']}\n"
            caixa_historico.insert(tk.END, linha)
            
    caixa_historico.config(state=tk.DISABLED)

# 🧮 Função principal acionada ao clicar no botão "calcular imc"
def calcular_imc():
    try:
        peso = float(entry_peso.get())
        altura = float(entry_altura.get())
    except ValueError:
        # ⚠️ Mensagem de erro customizada com estética direta
        messagebox.showerror("❌ erro", "🚨 insira números reais e válidos, por favor!")
        return

    if peso <= 0 or altura <= 0:
        messagebox.showerror("❌ erro", "🚨 peso ou altura não podem ser zero ou negativos!")
        return

    # 📐 Executa o cálculo matemático oficial do IMC
    resultado_imc = peso / (altura * altura)
    imc_formatado = f"{resultado_imc:.1f}"

    # 🚦 Central de tomadas de decisão baseada na estética de cores e emojis do BRAT
    if resultado_imc < 18.5:
        status = "abaixo do peso"
        emoji = "🥗"
        conselho = "🍏 foque na sua saúde! busque uma nutrição fortalecida e potente. ✨"
    elif 18.5 <= resultado_imc < 25:
        status = "peso normal"
        emoji = "🔋"
        conselho = "🟩 clubber saudável! tudo certo, mantenha o ritmo e quebre tudo na pista. 🏎️"
    elif 25 <= resultado_imc < 30:
        status = "sobrepeso"
        conselho = "🏃 de olho na rotina! se movimentar faz bem para o corpo e para a mente. 🔥"
        emoji = "⚡"
    else:
        status = "obesidade"
        emoji = "🩺"
        conselho = "💥 atenção redobrada! consulte profissionais para te dar aquele apoio. ❤️"

    # ✍️ Transforma a interface exibindo os resultados em caixa alta e cheia de emojis
    label_resultado_valor.config(text=f"{emoji} imc: {imc_formatado} {emoji}")
    label_resultado_status.config(text=f"» status: {status.upper()} «")
    label_resultado_conselho.config(text=conselho)

    # 💾 Salva os novos dados diretamente no arquivo JSON
    salvar_no_historico(imc_formatado, status, emoji)

# 🗑️ Função acionada pelo botão de apagar o histórico de registros
def limpar_historico():
    if os.path.exists(HISTORICO_ARQUIVO):
        os.remove(HISTORICO_ARQUIVO)
    
    # 🧹 Reseta o painel principal de resultados junto com o histórico
    label_resultado_valor.config(text="")
    label_resultado_status.config(text="")
    label_resultado_conselho.config(text="")
    
    atualizar_tela_historico()

# 🪩 ANIMAÇÃO BÔNUS: Faz o título piscar simulando luzes estroboscópicas de balada
def animar_titulo(estado=0):
    # Alterna as cores entre o verde limão clássico e o preto do álbum
    cores = ["#21fd0d", "#000000", "#21fd0d", "#21fd0d"]
    label_titulo.config(fg=cores[estado % len(cores)])
    # Executa a função novamente a cada 600 milissegundos
    root.after(600, lambda: animar_titulo(estado + 1))


# 🖥️ Configurações Iniciais da Janela do Aplicativo (Tkinter)
root = tk.Tk()
root.title("brat imc")
root.geometry("480x680")
root.configure(bg="#000000")

# 🟢 Paleta de Cores Oficial BRAT
COR_FUNDO = "#000000"
COR_BRAT = "#21fd0d" 
FONTE_LABEL = ("Franklin Gothic Medium", 13, "bold")
FONTE_INPUT = ("Franklin Gothic Medium", 15)

# 🎤 Rótulo do Título Principal (Agora animado e dinâmico!)
label_titulo = tk.Label(root, text="brat imc", font=("Franklin Gothic Medium", 48, "bold"), bg=COR_FUNDO, fg=COR_BRAT)
label_titulo.pack(pady=(25, 15))

# ⚖️ Seção de entrada de dados: Peso
label_peso = tk.Label(root, text="⚖️ insira seu peso (kg):", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_BRAT)
label_peso.pack(anchor="w", padx=45, pady=(10, 2))
entry_peso = tk.Entry(root, font=FONTE_INPUT, bg=COR_FUNDO, fg=COR_BRAT, insertbackground=COR_BRAT, borderwidth=2, relief="solid")
entry_peso.pack(fill="x", padx=45, pady=(0, 10))

# 📏 Seção de entrada de dados: Altura
label_altura = tk.Label(root, text="📏 insira sua altura (m):", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_BRAT)
label_altura.pack(anchor="w", padx=45, pady=(10, 2))
entry_altura = tk.Entry(root, font=FONTE_INPUT, bg=COR_FUNDO, fg=COR_BRAT, insertbackground=COR_BRAT, borderwidth=2, relief="solid")
entry_altura.pack(fill="x", padx=45, pady=(0, 20))

# ⚡ Botão de Calcular (Estilo Bloco Contraste)
btn_calcular = tk.Button(root, text="⚡ calcular imc ⚡", font=("Franklin Gothic Medium", 14, "bold"), bg=COR_BRAT, fg=COR_FUNDO, activebackground=COR_BRAT, activeforeground=COR_FUNDO, relief="flat", command=calcular_imc)
btn_calcular.pack(fill="x", padx=45, pady=5)

# 📊 Painel de Exibição dos Resultados (Mais vivo e espaçado)
label_resultado_valor = tk.Label(root, text="", font=("Franklin Gothic Medium", 22, "bold"), bg=COR_FUNDO, fg=COR_BRAT)
label_resultado_valor.pack(pady=(15, 2))

label_resultado_status = tk.Label(root, text="", font=("Franklin Gothic Medium", 14, "bold"), bg=COR_FUNDO, fg=COR_BRAT)
label_resultado_status.pack(pady=2)

label_resultado_conselho = tk.Label(root, text="", font=("Franklin Gothic Medium", 11, "italic"), bg=COR_FUNDO, fg=COR_BRAT, wraplength=380)
label_resultado_conselho.pack(pady=(2, 15))

# 📜 Seção de Histórico de Picos
label_historico_titulo = tk.Label(root, text="📜 histórico de picos:", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_BRAT)
label_historico_titulo.pack(anchor="w", padx=45, pady=(10, 5))

# 📋 Janela de texto interna com fonte monoespaçada estilo terminal hacker/clubber
caixa_historico = tk.Text(root, height=5, font=("Courier New", 11, "bold"), bg=COR_FUNDO, fg=COR_BRAT, bd=0, highlightthickness=0)
caixa_historico.pack(fill="x", padx=45)
caixa_historico.config(state=tk.DISABLED)

# 🗑️ Botão para deletar os arquivos e limpar a tela
btn_limpar = tk.Button(root, text="🗑️ limpar histórico", font=("Franklin Gothic Medium", 10, "bold"), bg=COR_FUNDO, fg=COR_BRAT, activebackground=COR_BRAT, activeforeground=COR_FUNDO, bd=1, relief="solid", command=limpar_historico)
btn_limpar.pack(pady=(15, 20))

# 🔄 Ativa as funções automáticas de inicialização do app
atualizar_tela_historico()
animar_titulo()

# ♾️ Inicia a aplicação
root.mainloop()