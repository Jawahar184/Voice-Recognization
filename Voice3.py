from gtts import gTTS
import os
import speech_recognition as sr
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# English and Tamil scheme details text
scheme_details_english = """
1. Differently Abled Pension Scheme
2. Assistance to Disabled Persons for Purchase/Fitting of Aids and Appliances (ADIP) Scheme
3. National Handicapped Finance and Development Corporation (NHFDC) Schemes
"""

scheme_details_tamil = """
1. பிரத்தியேகமாக இயங்கும் பட்டியலுக்கு உதவியியல் பென்ஷன் திட்டம்
2. மாற்றுக்கருத்துகள் உள்ள நபர்களுக்கான உதவிக்கான சாதனங்கள் வாங்குதல்/ஒட்டுதல் (ADIP) திட்டம்
3. நாட்டின் மாற்றுக்கருத்தான நிதி மற்றும் வளர்ச்சி கார்ப்பரேஷன் (NHFDC) திட்டங்கள்
"""

# Scheme descriptions dictionary
scheme_descriptions = {
    'english': {
        1: """Differently Abled Pension Scheme:
        Objective: Provides financial support to differently-abled individuals unable to work.
        Eligibility: Persons with disabilities, meeting income criteria.
        Benefits: Monthly pension to meet basic needs. Implementing Agency: State governments.""",
        
        2: """Assistance to Disabled Persons for Purchase/Fitting of Aids and Appliances (ADIP) Scheme:
        Objective: Financial assistance for aids and appliances for disabled persons.
        Eligibility: Persons certified with disabilities.
        Benefits: Funding for devices like Braille machines, white canes.""",
    },
    'tamil': {
        1: """பிரத்தியேகமாக இயங்கும் பட்டியலுக்கு உதவியியல் பென்ஷன் திட்டம்:
        நோக்கம்: வேலை செய்ய முடியாத மாற்றுக்கருத்துகள் உள்ள நபர்களுக்கு நிதி உதவி.
        தகுதி: மாற்றுக்கருத்துகள் உள்ளவர்கள் மற்றும் வருமான அளவுகளுக்கு உட்பட்டவர்.
        பயன்கள்: அடிப்படை தேவைகளை பூர்த்தி செய்ய மாதாந்திர பென்ஷன்.""",
        
        2: """மாற்றுக்கருத்துகள் உள்ள நபர்களுக்கான உதவிக்கான சாதனங்கள் வாங்குதல்/ஒட்டுதல் (ADIP) திட்டம்:
        நோக்கம்: மாற்றுக்கருத்துகள் உள்ள நபர்களுக்கு சாதனங்கள் வாங்க உதவி.
        தகுதி: சான்றிதழ் பெற்ற மாற்றுக்கருத்துகள் உள்ள நபர்கள்.""",
    }
}

def text_to_speech(text, lang_code, filename):
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save(filename)
    play_audio(filename)

def play_audio(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.stop()

def get_language_content(language):
    language_dict = {
        'english': ('en', scheme_details_english),
        'tamil': ('ta', scheme_details_tamil),
    }
    return language_dict.get(language.lower(), ('en', scheme_details_english))

def capture_voice_input(prompt, lang="en", retries=3):
    recognizer = sr.Recognizer()
    text_to_speech(prompt, lang, 'prompt.mp3')
    
    for _ in range(retries):
        with sr.Microphone() as source:
            print(prompt)
            audio = recognizer.listen(source)
        
        try:
            recognized_text = recognizer.recognize_google(audio, language=lang).lower()
            print(f"You said: {recognized_text}")
            return recognized_text
        except sr.UnknownValueError:
            print("Sorry, I could not understand. Please try again.")
        except sr.RequestError:
            print("Network error; please check your connection.")
            break
    return None

def ask_for_scheme_details(language):
    response = capture_voice_input("Would you like details about a specific scheme? Please say yes or no.", lang="en")
    if response == "yes":
        prompt_for_scheme_number(language)
    else:
        print("No further information requested.")

def prompt_for_scheme_number(language):
    response = capture_voice_input("Please say the number of the scheme you want details for.", lang="en")
    
    if response and response.isdigit():
        scheme_number = int(response)
        if 1 <= scheme_number <= 10:
            lang_code = 'en' if language == 'english' else 'ta'
            scheme_description = scheme_descriptions[language].get(scheme_number, "No details available for this scheme.")
            text_to_speech(scheme_description, lang_code, 'scheme_details_specific.mp3')
        else:
            print("Invalid scheme number.")
    else:
        print("Could not recognize a valid number.")

def voice_assisted_scheme(language):
    lang_code, scheme_details = get_language_content(language)
    text_to_speech(scheme_details, lang_code, 'scheme_details.mp3')
    ask_for_scheme_details(language)

if __name__ == "__main__":
    language_prompt = "Please say the language: English or Tamil."
    user_language = capture_voice_input(language_prompt, lang="en")

    if user_language:
        voice_assisted_scheme(user_language)
    else:
        print("Language input failed. Please try again.")



