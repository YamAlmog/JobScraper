from telegram import Bot
from telegram.ext import Updater, commandhandler
from dotenv import load_dotenv
import os
from manage_job_scraper_messages import ManageScrapersMessages 

load_dotenv(".env")
TELEGRAM_BOT_TOKEN  = os.getenv("TELEGRAM_TOKEN")



def start(update, context):
    update.message.reply_text('Hello! I will send you job positions.')

