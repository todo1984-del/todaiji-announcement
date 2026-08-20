import streamlit as st
import json

st.set_page_config(page_title="アナウンス支援", page_icon="🔊", layout="centered")

# --- 定型文エリア ---
st.header("🔊 定型アナウンス")
templates = {
    "落とし物": {"ja": "お知らせいたします。境内にてお忘れ物がございます。お心当たりの方は、だいぶつでんちゅうもんまえの警備詰所までお越しください。"},
    "迷子": {"ja": "迷子のお知らせです。お連れ様を探しているお子様を保護しております。だいぶつでんちゅうもんまえの警備詰所までお越しください。"},
    # ... 他の定型文も必要に応じて追加
}

selected = st.selectbox("定型文を選択", list(templates.keys()))
if st.button("定型文を日本語で再生"):
    js = f"<script>const u=new SpeechSynthesisUtterance('{templates[selected]['ja']}');u.lang='ja-JP';window.speechSynthesis.speak(u);</script>"
    st.components.v1.html(js, height=0)

st.divider()

# --- 自由入力エリア（コピペ用） ---
st.header("📝 自由入力（コピペ用）")
user_text = st.text_area("ここにテキストを貼り付けてください", height=100)
lang_select = st.selectbox("言語を選択", ["日本語", "英語", "中国語", "韓国語", "フランス語"])

lang_map = {
    "日本語": "ja-JP",
    "英語": "en-US",
    "中国語": "zh-CN",
    "韓国語": "ko-KR",
    "フランス語": "fr-FR"
}

if st.button("🚀 コピペした内容を再生"):
    if user_text:
        js = f"""
        <script>
        window.speechSynthesis.cancel();
        const u = new SpeechSynthesisUtterance("{user_text}");
        u.lang = "{lang_map[lang_select]}";
        window.speechSynthesis.speak(u);
        </script>
        """
        st.components.v1.html(js, height=0)
    else:
        st.warning("文章を貼り付けてください")
