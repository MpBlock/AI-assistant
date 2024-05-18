import os
import pyttsx3
import datetime
import webbrowser
import wikipedia
import random

# Configuração para a língua portuguesa
wikipedia.set_lang("pt")

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def pesquisar_no_google(pergunta):
    termo_pesquisa = '+'.join(pergunta.split())
    url = f"https://www.google.com/search?q={termo_pesquisa}"
    webbrowser.open(url)

def pesquisar_na_wikipedia(termo):
    try:
        pesquisa = wikipedia.summary(termo, sentences=2)
        falar(pesquisa)
    except wikipedia.exceptions.DisambiguationError as e:
        falar("Houve uma ambiguidade na busca. Por favor, seja mais específico.")
    except wikipedia.exceptions.PageError as e:
        falar("Desculpe, não encontrei informações sobre isso na Wikipédia.")

def cumprimento():
    agora = datetime.datetime.now()
    hora = agora.hour
    if hora < 12:
        return 'Bom dia!'
    elif 12 <= hora < 18:
        return 'Boa tarde!'
    else:
        return 'Boa noite!'

def selecionar_piada():
    # Lista de piadas
    piadas = [
        "Por que o gato não gosta de máquinas? Porque tem medo do mouse!",
        "Qual é o contrário de volátil? Vem cá sobrinho.",
        "Por que o papel higiênico foi no psicólogo? Porque estava sempre no mesmo rolo.",
        "O que o lápis disse para o papel? Deixa eu te contar uma história.",
        "Qual é o cúmulo da velocidade? Fazer uma ultrapassagem a pé!",
        "Por que a matemática é tão estressante? Porque tem muitos problemas.",
        "O que é um pontinho preto no microscópio? Uma micro ponto preta.",
        "Qual é o fim da picada? Quando o mosquito vai embora."
    ]
    # Selecionar uma piada aleatória
    return random.choice(piadas)


def pesquisar_no_youtube(termo):
    termo_pesquisa = '+'.join(termo.split())
    url = f"https://www.youtube.com/results?search_query={termo_pesquisa}"
    webbrowser.open(url)

def processar_resposta(resposta, nome):
    if resposta == '1':
        falar('Por favor, diga o que você gostaria de pesquisar no Google:')
        pergunta = input('Digite sua pergunta: ')
        pesquisar_no_google(pergunta)
        falar('A pesquisa foi realizada no Google.')
    elif resposta == '2':
        piada = selecionar_piada()
        falar(piada)
    elif resposta == '3':
        agora = datetime.datetime.now()
        hora = agora.strftime("%H:%M")
        falar(f'{nome}, são {hora}.')
    elif resposta == '4':
        falar('O que você gostaria de pesquisar na Wikipédia?')
        termo = input('Digite o termo: ')
        pesquisar_na_wikipedia(termo)
    elif resposta == '5':
        falar('O que você gostaria de pesquisar no YouTube?')
        termo = input('Digite o termo: ')
        pesquisar_no_youtube(termo)
        falar('A pesquisa foi realizada no YouTube.')
    else:
        falar('Digite apenas 1, 2, 3, 4 ou 5')

    # Perguntar se precisa de mais alguma coisa
    falar('Precisa de mais alguma coisa?')

def start():
    # Apresentar o chatbot
    falar(f'{cumprimento()} Bem-vindo à Assistente Flip')

    # Pedir o nome
    falar('Qual é o seu nome?')
    nome = input('Digite seu nome: ')
    falar(f'Olá, {nome}!')

    while True:
        # Perguntar em que posso ajudar
        falar('Em que posso ajudar?')

        while True:
            # Oferecer o menu de opções
            resposta = input(f'[1] - pesquisar no Google{os.linesep}[2] - me conte uma piada{os.linesep}'
                            f'[3] - que horas são?{os.linesep}[4] - o que significa algo?{os.linesep}'
                            f'[5] - pesquisar no YouTube{os.linesep}')
            processar_resposta(resposta, nome)

            # Perguntar se precisa de mais alguma coisa
            mais_alguma_coisa = input('Precisa de mais alguma coisa? ').lower()
            while mais_alguma_coisa not in ['sim', 'não']:
                falar('Por favor, responda sim ou não.')
                mais_alguma_coisa = input('Precisa de mais alguma coisa? ').lower()

            if mais_alguma_coisa == 'não':
                falar('Ok, estou aqui se precisar de mais alguma coisa.')
                break
            elif mais_alguma_coisa == 'sim':
                falar('Em que posso ajudar?')

        # Perguntar se deseja iniciar uma nova conversa
        nova_conversa = input('Para iniciar uma nova conversa, digite "flip". Para sair, digite "sair": ').lower()
        if nova_conversa != 'flip':
            falar('Até logo!')
            break

if __name__ == '__main__':
    start()