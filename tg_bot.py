import os
import pathlib
import re
import shutil
from urllib.parse import urlsplit

import requests
import vk_api
from environs import Env
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
from vk_bot import upload_vk_photo


def extract_file_extension(url):
    path, filename_tail = os.path.split(urlsplit(url).path)
    return filename_tail, path.split('/')[-1]


def download_file_image(url, message_info):
    filename_tail, path = extract_file_extension(url)
    pathlib.Path(os.path.join('downloads', path)).mkdir(
        parents=True,
        exist_ok=True
    )
    directory = os.path.join('downloads', path, filename_tail)
    response = requests.get(url)
    with open(directory, 'wb') as file:
        file.write(response.content)


def start(bot, update):
    print(message_info)
    if message_info['tgm_photo_id']:
        for photo_id in message_info['tgm_photo_id']:
            tgm_photo_url.append(bot.get_file(photo_id)['file_path'])
    if message_info['tgm_video_id']:
        for video_id in message_info['tgm_video_id']:
            try:
                tgm_video_url.append(bot.get_file(video_id).file_path)
            except:
                continue
    if message_info['tgm_entities']:
        message_info['tgm_url'] = re.search(r"(?P<url>https?://[^\s]+)", message_info['tgm_caption']).group("url")
        message_info['tgm_caption'] = message_info['tgm_caption'].replace(message_info["tgm_url"], '')
        message = message_info['tgm_caption']
    else:
        message = message_info['tgm_caption']
    for url in message_info['tgm_photo_url']:
        download_file_image(url, message_info)
    for url in message_info['tgm_video_url']:
        download_file_image(url, message_info)
    upload_vk_photo(upload, message, vk_group_id, vk, message_info)
    message = None
    tgm_photo_id.clear()
    tgm_video_id.clear()
    tgm_video_url.clear()
    tgm_photo_url.clear()
    message_info['tgm_caption'] = None
    bot.send_message(update.message.chat.id, 'Пост размещщён')
    shutil.rmtree('downloads')


def intercept_message(bot, update):
    print(update)
    if update.channel_post['media_group_id']:
        if update.channel_post.caption:
            message_info['tgm_caption'] = update.channel_post.caption
        if message_info['tgm_media_group_id'] == update.channel_post['media_group_id']:
            if update.channel_post.photo:
                tgm_photo_id.append(update.channel_post.photo[-1]['file_id'])
            if update.channel_post.video:
                tgm_video_id.append(update.channel_post.video['file_id'])
        else:
            message_info['tgm_media_group_id'] = update.channel_post['media_group_id']
            if update.channel_post.photo:
                tgm_photo_id.append(update.channel_post.photo[-1]['file_id'])
            if update.channel_post.video:
                tgm_video_id.append(update.channel_post.video['file_id'])

    else:
        if update.channel_post.caption:
            message_info['tgm_caption'] = update.channel_post.caption
        else:
            message_info['tgm_caption'] = update.channel_post.text
        if update.channel_post.photo:
            tgm_photo_id.append(update.channel_post.photo[-1]['file_id'])
        if update.channel_post.video:
            tgm_video_id.append(update.channel_post.video['file_id'])
        if update.channel_post.entities:
            message_info['tgm_entities'] = update.channel_post.text


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tgm_token = env('TGM_TOKEN')
    vk_token = env('VK_TOKEN')
    vk_group_id = env('VK_GROUP_ID')
    vk_session = vk_api.VkApi(token=vk_token)
    vk = vk_session.get_api()
    upload = vk_api.upload.VkUpload(vk_session)
    tgm_photo_id = []
    tgm_video_id = []
    tgm_photo_url = []
    tgm_video_url = []
    message_info = {
        'tgm_media_group_id': None,
        'tgm_photo_id': tgm_photo_id,
        'tgm_video_id': tgm_video_id,
        'tgm_photo_url': tgm_photo_url,
        'tgm_video_url': tgm_video_url,
        'tgm_caption': None,
        'tgm_entities': None,
        'tgm_url': None
    }
    updater = Updater(tgm_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.all, intercept_message))
    updater.start_polling()
    updater.idle()
