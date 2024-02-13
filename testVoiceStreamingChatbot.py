# Importazione delle librerie necessarie
from openai import OpenAI
import io
import pygame
from openai_key import api_key  # Assicurati che questo file contenga la tua chiave API in una variabile `api_key`

# Inizializzazione di Pygame per la gestione dell'audio
pygame.init()
pygame.mixer.init()

# Configurazione iniziale del client OpenAI e del modello
client = OpenAI(api_key=api_key) # Inizializza il client OpenAI con la chiave API
model_engine = "gpt-3.5-turbo"  # Imposta il modello di default
temperature = 0.9  # Imposta la temperatura di default

# Variabili globali per la gestione della conversazione
conversation_history = []  # Storico delle conversazioni
max_history_length = 5  # Numero massimo di messaggi da mantenere in memoria

def get_openai_chat_response(message, model, temperature):
    """
    Funzione per ottenere una risposta dall'API di chat di OpenAI.
    
    Args:
    - message: Il messaggio dell'utente a cui rispondere.
    - model: Il modello di OpenAI da utilizzare.
    - temperature: La temperatura per la generazione del testo.
    
    Returns:
    - La risposta generata da OpenAI.
    """
    response = client.chat.completions.create(
    model=model,
    temperature=temperature,
    messages=[
        {"role": "system", "content": "Sei una persona sintetica"},
        {"role": "user", "content": message},
    ]
    )
    return response.choices[0].message.content

def play_audio(stream):
    """
    Funzione per riprodurre un audio da uno stream in memoria.
    
    Args:
    - stream: Lo stream di byte dell'audio da riprodurre.
    """
    # Carica l'audio dallo stream in memoria e riproducilo
    pygame.mixer.music.load(stream)
    pygame.mixer.music.play()
    
    # Attende il termine della riproduzione dell'audio
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Loop principale per l'interazione con l'utente
while True:
    user_input = input("Tu: ")  # Richiede l'input dell'utente
    
    if user_input.lower() == "exit":  # Verifica se l'utente desidera uscire
        break
    
    if user_input:  # Se è stato ricevuto un input
        # Aggiorna lo storico delle conversazioni
        conversation_history.append(user_input)
        conversation_history = conversation_history[-max_history_length:]
        
        # Ottiene la risposta da OpenAI
        response = get_openai_chat_response(user_input,model_engine, temperature)
        print("AI: " + response)  # Stampa la risposta
        
        # Genera l'audio della risposta
        audio_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=response
        )
        
        # Prepara e riproduce l'audio della risposta
        audio_stream = io.BytesIO(audio_response.content)
        play_audio(audio_stream)
    else:
        print("Scusa, non ho capito. Puoi ripetere?")  # Gestisce il caso di input non valido
