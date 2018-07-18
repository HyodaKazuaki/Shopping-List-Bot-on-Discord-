#!/usr/bin/env python3

import discord
from discord.ext import commands
import asyncio
import re
import os
import sqlite3
from contextlib import closing

# About Discord
TOKEN = os.getenv("DISCORD_TOKEN", "")
OWNER = os.getenv("DISCORD_OWNER", "")

# About DB
DBNAME = 'database.db'
TABLE = 'list'
DIR = os.path.dirname(os.path.abspath(__file__)) + '/'
MAX_LENGTH = 1000

description = '''買い物リストを1日に1回送信するBotです。'''

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('-----')

### <retrun> コマンドの判定(boolean)
def command_validate(ctx):
    return not bot.user == ctx.message.author and ctx.message.author.id == OWNER

@bot.command()
@commands.check(command_validate)
async def add(messages: str = None):
    """
引数に与えられた品目をデータベースへ追加します。
すでに同じ品目が存在した場合は、上書きされることなく多重追加されます。
個数など、細かな指定は__***できません***__。
    """

    if messages == None:
        await bot.say("[Error] 品目を入力してください。")
        return

    if len(messages) > MAX_LENGTH:
        await bot.say("[Error] 文字数をオーバーしています。")
        return

    try:
        with closing(sqlite3.connect(DIR + DBNAME)) as conn:
            c = conn.cursor()
            sql = 'INSERT INTO ' + TABLE + ' (item) VALUES (?)'
            c.execute(sql, (messages,))
            conn.commit()
        await bot.say("追加しました。")
    except Exception as e:
        await bot.say("エラーが発生しました。\n{e}".format(**locals()))

@bot.command()
@commands.check(command_validate)
async def remove(id: int = None):
    """
引数に与えられたIDの品目をデータベースから削除します。
IDについては、!list コマンドを用いて確認してください。
    """
    if id == None:
        await bot.say("[Error] IDを入力してください。")
        return

    try:
        with closing(sqlite3.connect(DIR + DBNAME)) as conn:
            c = conn.cursor()
            sql = 'SELECT * FROM ' + TABLE + ' WHERE id=?'
            c.execute(sql, (id,))
            res = c.fetchone()
            item = res[1]
            sql = 'DELETE FROM ' + TABLE + ' WHERE id=?'
            c.execute(sql, (id,))
            conn.commit()
            await bot.say("ID {id}\t{item} を削除しました。".format(**locals()))
    except Exception as e:
        await bot.say("エラーが発生しました。\n{e}".format(**locals()))

    return

@bot.command()
@commands.check(command_validate)
async def list():
    """
次にメールが送信されるときに連絡される品目とそのIDを表示します。
すでに送信済みの品目や、削除済みの品目については表示されません。
    """
    try:
        with closing(sqlite3.connect(DIR + DBNAME)) as conn:
            c = conn.cursor()
            sql = 'SELECT * FROM ' + TABLE
            c.execute(sql)
            res = c.fetchall()
            if len(res) < 1:
                await bot.say("登録されている品目はありません。")
            else:
                m = "時刻\tID\t品目\t\n"
                for row in res:
                    m += "{0}\t{1}\t{2}\n".format(row[2], row[0], row[1])
                await bot.say(m)
    except Exception as e:
        await bot.say("エラーが発生しました。\n{e}".format(**locals()))

    return

bot.run(TOKEN)