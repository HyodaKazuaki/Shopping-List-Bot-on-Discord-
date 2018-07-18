#!/bin/sh

# 環境変数
export TO_MAIL="" # 送信先メールアドレス
export FROM_MAIL="" # 送信元メールアドレス
export MAIL_PASSWORD="" # 送信元メールアカウントパスワード
export SMTP_ADDR="" # 送信元メールアドレスの送信ドメイン
python3 /usr/local/bin/shopping-list-bot/send_mail.py