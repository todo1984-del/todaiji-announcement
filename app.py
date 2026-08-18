import streamlit as st
from google.cloud import texttospeech
import io

# ページの基本設定
st.set_page_config(
    page_title="東大寺 多言語アナウンス支援システム",
    page_icon="🏯",
    layout="centered"
)

st.title("🏯 東大寺 多言語アナウンス支援システム")
st.write("よく使うアナウンスを選択、または自由に入力して、各言語で順にアナウンスを流します。")

# Google Cloud Text-to-Speech クライアントの初期化
# ※Streamlit CloudのSecrets機能等で認証情報を読み込む想定、または環境変数を利用します
@st.cache_resource
def get_tts_client():
    return texttospeech.TextToSpeechClient()

def speak_text(text, language_code):
    """Google Cloud Text-to-Speech API を使用して音声を生成・再生する"""
    try:
        client = get_tts_client()
        input_text = texttospeech.SynthesisInput(text=text)
        
        # 音声の設定（言語や性別など）
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        
        # 音声ファイル形式の設定 (MP3)
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )
        
        # AudioとしてStreamlitで再生
        st.audio(io.BytesIO(response.audio_content), format="audio/mp3", autoplay=True)
    except Exception as e:
        st.error(f"音声生成エラー: {e}")
        st.info("※Google Cloudの認証情報（Secrets）が正しく設定されているか確認してください。")

# 定型文の定義（固有名詞の読み方も含めて完璧な翻訳に固定）
templates = {
    "落とし物": {
        "ja": "お知らせいたします。境内にてお忘れ物がございました。お心当たりの方は、お近くの係員までお申し出ください。",
        "en": "Attention please. An item has been lost within the temple grounds. If you think it might be yours, please notify a nearby staff member.",
        "zh": "请注意。境内发现了遗失物品。如有失领者，请向附近的工作人员申报。",
        "ko": "안내 말씀 드립니다. 경내에서 분실물이 발견되었습니다. 해당하는 분께서는 가까운 직원에게 문의해 주시기 바랍니다.",
        "fr": "Attention s'il vous plaît. Un objet a été perdu dans l'enceinte du temple. Si vous pensez qu'il s'agit du vôtre, veuillez le signaler à un membre du personnel."
    },
    "迷子": {
        "ja": "迷子のお知らせをいたします。お連れ様をお探しのお子様がいらっしゃいます。係員が保護しておりますので、お心当たりの方はお申し出ください。",
        "en": "This is a lost child announcement. A child is looking for their guardian. Our staff is currently looking after the child, so please approach a staff member if you are looking for them.",
        "zh": "寻人广播。有小朋友正在寻找同行的人。工作人员正在照看，请有线索的游客与工作人员联系。",
        "ko": "미아 안내 말씀 드립니다. 일행을 찾고 있는 아이가 있습니다. 직원이 보호하고 있으니 해당하시는 분께서는 안내해 주시기 바랍니다.",
        "fr": "C'est un avis d'enfant perdu. Un enfant cherche son accompagnateur. Notre personnel s'occupe de l'enfant, veuillez vous adresser à un membre du personnel."
    },
    "入場案内": {
        "ja": "東大寺へようこそ。大仏殿の拝観順路は一方通行となっております。矢印に沿ってお進みください。",
        "en": "Welcome to Todaiji Temple. The viewing route for the Daibutsuden (Great Buddha Hall) is one-way. Please follow the arrows.",
        "zh": "欢迎来到东大寺。大佛殿的参观路线为单向通行，请按照箭头方向前进。",
        "ko": "도다이지에 오신 것을 환영합니다. 대불전 관람로는 일방통행입니다. 화살표를 따라 이동해 주시기 바랍니다.",
        "fr": "Bienvenue au temple Todaiji. Le parcours de visite de la salle du Grand Bouddha est à sens unique. Veuillez suivre les flèches."
    },
    "閉門時間": {
        "ja": "皆様にお知らせいたします。まもなく閉門の時間となります。お気をつけてお帰りください。",
        "en": "Attention visitors. The temple gates will be closing shortly. Please make your way to the exits safely.",
        "zh": "各位游客请注意，寺门即将关闭，请注意安全并准备退场。",
        "ko": "관람객 여러분께 안내 말씀 드립니다. 잠시 후 문을 닫을 예정이오니, 조심히 돌아가시기 바랍니다.",
        "fr": "Attention visiteurs. Les portes du temple vont fermer sous peu. Veuillez regagner la sortie en toute sécurité."
    }
}

st.markdown("### 📌 よく使う定型アナウンス（ワンタッチ選択）")

col1, col2, col3, col4, col5 = st.columns(5)
selected_text = ""

with col1:
    if st.button("🛍️ 落とし物"):
        selected_text = templates["落とし物"]
with col2:
    if st.button("👶 迷子"):
        selected_text = templates["迷子"]
with col3:
    if st.button("🚶 入場案内"):
        selected_text = templates["入場案内"]
with col4:
    if st.button("⏰ 閉門時間"):
        selected_text = templates["閉門時間"]
with col5:
    if st.button("✏️ その他（自由入力）"):
        selected_text = {}

st.markdown("---")
st.write("アナウンスしたい文章（編集も可能です）")

# 入力欄
user_input = st.text_area(
    "テキスト入力",
    value=selected_text.get("ja", "") if isinstance(selected_text, dict) else "",
    placeholder="例：落とし物のお知らせです...",
    height=100,
    label_visibility="collapsed"
)

if st.button("🚀 音声アナウンスを開始する", type="primary", use_container_width=True):
    if user_input:
        st.write("📢 **日本語アナウンス中...**")
        speak_text(user_input, "ja-JP")
        
        # 英語
        en_text = selected_text.get("en", user_input) if isinstance(selected_text, dict) else user_input
        st.write("📢 **英語アナウンス中...**")
        speak_text(en_text, "en-US")
        
        # 中国語
        zh_text = selected_text.get("zh", user_input) if isinstance(selected_text, dict) else user_input
        st.write("📢 **中国語アナウンス中...**")
        speak_text(zh_text, "cmn-CN")
        
        # 韓国語
        ko_text = selected_text.get("ko", user_input) if isinstance(selected_text, dict) else user_input
        st.write("📢 **韓国語アナウンス中...**")
        speak_text(ko_text, "ko-KR")
        
        # フランス語
        fr_text = selected_text.get("fr", user_input) if isinstance(selected_text, dict) else user_input
        st.write("📢 **フランス語アナウンス中...**")
        speak_text(fr_text, "fr-FR")
        
        st.success("すべての言語のアナウンスが完了しました！")
    else:
        st.warning("アナウンスする文章を入力してください。")
