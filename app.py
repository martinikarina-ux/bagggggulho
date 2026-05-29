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
    # 📥 Inicializa uma lista vazia local para estruturar o histórico antes de salvar
    historico = []
    
    # 👀 Verifica se o arquivo com os dados gravados já existe no computador
    if os.path.exists(HISTORICO_ARQUIVO):
        # 🛡️ Tenta abrir e ler o arquivo sem que erros parem o aplicativo
        try:
            # 📖 Abre o arquivo json em modo de leitura pura com padrão de texto UTF-8
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                # 🔄 Converte o texto JSON puro lido de volta em um array do Python
                historico = json.load(f)
        # 🧯 Caso ocorra falha de leitura (arquivo corrompido), ignora o erro
        except:
            # 🧹 Define a lista como vazia para reiniciar o arquivo com segurança
            historico = []

    # 📦 Cria o dicionário com os dados estruturados da medição atual (incluindo o emoji!)
    novo_item = {
        # 🔢 Salva o valor final calculado do IMC
        "imc": imc,
        # 📑 Mescla o emoji e o texto do diagnóstico em uma única linha
        "status": f"{emoji} {status}",
        # 📅 Captura e formata a data atual do sistema para o padrão Dia/Mês
        "data": datetime.now().strftime("%d/%m")
    }

    # 🔀 Adiciona o novo registro exatamente no índice 0 da lista (topo do histórico)
    historico.insert(0, novo_item)
    
    # 🛑 Limita o armazenamento para guardar apenas os últimos 5 registros
    if len(historico) > 5:
        # ✂️ Remove o último item da lista (o mais antigo de todos)
        historico.pop()

    # 💾 Abre ou cria o arquivo histórico em modo de escrita sobrescrevendo os dados
    with open(HISTORICO_ARQUIVO, "w", encoding="utf-8") as f:
        # ✍️ Converte e grava a lista no arquivo, preservando acentos e formatando o layout
        json.dump(historico, f, ensure_ascii=False, indent=4)
    
    # 🔄 Atualiza o painel do histórico na tela chamando a função responsável
    atualizar_tela_historico()

# 📂 Função que lê o arquivo local e desenha os dados na tela do aplicativo
def atualizar_tela_historico():
    # 📥 Inicializa uma lista vazia temporária para armazenar a leitura
    historico = []
    # 👀 Confere se existe um arquivo de registros na pasta do app
    if os.path.exists(HISTORICO_ARQUIVO):
        # 🛡️ Inicia tratamento de exceção para evitar travamentos no carregamento
        try:
            # 📖 Abre o arquivo de texto em modo de leitura
            with open(HISTORICO_ARQUIVO, "r", encoding="utf-8") as f:
                # 🔄 Converte os dados de texto lidos em objetos válidos de Python
                historico = json.load(f)
        # 🧯 Trata possíveis erros de formatação no arquivo
        except:
            # 🧹 Mantém o array zerado caso a leitura falhe
            historico = []

    # 🧼 Desbloqueia a caixa de texto para que o script possa alterá-la
    caixa_historico.config(state=tk.NORMAL)
    # 🧼 Limpa a área de texto inteira, do primeiro caractere (1.0) até o fim (tk.END)
    caixa_historico.delete("1.0", tk.END)

    # 📭 Faz uma validação lógica simples se a lista retornou vazia
    if not historico:
        # ✍️ Escreve uma mensagem amigável avisando sobre a ausência de picos
        caixa_historico.insert(tk.END, "🌫️ histórico vazio... nenhum pico registrado ainda.\n")
    # 📋 Caso existam registros na lista, entra em modo de repetição
    else:
        # 🔄 Loop clássico que passa por cada bloco de dicionário dentro da lista
        for item in historico:
            # 🧾 Monta uma linha compacta e cheia de atitude para o painel
            linha = f" 🗓️ {item['data']} ➡️ imc: {item['imc']} | {item['status']}\n"
            # 📌 Adiciona a linha criada logo no fim do texto exibido na caixa
            caixa_historico.insert(tk.END, linha)
            
    # 🔒 Bloqueia a caixa de texto para que o usuário não consiga digitar nela manualmente
    caixa_historico.config(state=tk.DISABLED)

