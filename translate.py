from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def translate_text(api_key, service_url, text, target_language):
    authenticator = IAMAuthenticator(api_key)
    translator = LanguageTranslatorV3(version='2018-05-01', authenticator=authenticator)
    translator.set_service_url(service_url)

    result = translator.translate(text=text, source='en', target=target_language).get_result()
    return result['translations'][0]['translation']
