import streamlit as st

st.set_page_config(page_title="アナウンス支援", page_icon="🔊", layout="centered")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    h1 { font-size: 1.4rem !important; margin-bottom: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

st.title("🔊 アナウンス支援（固定文版）")

# 固定文章の定義
templates = {
    "落とし物": {
        "ja": "お知らせいたします。境内にてお忘れ物がございます。お心当たりの方は、南大門横の警備詰所までお越しください。",
        "en": "Attention please. An item has been lost within the temple grounds. If you think it is yours, please come to the Security Office next to the Nandaimon Gate.",
        "zh": "请注意。境内发现了遗失物品。如有失领者，请前往南大门旁的警备室。",
        "ko": "안내 말씀 드립니다. 경내에서 분실물이 발견되었습니다. 해당하는 분께서는 남대문 옆 경비실로 와주시기 바랍니다.",
        "fr": "Attention s'il vous plaît. Un objet a été perdu dans l'enceinte du temple. Si vous pensez qu'il s'agit du vôtre, veuillez vous rendre au poste de sécurité situé à côté de la porte Nandaimon."
    },
    "迷子": {
        "ja": "迷子のお知らせです。お連れ様を探しているお子様を保護しております。お心当たりの方は、南大門横の警備詰所までお越しください。",
        "en": "This is a lost child announcement. We are looking after a child who is looking for their guardian. If you think this is your child, please come to the Security Office next to the Nandaimon Gate.",
        "zh": "寻人广播。我们正在照看一位找不到家人的小朋友。请其家人尽快前往南大门旁的警备室。",
        "ko": "미아 안내 말씀 드립니다. 일행을 찾고 있는 아이를 보호하고 있습니다. 해당하는 분께서는 남대문 옆 경비실로 와주시기 바랍니다.",
        "fr": "C'est un avis d'enfant perdu. Nous prenons soin d'un enfant qui cherche son accompagnateur. Si vous pensez qu'il s'agit du vôtre, veuillez vous rendre au poste de sécurité situé à côté de la porte Nandaimon."
    },
    "混雑時": {
        "ja": "ただいま券売場が大変混雑しております。南大門横のミュージアムにてセット券をお求めいただくと、並ばずに入堂できます。ぜひご利用ください。",
        "en": "The ticket counter is currently very crowded. You can purchase a set ticket at the museum next to the Nandaimon Gate to enter without waiting. Please take advantage of this.",
        "zh": "目前售票处非常拥挤。您可以在南大门旁的博物馆购买套票，无需排队即可入场，欢迎使用。",
        "ko": "현재 매표소가 매우 혼잡합니다. 남대문 옆 박물관에서 세트권을 구매하시면 기다리지 않고 입장하실 수 있습니다. 이용해 주시기 바랍니다.",
        "fr": "Le guichet est actuellement très fréquenté. Vous pouvez acheter un billet combiné au musée situé à côté de la porte Nandaimon pour entrer sans attendre. Veuillez en profiter."
    },
    "拝観時間": {
        "ja": "拝観時間のお知らせです。ただいまの期間、閉門時間は17時30分となっております。お時間には余裕を持ってお回りください。",
        "en": "Viewing hours announcement. During this period, the temple closes at 17:30. Please ensure you have enough time for your visit.",
        "zh": "参观时间通知。目前寺院的关门时间为17:30。请各位游客合理安排参观时间。",
        "ko": "관람 시간 안내입니다. 현재 기간 동안의 폐문 시간은 17시 30분입니다. 시간 여유를 가지고 관람해 주시기 바랍니다.",
        "fr": "Annonce des horaires de visite. Durant cette période, la fermeture est à 17h30. Veuillez vous assurer d'avoir suffisamment de temps pour votre visite."
    }
}

# 選択機能
selected = st.selectbox("アナウンス内容を選択してください", list(templates.keys()))
text = templates[selected]["ja"]
st.info(f"【配信内容】\n\n{text}")

# 再生ボタン
col1, col2 = st.columns(2)
if col1.button("🚀 多言語で再生", type="primary", use_container_width=True):
    # 再生処理（先ほどのJavaScript構成と同じロジックをここに）
    # ... (省略: 以前のHTML/JS埋め込みコードをここに流し込む)
    st.success(f"{selected}を多言語で再生中...")

if col2.button("🇯🇵 日本語のみ再生", use_container_width=True):
    st.success(f"{selected}を日本語で再生中...")