# 🧮 Função principal acionada ao clicar no botão "calcular imc"
def calcular_imc():
    # 🛡️ Abre um bloco try para validar as entradas numéricas digitadas pelo usuário
    try:
        # 📥 Captura os caracteres do campo peso e tenta convertê-los para float
        peso = float(entry_peso.get())
        # 📥 Captura os caracteres do campo altura e tenta convertê-los para float
        altura = float(entry_altura.get())
    # 🧯 Executa esse bloco caso o usuário envie letras ou campos vazios
    except ValueError:
        # ⚠️ Exibe um pop-up clássico de sistema alertando o erro de digitação
        messagebox.showerror("❌ erro", "🚨 insira números reais e válidos, por favor!")
        # 🛑 Aborta o restante do cálculo imediatamente
        return

    # 🚫 Verifica se as entradas numéricas são menores ou iguais a zero
    if peso <= 0 or altura <= 0:
        # ⚠️ Exibe uma caixa de erro explicando a inconsistência física dos dados
        messagebox.showerror("❌ erro", "🚨 peso ou altura não podem ser zero ou negativos!")
        # 🛑 Para a execução da função
        return

    # 📐 Executa o cálculo matemático oficial do IMC: Peso dividido pelo quadrado da altura
    resultado_imc = peso / (altura * altura)
    # 🛠️ Formata e arredonda o número float obtido para uma única casa decimal
    imc_formatado = f"{resultado_imc:.1f}"

    # 🚦 Central de tomadas de decisão baseada na estética de cores e emojis do BRAT
    if resultado_imc < 18.5:
        # 🥗 Atribui o diagnóstico textual correspondente
        status = "abaixo do peso"
        # 🥗 Escolhe o emoji principal do status
        emoji = "🥗"
        # 🥗 Define a frase de conselho personalizada
        conselho = "🍏 foque na sua saúde! busque uma nutrição fortalecida e potente. ✨"
    # 🚦 Avalia se o resultado se encaixa na faixa considerada saudável
    elif 18.5 <= resultado_imc < 25:
        # 🔋 Define a identificação do peso normal
        status = "peso normal"
        # 🔋 Associa o emoji do status estável
        emoji = "🔋"
        # 🔋 Define o conselho animado voltado para a pista de dança
        conselho = "🟩 clubber saudável! tudo certo, mantenha o ritmo e quebre tudo na pista. 🏎️"
    # 🚦 Avalia se o resultado corresponde à faixa de sobrepeso
    elif 25 <= resultado_imc < 30:
        # ⚡ Define o rótulo do status moderado
        status = "sobrepeso"
        # ⚡ Atribui a frase com orientações de atividades físicas cotidianas
        conselho = "🏃 de olho na rotina! se movimentar faz bem para o corpo e para a mente. 🔥"
        # ⚡ Define o emoji elétrico de atenção
        emoji = "⚡"
    # 🚦 Entra aqui caso o valor seja igual ou superior a 30
    else:
        # 🩺 Define o status clínico de obesidade
        status = "obesidade"
        # 🩺 Seleciona o emoji médico para o diagnóstico
        emoji = "🩺"
        # 🩺 Define o conselho focado no cuidado e monitoramento profissional
        conselho = "💥 atenção redobrada! consulte profissionais para te dar aquele apoio. ❤️"

    # ✍️ Atualiza o texto do valor do IMC centralizado com os emojis correspondentes
    label_resultado_valor.config(text=f"{emoji} imc: {imc_formatado} {emoji}")
    # ✍️ Atualiza o texto da classificação forçando caixa alta usando a função .upper()
    label_resultado_status.config(text=f"» status: {status.upper()} «")
    # ✍️ Insere a frase do conselho na base do painel de resultados
    label_resultado_conselho.config(text=conselho)

    # 💾 Dispara o salvamento permanente desses resultados enviando-os para o arquivo
    salvar_no_historico(imc_formatado, status, emoji)

