from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def synthesize_speech(api_key, service_url, text, output_path, voice="en-US_AllisonV3Voice"):
    authenticator = IAMAuthenticator(api_key)
    tts = TextToSpeechV1(authenticator=authenticator)
    tts.set_service_url(service_url)

    with open(output_path, 'wb') as audio_file:
        result = tts.synthesize(text=text, voice=voice, accept='audio/mp3').get_result()
        audio_file.write(result.content)
