import uuid
import os
import base64
import json
import requests
import aiohttp
import asyncio
import re
from astrbot.core.provider.provider import TTSProvider
from astrbot.core.provider.entites import ProviderType
from astrbot.core.provider.register import register_provider_adapter
# host = "openspeech.bytedance.com"
# api_url = f"https://{host}/api/v1/tts"

# header = {"Authorization": f"Bearer;{access_token}"}




@register_provider_adapter("huoshan_tts_api", "HuoShan TTS API", provider_type=ProviderType.TEXT_TO_SPEECH,default_config_tmpl = {
    "access_token": "your token",
    "voice_type": "voice id",
    "app_id": "appid",
    "cluster": "volcano_icl"
},provider_display_name = "Huoshan TTS")
class ProviderHUOSHANTTSAPI(TTSProvider):
    def __init__(
        self, 
        provider_config: dict, 
        provider_settings: dict,
    ) -> None:
        super().__init__(provider_config, provider_settings)
        self.chosen_access_token = provider_config.get("access_token", "")
        self.voice = provider_config.get("voice_type", "")
        self.chosen_app_id = provider_config.get("app_id", "")
        self.chosen_cluster = provider_config.get("cluster", "volcano_icl")
        self.host = "openspeech.bytedance.com"
        self.api_url = f"https://{self.host}/api/v1/tts"
    
    def remove_complex_emoticons(self,text):
        pattern = r"""
                [a-zA-Z]                # 匹配所有英文字母
                |                       # 或
                \([^()]+\)              # 匹配括号内的复杂颜表情
                |                       # 或
                [^\u4e00-\u9fff，。？！、]  # 匹配非中文、非标点符号、非空格的字符
        """
        regex = re.compile(pattern, re.VERBOSE)
        cleaned_text = regex.sub('', text)
        return cleaned_text


    async def get_audio(self, text: str) -> str:
        path = f'data/temp/openai_tts_api_{uuid.uuid4()}.mp3'
        header = {"Authorization": f"Bearer;{self.chosen_access_token}"}
        clean_text = self.remove_complex_emoticons(text)
        async with aiohttp.ClientSession(headers=header, connector=aiohttp.TCPConnector(ssl=False)) as session:
            request_json = {
                "app": {
                    "appid": self.chosen_app_id,
                    "token": "access_token",
                    "cluster": self.chosen_cluster
                },
                "user": {
                    "uid": "388808087185088"
                },
                "audio": {
                    "voice_type": self.voice,
                    "encoding": "mp3",
                    "speed_ratio": 1.0,
                    "volume_ratio": 1.0,
                    "pitch_ratio": 1.0,
                },
                "request": {
                    "reqid": str(uuid.uuid4()),
                    "text": clean_text,
                    "text_type": "plain",
                    "operation": "query",
                    "with_frontend": 1,
                    "frontend_type": "unitTson"

                }
            }
            async with session.post(
                self.api_url,
                data=json.dumps(request_json)
            )as response:
                print(f"resp body: \n{response.json()}")
                with open(path, 'wb') as f:
                    chunk = await response.json()
                    audio_data = chunk["data"]
                    f.write(base64.b64decode(audio_data))
        return path



