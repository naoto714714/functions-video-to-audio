# Functions Video to Audio

Cloud Run関数を使用して、Google Cloud Storageにアップロードされた動画ファイルを自動的に音声ファイルに変換するシステムです。

## 概要

このシステムは以下の機能を提供します：

- `gs://im-naoto-test-bucket/inputs` に動画ファイルがアップロードされたことを検知
- 動画ファイルから音声を抽出
- 抽出した音声ファイルを `gs://im-naoto-test-bucket/outputs` に保存
- 処理が完了した元の動画ファイルを `gs://im-naoto-test-bucket/inputs` から削除

## 技術スタック

- Python 3.12
- Google Cloud Functions
- Google Cloud Storage
- FFmpeg（動画から音声への変換に使用）

## セットアップ

1. 必要なライブラリをインストール：
   ```
   pip install -r requirements.txt
   ```

2. ローカルでのテスト：
   ```
   python main.py
   ```

3. デプロイ：
   ```
   gcloud functions deploy video-to-audio \
     --runtime python312 \
     --trigger-resource gs://im-naoto-test-bucket/inputs \
     --trigger-event google.storage.object.finalize \
     --entry-point process_video
   ```

## 利用方法

1. 変換したい動画ファイルを `gs://im-naoto-test-bucket/inputs` にアップロードします。
2. システムが自動的に検知し、音声ファイルに変換します。
3. 変換された音声ファイルは `gs://im-naoto-test-bucket/outputs` に保存されます。
4. 元の動画ファイルは処理後に削除されます。
