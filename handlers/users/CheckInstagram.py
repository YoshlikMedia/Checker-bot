from aiogram import types
from data import texts
from data.config import INSTAGRAM_USERNAME, SESSION_FILE
from loader import dp
from states.States import Form
from instaloader import Instaloader, Profile
from keyboards.default.next_button import next
from utils.db_api.mongo import users_db


@dp.message_handler(state=Form.GetInstagram, text='⏩next')
async def get_instagram(msg: types.Message):
    await msg.answer(text=texts.text['instagram_subscription'].format(INSTAGRAM_USERNAME, INSTAGRAM_USERNAME))
    await Form.CheckInstagram.set()

@dp.message_handler(state=Form.CheckInstagram)
async def check_instagram(msg: types.Message):
    username = msg.text
    L = Instaloader()
    L.load_session_from_file('haminmoshotmi', SESSION_FILE)
    insta_check = False
    try:
        profile = Profile.from_username(L.context, INSTAGRAM_USERNAME)
        print("{} follows these profiles:".format(profile.username))
        for followee in profile.get_followers():
            if (followee.username).title() == username.title():
                insta_check = True
                break
    except:
        insta_check = False

    if insta_check:
        users_db.update_one({'telegram_id': msg.from_user.id}, {
            "$set":{
                'invite_instagram': username
            }
        }, upsert=True)
        await msg.reply(text=texts.text['instagram_next_text'], reply_markup=next)
        await Form.GetFacebook.set()
    else:
        await msg.reply(text=texts.text['instagram_repeat_buttuon'].format(INSTAGRAM_USERNAME))
