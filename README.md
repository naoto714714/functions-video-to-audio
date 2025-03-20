# Video to Audio Converter

Cloud Run 関数を使用して、Google Cloud Storage バケット内の動画ファイルを音声ファイルに自動変換するサービスです。

## 概要

このプロジェクトは、以下の機能を提供します：

- `gs://im-naoto-test-bucket/inputs` に動画ファイルがアップロードされたのを検知
- アップロードされた動画ファイルを音声ファイル（MP3）に変換
- `gs://im-naoto-test-bucket/outputs` に変換された音声ファイルを保存
- 処理済みの元の動画ファイルを `inputs` フォルダから削除

## 前提条件

- Python 3.12
- Google Cloud アカウントとプロジェクト
- Google Cloud Storage バケット（`im-naoto-test-bucket`）
- FFmpeg（動画変換用）

## セットアップ方法

### ローカル開発環境

1. リポジトリをクローンします：

```bash
git clone git@github.com:naoto714714/functions-video-to-audio.git
cd functions-video-to-audio
```

2. 仮想環境を作成して有効化します：

```bash
python -m venv venv
source venv/bin/activate  # Linuxの場合
# または
venv\Scripts\activate  # Windowsの場合
```

3. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

4. FFmpegがインストールされていることを確認してください。インストールされていない場合は、以下のコマンドでインストールします：

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# https://ffmpeg.org/download.html からダウンロードしてインストール
```

5. ローカルでの実行（テスト用）：

```bash
functions-framework --target=process_gcs_event --debug
```

### Google Cloud へのデプロイ

1. Google Cloud プロジェクトを設定します：

```bash
gcloud config set project [YOUR_PROJECT_ID]
```

2. Cloud Run 関数をデプロイします：

```bash
gcloud functions deploy video-to-audio \
  --gen2 \
  --runtime=python312 \
  --region=asia-northeast1 \
  --source=. \
  --entry-point=process_gcs_event \
  --trigger-event-filters="type=google.cloud.storage.object.v1.finalized" \
  --trigger-event-filters="bucket=im-naoto-test-bucket"
```

3. 必要に応じて、サービスアカウントに適切な権限を付与します：

```bash
gcloud projects add-iam-policy-binding [YOUR_PROJECT_ID] \
  --member="serviceAccount:[YOUR_SERVICE_ACCOUNT]" \
  --role="roles/storage.objectAdmin"
```

## 使用方法

1. `gs://im-naoto-test-bucket/inputs` フォルダに動画ファイルをアップロードします。
2. Cloud Run 関数が自動的に起動し、動画を音声に変換します。
3. 変換された音声ファイルは `gs://im-naoto-test-bucket/outputs` フォルダに保存されます。
4. 元の動画ファイルは処理後に自動的に削除されます。

## トラブルシューティング

- Cloud Run 関数のログを確認して、エラーがないか確認してください。
- 権限の問題が発生した場合は、サービスアカウントに適切な権限が付与されているか確認してください。
- FFmpeg関連のエラーが発生した場合は、Cloud Run 関数のランタイムに FFmpeg が正しくインストールされているか確認してください。
