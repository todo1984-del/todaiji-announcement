import streamlit as st

# ページの基本設定
st.set_page_config(
    page_title="東大寺 多言語アナウンス支援システム",
    page_icon="🏯",
    layout="centered"
)

# 余白と高さを抑えるためのCSS調整
st.markdown("""
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏯 東大寺 多言語アナウンス支援システム")

# 定型文の定義
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

# 状態の初期化
if "selected_key" not in st.session_state:
    st.session_state.selected_key = "その他（自由入力）"

st.markdown("##### 📌 定型アナウンス選択")

# スマホでも横並び（または綺麗に折り返し）になるように2行に分けて配置
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🛍️ 落とし物", use_container_width=True):
        st.session_state.selected_key = "落とし物"
with col2:
    if st.button("👶 迷子", use_container_width=True):
        st.session_state.selected_key = "迷子"
with col3:
    if st.button("✏️ その他", use_container_width=True):
        st.session_state.selected_key = "その他（自由入力）"

col4, col5 = st.columns(2)
with col4:
    if st.button("🚶 入場案内", use_container_width=True):
        st.session_state.selected_key = "入場案内"
with col5:
    if st.button("⏰ 閉門時間", use_container_width=True):
        st.session_state.selected_key = "閉門時間"

# テキストの決定
if st.session_state.selected_key in templates:
    current_template = templates[st.session_state.selected_key]
    ja_text = current_template["ja"]
    en_text = current_template["en"]
    zh_text = current_template["zh"]
    ko_text = current_template["ko"]
    fr_text = current_template["fr"]
    
    user_input = st.text_area("テキスト入力", value=ja_text, height=80, label_visibility="collapsed")
    ja_text = user_input
else:
    user_input = st.text_area("テキスト入力", placeholder="ここに自由にアナウンス文を入力...", height=80, label_visibility="collapsed")
    ja_text = user_input
    en_text = user_input
    zh_text = user_input
    ko_text = user_input
    fr_text = user_input

# 実行ボタン
if st.button("🚀 音声アナウンスを開始する", type="primary", use_container_width=True):
    if ja_text.strip():
        tts_html = f"""
        <div style="padding: 8px; background-color: #f0f2f6; border-radius: 8px; margin-bottom: 5px;">
            <p style="margin:0; font-size: 14px;">🔊 <b>再生中（日・英・中・韓・仏）...</b></p>
        </div>
        <script>
        const messages = [
            {{ text: {repr(ja_text)}, lang: "ja-JP" }},
            {{ text: {repr(en_text)}, lang: "en-US" }},
            {{ text: {repr(zh_text)}, lang: "zh-CN" }},
            {{ text: {repr(ko_text)}, lang: "ko-KR" }},
            {{ text: {repr(fr_text)}, lang: "fr-FR" }}
        ];

        function playSequence(index) {{
            if (index >= messages.length) return;
            const item = messages[index];
            const utterance = new SpeechSynthesisUtterance(item.text);
            utterance.lang = item.lang;
            utterance.rate = 0.9;
            
            utterance.onend = function() {{
                setTimeout(() => playSequence(index + 1), 800);
            }};
            
            window.speechSynthesis.speak(utterance);
        }}

        window.speechSynthesis.cancel();
        playSequence(0);
        </script>
        """
        st.components.v1.html(tts_html, height=60)
        st.success("再生を開始しました！")
    else:
        st.warning("文章を入力してください。")
