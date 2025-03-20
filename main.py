import os
import tempfile

from google.cloud import storage
from moviepy import VideoFileClip

# GCSバケット情報
INPUT_BUCKET = "im-naoto-test-bucket"
INPUT_PREFIX = "inputs/"
OUTPUT_BUCKET = INPUT_BUCKET
OUTPUT_PREFIX = "outputs/"


def process_video(event, context):
    """
    Cloud Functions エントリーポイント
    動画ファイルを音声に変換し、出力先に保存する関数

    Args:
        event (dict): Cloud Storageのイベントデータ
        context (google.cloud.functions.Context): イベントのメタデータ
    """
    # イベントからファイル情報を取得
    file_data = event

    # バケット名とファイルパスを取得
    bucket_name = file_data["bucket"]
    file_path = file_data["name"]

    # 入力バケットのinputsプレフィックス内のファイルでない場合は処理しない
    if not file_path.startswith(INPUT_PREFIX):
        print(f"File {file_path} is not in the inputs/ directory. Skipping.")
        return

    # ファイル名のみを取得（パスを除去）
    file_name = os.path.basename(file_path)

    # 出力ファイル名（拡張子をmp3に変更）
    output_file_name = os.path.splitext(file_name)[0] + ".mp3"
    output_path = f"{OUTPUT_PREFIX}{output_file_name}"

    print(f"Processing video file: {file_path}")

    # GCSクライアントを初期化
    storage_client = storage.Client()

    # 一時ディレクトリに動画ファイルをダウンロード
    bucket = storage_client.bucket(bucket_name)
    input_blob = bucket.blob(file_path)

    # 一時ファイルを作成
    with tempfile.NamedTemporaryFile(suffix=os.path.splitext(file_name)[1], delete=False) as temp_input_file:
        input_temp_path = temp_input_file.name
        input_blob.download_to_filename(input_temp_path)

    # 出力ファイルのパス
    output_temp_path = os.path.splitext(input_temp_path)[0] + ".mp3"

    try:
        # 動画から音声を抽出
        video = VideoFileClip(input_temp_path)
        audio = video.audio

        if audio is None:
            print(f"No audio track found in {file_path}")
            return

        # 音声をmp3として保存
        audio.write_audiofile(output_temp_path)
        video.close()

        # GCSに音声ファイルをアップロード
        output_blob = bucket.blob(output_path)
        output_blob.upload_from_filename(output_temp_path)

        print(f"Successfully converted {file_path} to {output_path}")

        # 処理が完了したら入力ファイルを削除
        input_blob.delete()
        print(f"Deleted original file: {file_path}")

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        raise

    finally:
        # 一時ファイルを削除
        if os.path.exists(input_temp_path):
            os.remove(input_temp_path)
        if os.path.exists(output_temp_path):
            os.remove(output_temp_path)


if __name__ == "__main__":
    # ローカルテスト用のコード
    # 実際のデプロイではこの部分は実行されない
    test_event = {
        "bucket": INPUT_BUCKET,
        "name": f"{INPUT_PREFIX}sample_video.mp4",
    }

    process_video(test_event, None)
