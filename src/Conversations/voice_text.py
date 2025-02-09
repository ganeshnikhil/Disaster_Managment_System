import speech_recognition as sr


def voice_to_text(temp_audio):

    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio) as source:
        audio_data = recognizer.record(source)
        
    try:
        trnanscribed_text = recognizer.recognize_google(audio_data)
        return trnanscribed_text
    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError:
        print("Could not request results, check your internet connection")
        