#!/bin/bash

# データベースが起動するまで待機
until psql $DATABASE_URL -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

# データベースの初期化と Flask アプリケーションの起動
flask db upgrade
flask run --host=0.0.0.0