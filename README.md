# Kokoro - MedGemma メンタルヘルス・カウンセリング

## アプリ概要
「Kokoro」は、医療分野に特化したAIモデル **MedGemma** を活用した、メンタルヘルス・カウンセリング支援アプリです。
大学の保健室の先生が学生の悩みを聞くような、温かく受容的な対話を目指しています。

ロジャーズ派の傾聴（Active Listening）の技法を取り入れ、ユーザーの感情に寄り添い、共感的な応答を行います。医療的な知見を背景に持ちつつも、まずは「聴く」ことを最優先し、ユーザーが安心して心の内を話せる場を提供します。

## セットアップ

### 1. モデルのダウンロード
このアプリを実行するには、GGUF形式のモデルファイルが必要です。以下のリンクからダウンロードし、プロジェクトのルートディレクトリに配置してください。

- **モデル配布先:** [unsloth/medgemma-4b-it-GGUF](https://huggingface.co/unsloth/medgemma-4b-it-GGUF/tree/main)
- **ファイル名:** `medgemma-4b-it-Q4_K_M.gguf`

### 2. 環境構築
Python 3.9以上がインストールされていることを確認してください。

```bash
# 仮想環境の作成
python -m venv venv

# 依存パッケージのインストール
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install -r requirements.txt
```

### 3. アプリの起動
以下のコマンドを実行すると、サーバーが起動し、ブラウザでアプリを利用できるようになります。

```bash
npm run dev
```

起動後、ブラウザで `http://localhost:8000` にアクセスしてください。

## 技術スタック
- **Frontend:** HTML, JavaScript, CSS
- **Backend:** FastAPI (Python)
- **AI Engine:** llama-cpp-python
- **Model:** MedGemma 4B IT (GGUF quantized)

## 注意事項
本アプリはAIによるカウンセリング支援を目的としており、医師による診断や治療を代替するものではありません。深刻な悩みや体調不良がある場合は、必ず専門の医療機関を受診してください。

## Author

t-cool
