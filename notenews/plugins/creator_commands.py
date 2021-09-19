from notenews import NoteNews, Functions
from pyrogram.types import Message
from pyrogram import Client, filters
import heroku3
from ..client import Config

from functools import partial, wraps

cmd = partial(filters.command, prefixes=list("/"))


@NoteMusic.on_message(cmd("add"))
async def add_feed(_, message: Message):
    if Functions.check_owner(message.from_user.id) == True:
        heroku_conn = heroku3.from_key(Config.HU_KEY)
        app = heroku_conn.apps()[Config.HU_APP]
        heroku_vars = app.config()
        var = heroku_vars["FEED_URLS"]
        heroku_vars["FEED_URLS"] = f"{var} | {Functions.input_str(message)}"