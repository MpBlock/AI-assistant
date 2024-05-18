import cv2
import serial
import os
import pyttsx3
import datetime
import webbrowser
import wikipedia
import random
import speech_recognition as sr

print("Versão do OpenCV:", cv2.__version__)

classificador = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
webCam = cv2.VideoCapture(0)

porta = 'COM3'
velocidadeBaud = 115200
ligarArduino = False
#ligarArduino = True

if ligarArduino:
    SerialArduino = serial.Serial(porta, velocidadeBaud)

# Configuração para a língua portuguesa
wikipedia.set_lang("pt")

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        reconhecedor.adjust_for_ambient_noise(source, duration=1)
        audio = reconhecedor.listen(source)
        try:
            texto = reconhecedor.recognize_google(audio, language='pt-BR')
            print("Você disse: " + texto)
            return texto.lower()
        except sr.UnknownValueError:
            print("Não entendi o áudio.")
            return ""
        except sr.RequestError as e:
            print("Erro ao acessar o serviço de reconhecimento de fala; {0}".format(e))
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
    if resposta == 'pesquisar no google':
        falar('Por favor, diga o que você gostaria de pesquisar no Google:')
        pergunta = ouvir()
        pesquisar_no_google(pergunta)
        falar('A pesquisa foi realizada no Google.')

    elif resposta == 'contar uma piada':
        piada = selecionar_piada()
        falar(piada)
    elif resposta == 'dizer a hora':
        agora = datetime.datetime.now()
        hora = agora.strftime("%H:%M")
        falar(f'{nome}, são {hora}.')

    elif resposta == 'pesquisar na wikipedia':
        falar('O que você gostaria de pesquisar na Wikipédia?')
        termo = ouvir()
        pesquisar_na_wikipedia(termo)

    else:
        falar('Desculpe, não entendi. Por favor, repita.')

    # Perguntar se precisa de mais alguma coisa
    falar('Precisa de mais alguma coisa?')

def start():
    # Apresentar o chatbot
    while True:
        conectou, imagem = webCam.read()
        imagem = cv2.flip(imagem, 1)  # inverte imagem(opcional)
        alturaImagem, larguraImagem = imagem.shape[:2]

        converteuCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        encontrarFaces = classificador.detectMultiScale(converteuCinza,
                                                        scaleFactor=1.5,
                                                        minSize=(150, 150),
                                                        maxSize=(200, 200))

        # Se o rosto for reconhecido, inicie a conversa
        # Se o rosto for reconhecido, inicie a conversa
        if len(encontrarFaces) > 0:
            webCam.release()  # Fechar a câmera
            cv2.destroyAllWindows()  # Fechar todas as janelas abertas pela OpenCV
            falar(f'{cumprimento()} Bem-vindo à Assistente Flip')
            falar('Por favor, diga seu nome.')
            nome = ouvir()
            falar(f'Olá, {nome}! Como posso ajudar?')
            break
        else:
            # falar('Rosto não detectado. Aguardando...')
            cv2.imshow('Aguardando Rosto', imagem)
            cv2.waitKey(1)

    while True:
        # Oferecer o menu de opções
        falar('Você pode pedir para pesquisar no Google, contar uma piada, dizer a hora ou pesquisar na Wikipédia.')
        resposta = ouvir().strip().lower()

        if resposta in ['pesquisar no google', 'contar uma piada', 'dizer a hora', 'pesquisar na wikipedia']:
            processar_resposta(resposta, nome)
        else:
            falar('Desculpe, não entendi. Por favor, repita.')

        # Perguntar se precisa de mais alguma coisa
        falar('Precisa de mais alguma coisa?')
        mais_alguma_coisa = ouvir().strip().lower()
        while mais_alguma_coisa not in ['sim', 'não']:
            falar('Por favor, responda sim ou não.')
            mais_alguma_coisa = ouvir().strip().lower()

        if mais_alguma_coisa == 'não':
            falar('Ok, estou aqui se precisar de mais alguma coisa.')
            break

    # Liberar recursos da webcam
    webCam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    start()