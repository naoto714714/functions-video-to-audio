# Functions Video to Audio

Cloud Run関数を使用して、Google Cloud Storage上の動画ファイルを音声ファイルに変換するシステムです。

## 概要

このシステムは以下の機能を持ちます：

1. `gs://im-naoto-test-bucket/inputs` バケットに動画ファイルがアップロードされるのを検知
2. アップロードされた動画ファイルから音声を抽出
3. 抽出した音声を `gs://im-naoto-test-bucket/outputs` バケットに保存
4. 処理が完了した動画ファイルを入力バケットから削除

## 必要条件

- Python 3.12
- Google Cloud アカウント
- `im-naoto-test-bucket` バケットへのアクセス権限

## セットアップ方法

### ローカル開発環境

1. リポジトリをクローン
   ```bash
   git clone git@github.com:naoto714714/functions-video-to-audio.git
   cd functions-video-to-audio
   ```

2. 仮想環境の作成とアクティベート
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   # または
   venv\Scripts\activate  # Windows
   ```

3. 依存パッケージのインストール
   ```bash
   pip install -r requirements.txt
   ```

4. Google Cloud認証の設定
   ```bash
   gcloud auth application-default login
   ```

### デプロイ方法

1. Cloud Run関数にデプロイ
   ```bash
   gcloud functions deploy video-to-audio \
     --gen2 \
     --runtime=python312 \
     --region=asia-northeast1 \
     --source=. \
     --entry-point=video_to_audio \
     --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
     --trigger-event-filters="bucket=im-naoto-test-bucket"
   ```

## 使い方

1. `gs://im-naoto-test-bucket/inputs` バケットに動画ファイルをアップロード
2. Cloud Run関数が自動的に起動し、動画から音声を抽出
3. 抽出された音声ファイルが `gs://im-naoto-test-bucket/outputs` バケットに保存される
4. 元の動画ファイルが入力バケットから削除される

## ライセンス

MIT
