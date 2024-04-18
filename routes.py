from __future__ import annotations

import json

import httpx
from typing import Annotated, Optional, Union

from aiogram import types
from fastapi import APIRouter, Header
from loguru import logger
from pydantic import BaseModel
from pydub import AudioSegment

from bot import bot, dp
from settings import get_settings

cfg = get_settings()

root_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found"}},
)


class VoiceMessage(BaseModel):
    duration: int
    mime_type: str
    file_id: str
    file_unique_id: str
    file_size: int


class ChatMessage(BaseModel):
    text: Optional[str]


@root_router.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@root_router.post(cfg.webhook_path)
async def bot_webhook(update: dict,
                      x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None) -> Union[None, dict]:
    """ Register webhook endpoint for telegram bot"""
    print('update:', update)
    if x_telegram_bot_api_secret_token != cfg.telegram_my_token:
        logger.error("Wrong secret token!")
        return {"status": "error", "message": "Wrong secret token!"}

    if 'message' in update:
        message = update['message']
        logger.info(f"Message chat id: {message['chat']['id']}")
        if 'voice' in message:
            voice_message = VoiceMessage(**message['voice'])
            await handle_voice_message(voice_message, message['chat']['id'], message['message_id'])
        elif 'text' in message:
            text = message['text']
            if text.startswith('/'):
                telegram_update = types.Update(**update)
                await dp.feed_webhook_update(bot=bot, update=telegram_update)
                return {"status": "success"}
            chat_message = ChatMessage(text=message['text'])
            await handle_chat_message(chat_message, chat_id=message['chat']['id'], message_id=message['message_id'])

    return {"status": "success"}


async def handle_voice_message(voice_message: VoiceMessage, chat_id: int, message_id: int = None):
    logger.info(f"Received voice message: {voice_message}")
    request_url = cfg.stt_url
    headers = {
        'Authorization': f'Bearer {cfg.api_token}'
    }
    file = await bot.get_file(voice_message.file_id)
    await bot.download_file(file.file_path, "123")

    AudioSegment.from_file("123").export("123-1.mp3", format="mp3")
    mp3_data = open("123-1.mp3", "rb")

    files = {
        'audio': mp3_data
    }
    logger.info(f"Sending file to STT service: {files}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(request_url, headers=headers, files=files)
            if response.status_code == 200:
                text = response.json().get('text')
                logger.info(f"Text from voice message: {text}")
                await bot.send_message(chat_id, text, reply_to_message_id=message_id)
            else:
                logger.error(f"Can't get text from voice message: {response.text}")
                await bot.send_message(chat_id, "Can't get text from voice message", reply_to_message_id=message_id)
        except Exception as e:
            logger.error(f"Error while processing voice message: {e}")
            await bot.send_message(chat_id, "Error while processing voice message", reply_to_message_id=message_id)


async def handle_chat_message(chat_message: ChatMessage, chat_id: int, message_id: int = None):
    logger.info(f"Received chat message: {chat_message}")
    request_url = cfg.tts_url
    headers = {
        'Authorization': f'Bearer {cfg.api_token}'
    }

    text = chat_message.text
    data = {
        'speaker_id': 1,
        'text': text

    }
    data = json.dumps(data).encode('utf-8')
    data = json.loads(data)
    logger.info(f"Sending text to TTS service: {data}")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(request_url, headers=headers, json=data)
            logger.info(f"Response: {response}")
            if response.status_code == 200:
                with open("output.mp3", "wb") as f:
                    f.write(response.content)
                logger.info(f"Voice message saved as: {'output.mp3'}")
                await bot.send_audio(chat_id, 'output.mp3', reply_to_message_id=message_id)
            else:
                logger.error(f"Can't get voice message from text: {response.text}")
                await bot.send_message(chat_id, "Can't get voice message from text", reply_to_message_id=message_id)
        except Exception as e:
            logger.error(f"Error while processing chat message: {e}")
            await bot.send_message(chat_id, "Error while processing chat message", reply_to_message_id=message_id)
