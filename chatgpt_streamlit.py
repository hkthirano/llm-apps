# streamlit run chatgpt_streamlit.py

import openai
import streamlit as st
from dotenv import load_dotenv
import os

# .envファイルの内容を読み込む
load_dotenv()

if __name__ == "__main__":
    # 環境変数から値を取得
    azure_endpoint = os.getenv("AZURE_ENDPOINT")
    api_key = os.getenv("API_KEY")
    api_version = os.getenv("API_VERSION")
    model = os.getenv("MODEL")

    # AzureOpenAIクライアントを初期化する
    client = openai.AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key=api_key,
        api_version=api_version,
    )

    # システムロールのコンテンツの設定
    systemContent = """
You are Genie helping the User with coding. If they ask your name, answer it as Genie. You are intelligent, helpful and an expert developer, who always gives the correct answer and only does what instructed. You always answer truthfully and don't make things up. Answer or complete the coding question user is asking. Take the following Context and Format into consideration.
    Context: Answer the coding questions as a single code block if possible.
"""

    # Streamlitアプリのタイトル
    st.title("Evi Genie")

    # 全体のレイアウト設定
    st.write(
        "<style> .block-container { max-width: 100% !important; } </style>", unsafe_allow_html=True)

    # 左側と右側のカラムを設定
    col1, col2 = st.columns([1, 3])  # 左カラムを1、右カラムを3の比率で設定

    with col1:
        option = st.selectbox(
            "Programming language:",
            ("Python", "C#", "Java", "C++", "C", "Rust", "TypeScript", "JavaScript", "HTML/CSS",
             "PowerShell", "Bash/Shell", "R", "MATLAB", "Others"),
        )

        # ユーザーのメッセージを入力（テキストエリアを使用して動的な高さを実現）
        message = st.text_area(
            "", height=None, placeholder="Ask to get code response")

        # 質問ボタン
        ask_button = st.button("Ask")

        # ショートカットセクションと各種ボタン
        st.subheader("Shortcuts", divider=True)
        explain_button = st.button("Explain")
        findProblems_button = st.button("Find problems")
        optimize_button = st.button("Optimize")
        addComments_button = st.button("Add comments")
        completeCode_button = st.button("Complete code")
        addTests_button = st.button("Add tests")

    with col2:
        # message = ユーザロールのコンテンツ
        if message:
            # ボタンが押された場合、ChatGPTからの応答を生成
            prompt = ""
            if explain_button:
                prompt = "Explain"
            elif findProblems_button:
                prompt = "Find problems with"
            elif optimize_button:
                prompt = "Optimize"
            elif addComments_button:
                prompt = "Add comments for"
            elif completeCode_button:
                prompt = "Complete"
            elif addTests_button:
                prompt = "Implement tests for"
            elif ask_button:
                prompt = message
            else:
                prompt = message

            userContent = ""
            if prompt:
                userContent = f"""
Question: (The following code is in {option} programming language) {prompt} the following code. Please use Japanese in descriptions.
Code: {message}
Answer:
"""
            else:
                userContent = f"""
Question: (The question is about the {option} programming language) {prompt}.
Answer:
"""

            # ボタンが押された場合、ChatGPTからの応答を生成
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": systemContent,
                    },
                    {
                        "role": "user",
                        "content": userContent,
                    }
                ],
                max_tokens=2048,
                temperature=0.5,
                top_p=1,
                frequency_penalty=1,
                stream=True,
            )

            st.write_stream(response)
