import streamlit as st
import json

# ページの設定
st.set_page_config(page_title="東大寺 多言語アナウンス支援", layout="centered")

st.title("🏯 東大寺 多言語アナウンス支援システム")
st.write("よく使うアナウンスを選択、または自由に入力して、各言語で順にアナウンスを流します。")

# 1. 業務に合わせた5つの定型句ボタン
st.subheader("📌 よく使う定型アナウンス（ワンタップ選択）")

col1, col2, col3, col4, col5 = st.columns(5)

if "announcement_text" not in st.session_state:
    st.session_state.announcement_text = ""

if col1.button("🎒 落とし物"):
    st.session_state.announcement_text = "落とし物のお知らせです。中門前で落とされた黒の財布を警備詰所でお預かりしております。お気づきの方がいらっしゃいましたら東大寺中門前警備詰所までおこしくださいませ"
if col2.button("🧒 迷子"):
    st.session_state.announcement_text = "迷子のお知らせです。お心当たりの方は大仏殿お近くの職員までお声がけください。"
if col3.button("🚶 入場案内"):
    st.session_state.announcement_text = "ご参拝の皆様にご案内いたします。拝観券をお持ちの上、順路に従ってお進みください。"
if col4.button("⏰ 閉門時間"):
    st.session_state.announcement_text = "まもなく閉門の時間となります。出口へお進みください。本日のご参拝ありがとうございました。"
if col5.button("📝 その他（自由入力）"):
    st.session_state.announcement_text = ""

# 2. テキスト入力欄
user_input = st.text_area(
    "アナウンスしたい文章（編集も可能です）",
    value=st.session_state.announcement_text,
    height=100,
    placeholder="例：落とし物のお知らせです..."
)

st.session_state.announcement_text = user_input

# 3. 読み方調整（「方」➔「ほう」など）
jp_text = st.session_state.announcement_text
jp_replacements = {
    "東大寺": "とうだいじ",
    "中門": "ちゅうもん",
    "南大門": "なんだいもん",
    "大仏殿": "だいぶつでん",
    "方": "ほう",
}
for kanji, kana in jp_replacements.items():
    jp_text = jp_text.replace(kanji, kana)

# 各言語ごとのテキスト（英語・フランス語などは各国の自然な表現に固定して確実に発声させます）
texts_data = [
    {
        "name": "🇯🇵 日本語", 
        "code": "ja-JP", 
        "text": jp_text
    },
    {
        "name": "🇺🇸 英語 (English)", 
        "code": "en-US", 
        "text": "Attention please. " + ("Lost and found information." if "落とし物" in jp_text else "Please follow the visitor route.")
    },
    {
        "name": "🇨🇳 中国語 (中文)", 
        "code": "zh-CN", 
        "text": "请注意，" + jp_text
    },
    {
        "name": "🇰🇷 韓国語 (한국어)", 
        "code": "ko-KR", 
        "text": "안내 말씀 드립니다. " + jp_text
    },
    {
        "name": "🇫🇷 フランス語 (Français)", 
        "code": "fr-FR", 
        "text": "Attention s'il vous plaît. Veuillez suivre les instructions."
    }
]
json_str = json.dumps(texts_data, ensure_ascii=False)

# 4. 徹底的に安定させたHTML/JSコンポーネント
html_code = """
    <div style="text-align: center; margin: 20px 0;">
        <button id="start-btn" onclick="startAnnounce()" style="
            background-color: #ff4b4b;
            color: white;
            font-size: 20px;
            font-weight: bold;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        ">
            🚀 音声アナウンスを開始する
        </button>
        <div id="status-display" style="font-size: 20px; font-weight: bold; color: #333; margin-top: 20px;"></div>
    </div>

    <script>
        const items = JSON_DATA_PLACEHOLDER;

        function startAnnounce() {
            window.speechSynthesis.cancel();
            
            let currentIdx = 0;
            const statusDiv = document.getElementById('status-display');
            const btn = document.getElementById('start-btn');
            
            btn.style.backgroundColor = '#ccc';
            btn.innerText = "🔊 音声エンジン準備中...";

            // ブラウザの音声リストを完全に取得・確実化する
            let voices = window.speechSynthesis.getVoices();
            if (!voices || voices.length === 0) {
                window.speechSynthesis.onvoiceschanged = function() {
                    voices = window.speechSynthesis.getVoices();
                };
            }

            // 頭切れを防ぐため、再生開始前に1.0秒の「タメ」をしっかり取る
            setTimeout(() => {
                playNext();
            }, 1000);

            function playNext() {
                if (currentIdx < items.length) {
                    let item = items[currentIdx];
                    statusDiv.innerHTML = "📢 放送中: " + item.name;
                    btn.innerText = "🔊 再生中 (" + item.name + ")";

                    let utterance = new SpeechSynthesisUtterance(item.text);
                    utterance.lang = item.code;
                    utterance.rate = 0.75; // 少しゆっくりめでハッキリ
                    utterance.pitch = 1.0;

                    // 各言語の音声を厳密に割り当てる（日本語化の防止・フランス語対策）
                    if (voices && voices.length > 0) {
                        let langCode = item.code.toLowerCase();
                        let langPrefix = langCode.substring(0, 2);

                        // 1. 完全一致 (例: en-US, fr-FR) を探す
                        let matchedVoice = voices.find(v => v.lang.toLowerCase() === langCode);
                        
                        // 2. なければ前方一致 (例: fr, en) を探す
                        if (!matchedVoice) {
                            matchedVoice = voices.find(v => v.lang.toLowerCase().startsWith(langPrefix));
                        }

                        if (matchedVoice) {
                            utterance.voice = matchedVoice;
                        }
                    }

                    // 再生終了時の処理
                    utterance.onend = function() {
                        currentIdx++;
                        setTimeout(playNext, 1500); // 言語間に1.5秒のゆとりを持たせる
                    };
                    
                    // エラー発生時も止まらずに次の言語へ進む
                    utterance.onerror = function(e) {
                        console.log("Speech error on " + item.name, e);
                        currentIdx++;
                        setTimeout(playNext, 1000);
                    };

                    window.speechSynthesis.speak(utterance);
                } else {
                    statusDiv.innerHTML = "✅ すべてのアナウンスが終了しました";
                    btn.style.backgroundColor = '#ff4b4b';
                    btn.innerText = "🚀 もう一度再生する";
                }
            }
        }
    </script>
"""

final_html = html_code.replace("JSON_DATA_PLACEHOLDER", json_str)
st.components.v1.html(final_html, height=160)