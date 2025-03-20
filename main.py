import os
import subprocess
import tempfile

from flask import Flask, Request
from google.cloud import storage

app = Flask(__name__)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Google Cloud Storageからファイルをダウンロードする"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Google Cloud Storageにファイルをアップロードする"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)


def delete_blob(bucket_name, blob_name):
    """Google Cloud Storage上のファイルを削除する"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()


def convert_video_to_audio(video_file, audio_file):
    """FFmpegを使用して動画ファイルを音声ファイルに変換する"""
    command = [
        "ffmpeg",
        "-i",
        video_file,
        "-vn",  # 映像を除外
        "-acodec",
        "libmp3lame",  # MP3コーデックを使用
        "-q:a",
        "2",  # 音質設定
        audio_file,
    ]
    subprocess.run(command, check=True)


@app.route("/", methods=["POST"])
def process_gcs_event(request: Request):
    """Cloud Storage triggerからのイベントを処理する"""
    envelope = request.get_json()

    if not envelope:
        return "No event data", 400

    # イベントからファイル情報を取得
    event = envelope
    bucket_name = event["bucket"]
    file_name = event["name"]

    # 入力バケットのパスのみ処理
    if not file_name.startswith("inputs/"):
        return "Not in inputs directory", 200

    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(file_name)[1]) as video_temp:
        # 動画ファイルをダウンロード
        download_blob(bucket_name, file_name, video_temp.name)

        # 出力音声ファイル名を生成
        audio_file_name = os.path.basename(file_name)
        audio_file_name = os.path.splitext(audio_file_name)[0] + ".mp3"

        # 一時的な音声ファイルのパス
        with tempfile.NamedTemporaryFile(suffix=".mp3") as audio_temp:
            # 動画を音声に変換
            convert_video_to_audio(video_temp.name, audio_temp.name)

            # 音声ファイルをアップロード
            output_path = f"outputs/{audio_file_name}"
            upload_blob(bucket_name, audio_temp.name, output_path)

    # 処理が完了した元の動画ファイルを削除
    delete_blob(bucket_name, file_name)

    return f"Successfully converted {file_name} to audio", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
