# Translation-app


# Healthcare Translation Assistant 🏥

A powerful medical translation web application built with Streamlit and Google's Gemini AI. This tool helps healthcare providers and patients communicate across language barriers with medical-specific translations and text-to-speech capabilities.

![Healthcare Translation Assistant](https://raw.githubusercontent.com/your-username/your-repo/main/demo.gif)

## 🌟 Features

- **Medical-Specific Translation**: Optimized for healthcare terminology and context
- **Multiple Language Support**: Translate between 8+ languages including:
  - English
  - Spanish
  - French
  - German
  - Chinese
  - Arabic
  - Hindi
  - Japanese
- **Text-to-Speech**: Hear the pronunciation of translations
- **Quick Medical Phrases**: Common medical phrases available with one click
- **User-Friendly Interface**: Clean, intuitive design for healthcare settings
- **Privacy-Focused**: No data storage, real-time processing only
- **API Key Management**: Use default or custom Gemini API keys

## 🚀 Live Demo

Try the application here: [Healthcare Translator App](https://hlangtranslate.streamlit.app/)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/abdullah-w-21/Translation-app.git
cd Translation-app
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your API key:
   - Create a `.streamlit/secrets.toml` file:
   ```toml
   DEFAULT_GEMINI_API_KEY = "your-gemini-api-key-here"
   ```
   - Or use environment variables:
   ```bash
   export DEFAULT_GEMINI_API_KEY='your-gemini-api-key-here'
   ```

5. Run the application:
```bash
streamlit run app.py
```

## 📋 Requirements

- Python 3.9+
- Streamlit
- Google Generative AI
- gTTS (Google Text-to-Speech)
- Python-dotenv

## 💻 Usage

1. **Select Languages**:
   - Choose source and target languages from the sidebar
   - Supports 8+ languages for translation

2. **Enter Text**:
   - Type or paste medical text in the input box
   - Use quick medical phrases for common communications

3. **Translate**:
   - Click the "Translate" button
   - View the translation in real-time

4. **Text-to-Speech**:
   - Click "Speak Translation" to hear the pronunciation
   - Audio playback available for all supported languages

## 🔒 Privacy & Security

- No patient data is stored
- All translations are processed in real-time
- Information is discarded after translation
- Secure API key management
- No database or storage system used

## 🌐 Deployment

The application can be deployed on Streamlit Cloud:

1. Fork this repository
2. Connect to Streamlit Cloud
3. Add your API key in Streamlit Cloud secrets
4. Deploy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


## 👥 Authors

- Abdullsh Wasim - [GitHub Profile]([https://github.com/your-username](https://github.com/abdullah-w-21))

## 🙏 Acknowledgments

- Google Gemini LLM for providing the translation capabilities
- Streamlit for the amazing web framework
- The open-source community for various dependencies


## 🗺️ Roadmap

- [ ] Add support for more languages
- [ ] Implement real-time translation
- [ ] Add medical term dictionary
- [ ] Add Live speech recording transcription in the full stack app (library not supported on streamlit cloud implemented that on local)
- [ ] Improve accessibility features
- [ ] Add support for medical document upload
- [ ] Implement batch translation feature

---

Made with ❤️ by Abdullah Wasim
