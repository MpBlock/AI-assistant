import os
import pyttsx3
import datetime
import webbrowser
import wikipedia
import random
import speech_recognition as sr

# Configuração para a língua portuguesa
wikipedia.set_lang("pt")

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Diga algo...")
        audio = recognizer.listen(source)
    
    try:
        texto = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse: ", texto)
        return texto
    except sr.UnknownValueError:
        print("Não foi possível entender a fala.")
        return ""
    except sr.RequestError as e:
        print("Erro no serviço de reconhecimento de fala; {0}".format(e))
        return ""

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

def processar_resposta(resposta, nome):
    if 'pesquisar' in resposta:
        falar('Por favor, diga o que você gostaria de pesquisar no Google:')
        pergunta = ouvir()
        if pergunta:
            pesquisar_no_google(pergunta)
            falar('A pesquisa foi realizada no Google.')
        else:
            falar('Desculpe, não entendi sua pergunta.')
    elif 'piada' in resposta:
        piada = selecionar_piada()
        falar(piada)
    elif 'horas' in resposta:
        agora = datetime.datetime.now()
        hora = agora.strftime("%H:%M")
        falar(f'{nome}, são {hora}.')
    elif 'wikipédia' in resposta or 'significa' in resposta:
        falar('O que você gostaria de pesquisar na Wikipédia?')
        termo = ouvir()
        if termo:
            pesquisar_na_wikipedia(termo)
        else:
            falar('Desculpe, não entendi o termo.')
    else:
        falar('Desculpe, não entendi sua solicitação.')

    # Perguntar se precisa de mais alguma coisa
    falar('Precisa de mais alguma coisa?')

def start():
    # Apresentar o chatbot
    falar(f'{cumprimento()} Bem-vindo à Assistente Flip')

    # Pedir o nome
    falar('Qual é o seu nome?')
    nome = ouvir()
    if nome:
        falar(f'Olá, {nome}!')
    else:
        falar('Desculpe, não entendi seu nome.')

    while True:
        # Perguntar em que posso ajudar
        falar('Em que posso ajudar?')

        # Ouça a opção escolhida
        resposta = ouvir().lower()

        # Processar a resposta
        processar_resposta(resposta, nome)

        # Perguntar se precisa de mais alguma coisa
        falar('Precisa de mais alguma coisa?')

        # Ouvir a resposta e verificar se a conversa deve continuar
        mais_alguma_coisa = ouvir().lower()
        if 'não' in mais_alguma_coisa:
            falar('Ok, estou aqui se precisar de mais alguma coisa.')
            break

    # Perguntar se deseja iniciar uma nova conversa
    falar('Para iniciar uma nova conversa, diga "flip". Para sair, diga "sair".')
    nova_conversa = ouvir().lower()
    if 'sair' in nova_conversa:
        falar('Até logo!')
    elif 'flip' in nova_conversa:
        start()

if __name__ == '__main__':
    start()