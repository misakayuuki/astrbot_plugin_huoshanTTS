from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("astrbot_plugin_huoshanTTS", "misa想变木苒苒", "添加火山TTS api支持", "1.0.0", "https://github.com/misakayuuki/astrbot_plugin_huoshanTTS")
class MyPlugin(Star):
    def __init__(self, context: Context):
        from .huoshan import ProviderHUOSHANTTSAPI # noqa
