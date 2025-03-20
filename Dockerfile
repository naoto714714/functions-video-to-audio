# Python 3.12をベースイメージとして使用
FROM python:3.12-slim

# 作業ディレクトリを設定
WORKDIR /app

# FFmpegをインストール（動画処理に必要）
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 依存関係ファイルをコピー
COPY requirements.txt .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# ソースコードをコピー
COPY main.py .

# Cloud Run関数のエントリポイントを設定
CMD ["python", "main.py"]

# Cloud Run関数のエントリポイントとして関数名を環境変数で指定
ENV FUNCTION_TARGET=process_video
