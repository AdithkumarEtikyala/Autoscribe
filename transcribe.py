from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def transcribe_audio(api_key, service_url, audio_path):
    authenticator = IAMAuthenticator(api_key)
    speech_to_text = SpeechToTextV1(authenticator=authenticator)
    speech_to_text.set_service_url(service_url)

    with open(audio_path, 'rb') as audio_file:
        result = speech_to_text.recognize(audio=audio_file, content_type='audio/mp3').get_result()

    transcript = " ".join([alt['alternatives'][0]['transcript'] for alt in result['results']])
    return transcript
