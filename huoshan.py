import uuid
import os
import base64
import json
import requests
import aiohttp
import asyncio
from astrbot.core.provider.provider import TTSProvider
from astrbot.core.provider.entites import ProviderType
from astrbot.core.provider.register import register_provider_adapter
# host = "openspeech.bytedance.com"
# api_url = f"https://{host}/api/v1/tts"

# header = {"Authorization": f"Bearer;{access_token}"}




@register_provider_adapter("huoshan_tts_api", "HuoShan TTS API", provider_type=ProviderType.TEXT_TO_SPEECH)
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
        self.api_url = f"https://{host}/api/v1/tts"
        
    async def get_audio(self, text: str) -> str:
        path = f'data/temp/openai_tts_api_{uuid.uuid4()}.wav'
        header = {"Authorization": f"Bearer;{self.chosen_api_key}"}
        async with aiohttp.ClientSession(headers=header) as session:
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
                    "encoding": "wav",
                    "speed_ratio": 1.0,
                    "volume_ratio": 1.0,
                    "pitch_ratio": 1.0,
                },
                "request": {
                    "reqid": str(uuid.uuid4()),
                    "text": text,
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
                with open(path, 'wb') as f:
                    async for chunk in response.iter_bytes(chunk_size=1024):
                        f.write(chunk)
        return path



