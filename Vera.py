import apiai, json, re
import pyttsx3
import speech_recognition as sr

tts=pyttsx3.init()
rate = tts.getProperty('rate')
tts.setProperty('rate', rate-10)

volume=tts.getProperty('volume')
tts.setProperty('volume',volume)

voices=tts.getProperty('voices')

tts.setProperty('voice','ru')

for voice in voices:
    if voice.name == 'Victoria':
        tts.setProperty('voice', voice.id)

def record_volume():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        print('Настраиваюсь.')
        r.adjust_for_ambient_noise(source, duration=0.5)
        print('Слушаю...')
        audio = r.listen(source)
    print('Услышала.')
    try:
        query = r.recognize_google(audio, language = 'ru-RU')
        text = query.lower()
        print(f'Вы сказали: {query.lower()}')
        talk(text)
    except:
        print('Ошибка распознания')


def talk( text ):
    tts.say( text )
    tts.runAndWait()

def textMessage( text ):
    request = apiai.ApiAI('ваш токен').text_request()
    request.lang = 'ru'
    request.query = text
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] 
    if response:
        request.audio_output = response
        talk(response)
    else:
        talk('Простите, я вас не совсем поняла')

while True:
    record_volume()