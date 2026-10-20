import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

st.set_page_config(
    page_title="AI Language Translator | CodeAlpha",
    page_icon="🌐",
    layout="centered"
)

# Custom Styling for Professional Look
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #555555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        background: #E3F2FD;
        color: #1565C0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align: center;"><span class="badge">CodeAlpha AI Internship — Task 1</span></div>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">🌐 AI Language Translation Tool</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Instant multi-language neural translation with text-to-speech pronunciation</p>', unsafe_allow_html=True)

LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Gujarati": "gu",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Russian": "ru",
    "Arabic": "ar",
    "Portuguese": "pt",
    "Italian": "it",
    "Dutch": "nl",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Turkish": "tr",
    "Vietnamese": "vi"
}

lang_names = list(LANGUAGES.keys())

col_src, col_btn, col_tgt = st.columns([5, 1, 5])

with col_src:
    source_choice = st.selectbox(
        "Source Language",
        ["Auto Detect"] + lang_names,
        index=0,
        help="Select language to translate from"
    )

with col_btn:
    st.write("")
    st.write("")
    swap = st.button("⇄", help="Swap languages")

with col_tgt:
    default_target_idx = 4  # Default to Hindi
    if swap and source_choice != "Auto Detect":
        # Swap source and target
        new_tgt = source_choice
        target_choice = st.selectbox("Target Language", lang_names, index=lang_names.index(new_tgt))
    else:
        target_choice = st.selectbox("Target Language", lang_names, index=default_target_idx)

input_text = st.text_area(
    "Enter text to translate:",
    height=140,
    placeholder="Type or paste text here (e.g., 'Artificial Intelligence is revolutionizing modern technology.')..."
)

char_count = len(input_text)
word_count = len(input_text.split()) if input_text.strip() else 0
st.caption(f"📝 Characters: **{char_count}** | Words: **{word_count}**")

col_act1, col_act2 = st.columns([1, 4])
with col_act1:
    translate_clicked = st.button("🚀 Translate", type="primary", use_container_width=True)

if translate_clicked or (input_text and "last_input" in st.session_state and st.session_state.last_input != input_text):
    if not input_text.strip():
        st.warning("⚠️ Please enter some text to translate.")
    else:
        src_code = "auto" if source_choice == "Auto Detect" else LANGUAGES[source_choice]
        tgt_code = LANGUAGES[target_choice]

        with st.spinner("Translating..."):
            try:
                translator = GoogleTranslator(source=src_code, target=tgt_code)
                translated_result = translator.translate(input_text)
                st.session_state.last_translation = translated_result
                st.session_state.last_input = input_text
            except Exception as e:
                st.error(f"❌ Translation failed: {e}")
                st.session_state.last_translation = None

if "last_translation" in st.session_state and st.session_state.last_translation:
    res = st.session_state.last_translation
    st.success("✅ Translation Complete")
    
    st.text_area("Translated Output:", value=res, height=140)
    
    col_out1, col_out2, col_out3 = st.columns(3)
    
    # 1. Quick Copy Box
    with col_out1:
        st.write("**Raw Text (Click to Copy):**")
        st.code(res, language=None)
        
    # 2. Text-to-Speech Feature (Audio Pronunciation)
    with col_out2:
        st.write("**🔊 Pronunciation Audio:**")
        tgt_code = LANGUAGES[target_choice]
        # Some languages might have slight regional codes in gTTS
        gtts_code = tgt_code.split("-")[0].lower()
        try:
            tts = gTTS(text=res, lang=gtts_code, slow=False)
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            audio_fp.seek(0)
            st.audio(audio_fp.read(), format="audio/mp3")
        except Exception:
            st.info("Audio pronunciation not supported for this dialect.")
            
    # 3. Download translation file
    with col_out3:
        st.write("**📥 Export:**")
        st.download_button(
            label="Download .txt",
            data=f"Original ({source_choice}):\n{input_text}\n\nTranslation ({target_choice}):\n{res}\n",
            file_name=f"translation_{target_choice.lower()}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
st.markdown("<div style='text-align: center; color: #888; font-size: 0.85rem;'>Developed for CodeAlpha Artificial Intelligence Internship | Author: Abhi B Sheth</div>", unsafe_allow_html=True)
