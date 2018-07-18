# Shopping List Bot on *Discord*

このBotは<a href="https://discordapp.com/">Discord</a>のチャットから買うものを登録し、ある時間になったら自動でそのリストを登録したメールアドレスへ送信するBotです。

## できること
* Discordから品目の追加、削除、一覧表示
* 一定時間ごとに品目を買ってきてほしいものとして自動で送信

## 使い方
はじめに**Discord側でBotを準備しておく必要があります。**
1. Python3及びPythonのdiscordライブラリ(<a href="https://github.com/Rapptz/discord.py">discord.py</a>)をインストールする
2. このリポジトリを任意のディレクトリにクローンする
3. discord_env.exampleをコピーしてdiscord_envにリネームし必要事項を設定する
4. cron_job.shを編集し必要事項を設定し、8行目を次のように変更する
```systemd
python3 {このBotをクローンしたディレクトリ}/send_mail.py
```
5. add_table.py, bot.py, send_mail.py, cron_job.shのパーミッションを705に変更する
6. add_table.pyを実行してデータ保存用SQLテーブルを準備する
7. shoppinglistbot.serviceを編集し8,9行目を次のように変更する
```systemd
EnvironmentFile={このBotをクローンしたディレクトリ}/shopping-list-bot/environment
WorkingDirectory={このBotをクローンしたディレクトリ}/shopping-list-bot/
```
7. shoppinglistbot.serviceをユニット定義ファイルの格納ディレクトリへ移動し、デーモンをリロードする
8. cronでcron_job.shを好きなタイミングで呼び出すように設定する
9. shoppinglistbotデーモンを起動させ、お好みで自動起動を有効化する

## 注意
* プログラムはPython3で書かれており、**discordライブラリの<a href="https://github.com/Rapptz/discord.py">discord.py</a>が必要です。**

## ライセンス
このプログラムはMIT Licenseの元、自由に利用することが可能です。詳しくはLICENSEをご覧ください。
This software is released under the MIT License, see LICENSE.

## 募集
このプログラムの改善点などありましたらお知らせいただけると幸いです。