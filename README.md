# Kokoro - MedGemma 学校保健室の校医診断

## アプリ概要
「Kokoro」は、医療分野に特化したAIモデル **MedGemma** を活用した、学校保健室での医学的診断・指導をシミュレーションするアプリです。
学生が身体の不調（腹痛、頭痛、発熱など）を相談し、校医が問診を通じて原因を絞り込み、適切なアドバイスや受診勧奨を行う体験を提供します。

MedGemmaの高度な医学知識を背景に、単なる情報提供にとどまらず、対話を通じて症状の詳細を聞き取り、論理的な診断プロセスに基づいた指導を行います。

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
本アプリはAIによる医学的シミュレーションを目的としており、実際の医師による診断を代替するものではありません。深刻な身体症状がある場合は、直ちに実際の医療機関を受診してください。

## Author

t-cool
