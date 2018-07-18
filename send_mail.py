#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os
import sqlite3
from contextlib import closing

# About mail
MAILADDRESS = os.getenv("TO_MAIL", "")
USER = os.getenv("FROM_MAIL", "")
PASSWORD = os.getenv("MAIL_PASSWORD", "")
SMTP_ADDRESS = os.getenv("SMTP_ADDR", "")

# About DB
DBNAME = 'database.db'
TABLE = 'list'
DIR = os.path.dirname(os.path.abspath(__file__)) + '/'

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body.encode("utf-8"), 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addr, msg):
    smtpobj = smtplib.SMTP(SMTP_ADDRESS, 587)
    smtpobj.ehlo()
    smtpobj.login(USER, PASSWORD)
    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
    smtpobj.close()

def getItems():
    try:
        with closing(sqlite3.connect(DIR + DBNAME)) as conn:
            c = conn.cursor()
            sql = 'SELECT * FROM ' + TABLE
            c.execute(sql)
            res = c.fetchall()
            if len(res) > 0:
                items = "買ってきてほしいもの\n"
                for row in res:
                    items += "・{0}\n".format(row[1])
                sql = 'DELETE FROM ' + TABLE + ''' WHERE insert_time < (DATETIME('now','localtime'))'''
                c.execute(sql)
                conn.commit()
                msg = create_message(USER, MAILADDRESS, '買い物リスト', items)
                send(USER, MAILADDRESS, msg)
                print("Mail has been sent successfull")
            else:
                print("No Items")
    except Exception as e:
        print("Error has been occured\n{e}\n".format(**locals()) + DIR)

getItems()
