import json
import os
import random

lista_perguntas = []
lista_usuarios = []
lista_ranking = []

"""
Menu principal com escolhas iniciais do jogo
"""

def menu_principal():
    while True:
        print("_"*50)
        print("QUIZ - Conhecimentos Gerais")
        print("_"*50)
        print("Escolha uma opção:")
        print("1 - Iniciar Jogo")
        print("2 - Ranking")
        print("3 - Sair")
        opcao = int(input().strip())
        if(opcao == 1):
                iniciar_jogo()
        elif(opcao == 2):
                mostrar_ranking()
        elif(opcao == 3):
                exit(1)

"""
Função principal que inicia o jogo
"""

def iniciar_jogo():
    print("_"*50)
    nome_jogador = input("Digite o nome do jogador: ").strip()
    pontuacao = 0
    perguntas = adicionar_perguntas()
    print("_"*50)
    print("Começando Jogo!")
    print("_"*50)

    #exibi cada uma das 9 perguntas selecionadas
    for pergunta in perguntas:
        print(pergunta["pergunta"])
        alternativas = pergunta["alternativas"]
        for alternativa in alternativas.keys():
            print(f'{alternativa} - {alternativas[alternativa]}')
        resposta = input("Qual a alternativa correta? ").strip()
        if(resposta == pergunta["resposta"]):
            pontuacao += pergunta["dificuldade"]
        print("_"*50)

    #Salva dados da pontuação do jogador e finaliza o jogo
    raking = {"jogador": nome_jogador, "pontuacao" : pontuacao}
    atualizarRank(raking)
    print(f'Você conseguiu {pontuacao} pontos! Parabéns!')
    input("Pressione qualquer tecla para voltar ao menu principal")
    menu_principal()

"""
Atualiza ranking com dados do jogador e pontuação
"""
def atualizarRank(ranking_atual):
    encontrou_jogador = False
    ranking_antigo = {}
    #checa se o jogador ja tem ranking cadastrado
    for rank in lista_ranking:
        if(rank["jogador"] == ranking_atual["jogador"]):
            encontrou_jogador = True
            ranking_antigo = rank
            break
    #Atualiza ranking se existente, caso contrario registra nova entrada
    if(encontrou_jogador == True):
        if(ranking_antigo["pontuacao"] < ranking_atual["pontuacao"]):
            lista_ranking.remove(rank)
            lista_ranking.append(ranking_atual)
    else:
        lista_ranking.append(ranking_atual)
    salvar_ranking()

"""
Retorna 9 perguntas aleatoriamente selecionadas do arquivo. 3 perguntas de cada dificuldade.
"""
def adicionar_perguntas():
    perguntas_faceis = []
    perguntas_medias = []
    perguntas_dificeis = []
    perguntas_selecionadas = []

    #separa as perguntas por dificuldades
    for pergunta in lista_perguntas:
        if(pergunta["dificuldade"] == 1):
            perguntas_faceis.append(pergunta)
        elif(pergunta["dificuldade"] == 2):
            perguntas_medias.append(pergunta)
        elif(pergunta["dificuldade"] == 3):
            perguntas_dificeis.append(pergunta)

    #seleciona 3 perguntas de cada dificuldade
    for num in range(3):
        indice = random.randrange(0, len(perguntas_faceis)-1)
        perguntas_selecionadas.append(perguntas_faceis[indice])
        perguntas_faceis.pop(indice)

    for num in range(3):
        indice = random.randrange(0, len(perguntas_medias)-1)
        perguntas_selecionadas.append(perguntas_medias[indice])
        perguntas_medias.pop(indice)

    for num in range(3):
        indice = random.randrange(0, len(perguntas_dificeis)-1)
        perguntas_selecionadas.append(perguntas_dificeis[indice])
        perguntas_dificeis.pop(indice)
    
    return perguntas_selecionadas

"""
Exibe ranking dos jogadores. So uma entrada é exibida por jogador, a ultima entrada
com maior pontuação
"""
def mostrar_ranking():
    print("_"*50)
    print("RANKING")
    print("_"*50)
    print("Jogador | Pontuação")
    
    posicao = 1
    #ordena pontuação
    lista_ranking.sort(key=lambda rank:rank["pontuacao"], reverse = True)
    for rank in lista_ranking:
        print(f'{posicao} - {rank["jogador"]} = {rank["pontuacao"]} pts')
        posicao +=1
    
"""
Carrega conteudo dos arquivos do jogo em variáveis temporárias
"""

def carregar_todos_arquivos():
    arquivo_perguntas = carregar_arquivo('perguntas.json')
    arquivo_ranking = carregar_arquivo('ranking.json')

    if(not arquivo_perguntas == ""):
        lista_perguntas.extend(json.loads(arquivo_perguntas))

    if(not arquivo_ranking == ""):
        lista_ranking.extend(json.loads(arquivo_ranking))
"""
Carrega conteudo de um arquivo passado como parametro
"""
def carregar_arquivo(nome_arquivo):
    conteudo_arquivo = ""
    if not os.path.exists(nome_arquivo):
        open(nome_arquivo, 'x')
    else:
        with open(nome_arquivo,  encoding="utf8") as f:
            conteudo_arquivo = f.read()
    return conteudo_arquivo

"""
Pega dados do ranking e salva em arquivo
"""
def salvar_ranking():
    
    with open('ranking.json', 'w') as convert_file:
        convert_file.write(json.dumps(lista_ranking))

carregar_todos_arquivos()
menu_principal()