import streamlit as st
import json

st.set_page_config(page_title="多言語アナウンス支援", page_icon="🔊", layout="centered")

# --- レイアウト調整CSS（上部が切れないように余裕を持たせる） ---
st.markdown("""
    <style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 1rem;
    }
    h1 {
        font-size: 1.2rem !important;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    h3 {
        font-size: 1.1rem !important;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🔊 多言語アナウンス支援")

# --- 定型文定義 ---
templates = {
    "落とし物": {
        "ja": "お知らせいたします。境内にてお忘れ物がございます。お心当たりの方は、大仏殿中門前（だいぶつでんちゅうもんまえ）の警備詰所までお越しください。",
        "ja_read": "お知らせいたします。境内にてお忘れ物がございます。お心当たりの方は、だいぶつでんちゅうもんまえの警備詰所までお越しください。",
        "en": "Attention please. An item has been lost within the temple grounds. If you think it is yours, please come to the Security Office in front of the Daibutsuden Chumon Gate.",
        "zh": "请注意。境内发现了遗失物品。如有失领者，请前往大佛殿中门前的警备室。",
        "ko": "안내 말씀 드립니다. 경내에서 분실물이 발견되었습니다. 해당하는 분께서는 대불전 중문 앞 경비실로 와주시기 바랍니다.",
        "fr": "Attention s'il vous plaît. Un objet a été perdu dans l'enceinte du temple."
    },
    "迷子": {
        "ja": "迷子のお知らせです。お連れ様を探しているお子様を保護しております。お心当たりの方は、大仏殿中門前（だいぶつでんちゅうもんまえ）の警備詰所までお越しください。",
        "ja_read": "迷子のお知らせです。お連れ様を探しているお子様を保護しております。お心当たりの方は、だいぶつでんちゅうもんまえの警備詰所までお越しください。",
        "en": "This is a lost child announcement. We are looking after a child who is looking for their guardian. Please come to the Security Office in front of the Daibutsuden Chumon Gate.",
        "zh": "寻人广播。我们正在照看一位找不到家人的小朋友。请前往大佛殿中门前的警备室。",
        "ko": "미아 안내 말씀 드립니다. 일행을 찾고 있는 아이를 보호하고 있습니다. 대불전 중문 앞 경비실로 와주시기 바랍니다.",
        "fr": "C'est un avis d'enfant perdu. Nous prenons soin d'un enfant qui cherche son accompagnateur."
    },
    "混雑時": {
        "ja": "ただいま券売場が混雑しております。南大門横のミュージアムにてセット券をお求めいただくと、並ばずに入堂できます。ぜひご利用ください。",
        "ja_read": "ただいま券売場が混雑しております。南大門横のミュージアムにてセット券をお求めいただくと、並ばずに入堂できます。ぜひご利用ください。",
        "en": "The ticket counter is currently crowded. You can purchase a set ticket at the museum next to the Nandaimon Gate to enter without waiting.",
        "zh": "目前售票处非常拥挤。您可以在南大门旁的博物馆购买套票，无需排队即可入场。",
        "ko": "현재 매표소가 혼잡합니다. 남대문 옆 박물관에서 세트권을 구매하시면 기다리지 않고 입장하실 수 있습니다.",
        "fr": "Le guichet est actuellement fréquenté. Vous pouvez acheter un billet combiné au musée pour entrer sans attendre."
    },
    "拝観時間": {
        "ja": "拝観時間のお知らせです。ただいまの期間、閉門時間は17時30分となっております。お時間には余裕を持ってお回りください。",
        "ja_read": "拝観時間のお知らせです。ただいまの期間、閉門時間は17時30分となっております。お時間には余裕を持ってお回りください。",
        "en": "Viewing hours announcement. The temple closes at 17:30. Please ensure you have enough time.",
        "zh": "参观时间通知。目前寺院的关门时间为17:30。请合理安排参观时间。",
        "ko": "관람 시간 안내입니다. 현재 기간 동안의 폐문 시간은 17시 30분입니다. 시간 여유를 가지고 관람해 주시기 바랍니다.",
        "fr": "Annonce des horaires de visite. La fermeture est à 17h30. Veuillez prévoir suffisamment de temps."
    }
}

# --- 画面表示 ---
st.subheader("📌 定型アナウンス")
selected = st.selectbox("アナウンス内容を選択", list(templates.keys()), label_visibility="collapsed")
st.info(f"{templates[selected]['ja']}")

if st.button("🚀 多言語で再生", type="primary", use_container_width=True):
    t = templates[selected]
    messages = [
        {"text": t["ja_read"], "lang": "ja-JP"},
        {"text": t["en"], "lang": "en-US"},
        {"text": t["zh"], "lang": "zh-CN"},
        {"text": t["ko"], "lang": "ko-KR"},
        {"text": t["fr"], "lang": "fr-FR"}
    ]
    js = f"""<script>const msgs={json.dumps(messages)};let i=0;function play(){{if(i>=msgs.length)return;const u=new SpeechSynthesisUtterance(msgs[i].text);u.lang=msgs[i].lang;u.onend=()=>{{i++;setTimeout(play,800);}};window.speechSynthesis.speak(u);}}window.speechSynthesis.cancel();play();</script>"""
    st.components.v1.html(js, height=0)

st.divider()

# --- 追加機能：自由入力 ---
st.subheader("📝 自由入力・コピペ再生")
user_text = st.text_area("テキストを貼り付け", height=70, placeholder="ここにテキストをコピペ...", label_visibility="collapsed")
lang_select = st.selectbox("言語を選択", ["英語 (en)", "中国語 (zh)", "韓国語 (ko)", "フランス語 (fr)", "日本語 (ja)"], label_visibility="collapsed")

lang_map = {"英語 (en)":"en-US", "中国語 (zh)":"zh-CN", "韓国語 (ko)":"ko-KR", "フランス語 (fr)":"fr-FR", "日本語 (ja)":"ja-JP"}

if st.button("🚀 コピペ文章を再生", use_container_width=True):
    if user_text:
        js = f"""<script>window.speechSynthesis.cancel();const u=new SpeechSynthesisUtterance({json.dumps(user_text)});u.lang="{lang_map[lang_select]}";window.speechSynthesis.speak(u);</script>"""
        st.components.v1.html(js, height=0)
    else:
        st.warning("文章を入力してください")
