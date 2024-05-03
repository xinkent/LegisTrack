# 法律案収集用クローラー

## Requirements
Python 3.11
poetry

## 実行方法

```:shell
poetry install
poetry run python src/main.py
```

## デプロイ

```:shell
gcloud functions deploy legis-track-crawler \
--entry-point=execute \
--region=asia-northeast1 \
--runtime=python312 \
--source=./src/ \
--trigger-http \
--allow-unauthenticated
```