# 🗑️ Função acionada pelo botão de apagar o histórico de registros
def limpar_historico():
    # 👀 Confere se o arquivo json físico existe gravado no disco
    if os.path.exists(HISTORICO_ARQUIVO):
        # 🗑️ Executa a remoção definitiva do arquivo do sistema operacional
        os.remove(HISTORICO_ARQUIVO)
    
    # 🧹 Limpa os textos da tela redefinindo o rótulo do valor do IMC para vazio
    label_resultado_valor.config(text="")
    # 🧹 Apaga a linha da classificação textual exibida na interface
    label_resultado_status.config(text="")
    # 🧹 Apaga a frase de conselho ativa na tela do aplicativo
    label_resultado_conselho.config(text="")
    
    # 🔄 Atualiza a interface gráfica do histórico para exibir o estado resetado
    atualizar_tela_historico()

# 🪩 ANIMAÇÃO BÔNUS: Faz o título piscar simulando luzes estroboscópicas de balada
def animar_titulo(estado=0):
    # 🎨 Cria um ciclo de cores alternando o verde limão oficial e o preto absoluto
    cores = ["#21fd0d", "#000000", "#21fd0d", "#21fd0d"]
    # 🎨 Aplica na propriedade fg (foreground) a cor correspondente ao ciclo atual
    label_titulo.config(fg=cores[estado % len(cores)])
    # ⏱️ Agenda a própria função para rodar novamente de forma cíclica em 600 milissegundos
    root.after(600, lambda: animar_titulo(estado + 1))


# 🖥️ Configurações Iniciais da Janela do Aplicativo (Tkinter)
root = tk.Tk()
# 🏷️ Aplica o título conceitual que aparecerá no topo da barra do sistema
root.title("brat imc")
# 📐 Modifica o tamanho padrão de abertura da janela (largura x altura em pixels)
root.geometry("480x680")
# 🖤 Altera a cor de fundo nativa da janela para preto total
root.configure(bg="#000000")

# 🟢 Paleta de Cores Oficial BRAT
COR_FUNDO = "#000000"
# 🟢 Código hexadecimal do verde ácido customizado do álbum
COR_BRAT = "#21fd0d" 
# 🟢 Cria uma tupla com as especificações de estilo para as legendas padrões
FONTE_LABEL = ("Franklin Gothic Medium", 13, "bold")
# 🟢 Cria uma tupla com as especificações de tamanho para as caixas de digitação
FONTE_INPUT = ("Franklin Gothic Medium", 15)

# 🎤 Cria a tag de texto do título acoplada à tela do aplicativo
label_titulo = tk.Label(root, text="brat imc", font=("Franklin Gothic Medium", 48, "bold"), bg=COR_FUNDO, fg=COR_BRAT)
# 📐 Renderiza o título adicionando espaçamentos internos verticais controlados
label_titulo.pack(pady=(25, 15))

# ⚖️ Cria a legenda textual explicativa para orientar a entrada do peso
label_peso = tk.Label(root, text="⚖️ insira seu peso (kg):", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_BRAT)
# 📐 Alinha a legenda à esquerda (West) definindo margens externas de recuo
label_peso.pack(anchor="w", padx=45, pady=(10, 2))
# ⌨️ Cria o campo de entrada editável configurando a cor verde do cursor de digitação
entry_peso = tk.Entry(root, font=FONTE_INPUT, bg=COR_FUNDO, fg=COR_BRAT, insertbackground=COR_BRAT, borderwidth=2, relief="solid")
# 📐 Estica a barra horizontalmente para preencher a tela mantendo recuos laterais
entry_peso.pack(fill="x", padx=45, pady=(0, 10))

