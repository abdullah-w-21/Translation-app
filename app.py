import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import os
from io import BytesIO
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="Healthcare Translator",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state variables
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""
if 'translation' not in st.session_state:
    st.session_state.translation = ""
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'api_key' not in st.session_state:
    st.session_state.api_key = None
if 'use_custom_key' not in st.session_state:
    st.session_state.use_custom_key = False

# Language options
LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Chinese': 'zh',
    'Arabic': 'ar',
    'Hindi': 'hi',
    'Japanese': 'ja'
}


# Gemini API setup
def setup_gemini(api_key):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        st.error(f"Error configuring Gemini API: {str(e)}")
        return None


# API Key Management
def manage_api_key():
    with st.sidebar:
        st.header("API Key Settings")

        # Option to use custom key
        use_custom = st.checkbox("Use Custom API Key", value=st.session_state.use_custom_key)

        if use_custom:
            custom_key = st.text_input(
                "Enter your Gemini API Key",
                type="password",
                help="Enter your own Gemini API key"
            )
            if custom_key:
                st.session_state.api_key = custom_key
                st.session_state.use_custom_key = True
                return custom_key
        else:
            st.session_state.use_custom_key = False
            default_key = os.getenv('DEFAULT_GEMINI_API_KEY')
            if not default_key:
                st.error("No default API key found in environment variables!")
                return None
            st.session_state.api_key = default_key
            return default_key


# Speech recognition function
def record_audio(source_lang):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=source_lang)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
            return None
        except sr.RequestError:
            st.error("Could not request results from speech recognition service")
            return None


# Translation function using Gemini
def translate_text(model, text, source_lang, target_lang):
    prompt = f"""
    Act as a professional medical translator. Translate the following text from {source_lang} to {target_lang}.
    Please maintain medical accuracy and context. If there are medical terms, provide accurate translations while keeping the meaning clear.

    Text to translate: {text}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None


# Text-to-speech function
def text_to_speech(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        fp = BytesIO()
        tts.write_to_fp(fp)
        return fp
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None


# Main app layout
def main():
    st.title("🏥 Healthcare Translation Assistant")

    # Handle API key
    api_key = manage_api_key()
    if not api_key:
        st.warning("Please configure an API key to use the translator")
        return

    # Initialize Gemini model
    model = setup_gemini(api_key)
    if not model:
        return

    # Sidebar for language selection
    with st.sidebar:
        st.header("Language Settings")
        source_language = st.selectbox("Source Language", list(LANGUAGES.keys()), key="source")
        target_language = st.selectbox("Target Language", list(LANGUAGES.keys()), key="target")

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Text")
        # Record button
        if st.button("🎤 Start Recording" if not st.session_state.is_recording else "⏹️ Stop Recording"):
            st.session_state.is_recording = not st.session_state.is_recording
            if st.session_state.is_recording:
                text = record_audio(LANGUAGES[source_language])
                if text:
                    st.session_state.transcript = text

        # Text input area
        st.session_state.transcript = st.text_area(
            "Or type text here:",
            value=st.session_state.transcript,
            height=200
        )

    with col2:
        st.subheader("Translated Text")
        if st.button("Translate"):
            if st.session_state.transcript:
                with st.spinner("Translating..."):
                    translation = translate_text(
                        model,
                        st.session_state.transcript,
                        source_language,
                        target_language
                    )
                    if translation:
                        st.session_state.translation = translation

        st.text_area(
            "Translation:",
            value=st.session_state.translation,
            height=200,
            key="translation_area"
        )

        # Audio playback
        if st.session_state.translation:
            if st.button("🔊 Speak Translation"):
                with st.spinner("Generating audio..."):
                    audio_fp = text_to_speech(
                        st.session_state.translation,
                        LANGUAGES[target_language]
                    )
                    if audio_fp:
                        st.audio(audio_fp)

    # Footer with information
    st.markdown("---")
    st.markdown("""
    ### Usage Instructions:
    1. Configure API key (use custom or default)
    2. Select source and target languages
    3. Either record speech using the microphone or type text
    4. Click 'Translate' to get the translation
    5. Use the 'Speak Translation' button to hear the translation

    ### Privacy Notice:
    This application processes medical information. No data is stored permanently.
    All translations are performed in real-time and immediately discarded.
    """)


if __name__ == "__main__":
    main()