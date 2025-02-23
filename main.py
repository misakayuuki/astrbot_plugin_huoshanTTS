from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("astrbot_plugin_huoshanTTS", "misa想变木苒苒", "添加火山声音复刻 api支持。在服务提供商里添加即可使用", "1.0.1", "https://github.com/misakayuuki/astrbot_plugin_huoshanTTS")
class MyPlugin(Star):
    def __init__(self, context: Context):
        from .huoshan import ProviderHUOSHANTTSAPI # noqa