# 📏 Cria a legenda explicativa voltada ao recebimento da altura do usuário
label_altura = tk.Label(root, text="📏 insira sua altura (m):", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_BRAT)
# 📐 Alinha o texto do rótulo à esquerda da interface
label_altura.pack(anchor="w", padx=45, pady=(10, 2))
# ⌨️ Constrói a caixa de digitação para a inserção dos dados de altura
entry_altura = tk.Entry(root, font=FONTE_INPUT, bg=COR_FUNDO, fg=COR_BRAT, insertbackground=COR_BRAT, borderwidth=2, relief="solid")
# 📐 Posiciona a caixa expandindo em largura e definindo espaçamento inferior
entry_altura.pack(fill="x", padx=45, pady=(0, 20))

# ⚡ Cria o botão com as propriedades invertidas (fundo verde ácido e texto preto)
btn_calcular = tk.Button(root, text="⚡ calcular imc ⚡", font=("Franklin Gothic Medium", 14, "bold"), bg=COR_BRAT, fg=COR_FUNDO, activebackground=COR_BRAT, activeforeground=COR_FUNDO, relief="flat", command=calcular_imc)
# 📐 Insere o botão na tela expandindo-o para ocupar o bloco horizontal completo
btn_calcular.pack(fill="x", padx=45, pady=5)

# 📊 Painel de Exibição dos Resultados: Cria o espaço que receberá o número do IMC
label_resultado_valor = tk.Label(root, text="", font=("Franklin Gothic Medium", 22, "bold"), bg=COR_FUNDO, fg=COR_BRAT)
# 📐 Organiza o elemento visual na tela definindo folga nas bordas
label_resultado_valor.pack(pady=(15, 2))

# 📊 Cria o rótulo de texto encarregado de mostrar a classificação por extenso
label_resultado_status = tk.Label(root, text="", font=("Franklin Gothic Medium", 14, "bold"), bg=COR_FUNDO, fg=COR_BRAT)
# 📐 Posiciona a linha do diagnóstico na árvore visual
label_resultado_status.pack(pady=2)

# 📊 Cria o campo para o conselho de saúde, limitando a quebra de linha em 380 pixels
label_resultado_conselho = tk.Label(root, text="", font=("Franklin Gothic Medium", 11, "italic"), bg=COR_FUNDO, fg=COR_BRAT, wraplength=380)
# 📐 Fixa o campo do conselho aplicando margem de afastamento na base
label_resultado_conselho.pack(pady=(2, 15))

# 📜 Cria a legenda fixa que intitula o painel de registros armazenados
label_historico_titulo = tk.Label(root, text="📜 histórico de picos:", font=FONTE_LABEL, bg=COR_FUNDO, fg=COR_BRAT)
# 📐 Alinha o título do histórico à esquerda da janela gráfica
label_historico_titulo.pack(anchor="w", padx=45, pady=(10, 5))

# 📋 Constrói um componente de bloco de texto para comportar os itens do arquivo json
caixa_historico = tk.Text(root, height=5, font=("Courier New", 11, "bold"), bg=COR_FUNDO, fg=COR_BRAT, bd=0, highlightthickness=0)
# 📐 Fixa o painel de texto esticando na horizontal dentro do limite definido pelos paddings
caixa_historico.pack(fill="x", padx=45)
# 🔒 Desativa por padrão a digitação manual sobre este bloco de texto
caixa_historico.config(state=tk.DISABLED)

# 🗑️ Cria o botão vazado de limpeza aplicando uma borda sólida fina de 1 pixel
btn_limpar = tk.Button(root, text="🗑️ limpar histórico", font=("Franklin Gothic Medium", 10, "bold"), bg=COR_FUNDO, fg=COR_BRAT, activebackground=COR_BRAT, activeforeground=COR_FUNDO, bd=1, relief="solid", command=limpar_historico)
# 📐 Posiciona o botão de limpeza na base da interface estrutural do programa
btn_limpar.pack(pady=(15, 20))

# 🔄 Roda o carregamento inicial buscando dados no arquivo assim que o app liga
atualizar_tela_historico()
# 🪩 Liga o gatilho da rotina de animação para iniciar a oscilação de cor do título
animar_titulo()

# ♾️ Inicia a escuta contínua de eventos do aplicativo, mantendo a janela rodando e ativa
root.mainloop()