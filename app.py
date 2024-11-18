import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os
from io import BytesIO
from dotenv import load_dotenv
import tempfile

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
            # Try to get API key from environment variable or Streamlit secrets
            default_key = os.getenv('DEFAULT_GEMINI_API_KEY') or st.secrets.get("DEFAULT_GEMINI_API_KEY")
            if not default_key:
                st.error("No default API key found!")
                return None
            st.session_state.api_key = default_key
            return default_key

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
        fp.seek(0)
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
        
        # Text input area with example
        example_text = "Enter your medical text here. For example: 'The patient presents with acute abdominal pain and fever.'"
        st.session_state.transcript = st.text_area(
            "Enter text to translate:",
            value=st.session_state.transcript,
            height=200,
            placeholder=example_text
        )

        # Quick phrases
        st.subheader("Quick Medical Phrases")
        if st.button("🤒 Where does it hurt?"):
            st.session_state.transcript = "Where does it hurt?"
        if st.button("💊 Take this medication twice daily"):
            st.session_state.transcript = "Take this medication twice daily"
        if st.button("🩺 I need to examine you"):
            st.session_state.transcript = "I need to examine you"

    with col2:
        st.subheader("Translated Text")
        if st.button("🔄 Translate", key="translate_button"):
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
                        st.success("Translation completed!")
            else:
                st.warning("Please enter some text to translate")

        # Translation output
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

    # Settings and Information
    with st.expander("ℹ️ App Information and Usage"):
        st.markdown("""
        ### How to Use:
        1. Select your source and target languages from the sidebar
        2. Type or paste your medical text in the input box
        3. Click 'Translate' to get the translation
        4. Use 'Speak Translation' to hear the pronunciation
        
        ### Features:
        - Medical-specific translations
        - Text-to-speech capability
        - Quick medical phrases
        - Support for multiple languages
        
        ### Privacy Notice:
        - No data is stored permanently
        - All translations are processed in real-time
        - Information is discarded after translation
        """)

if __name__ == "__main__":
    main()
