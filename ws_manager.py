from playwright.async_api import WebSocketRoute
import json
from typing import Callable, List, Any

from log_manager import create_logger



class WSManager():
    def __init__(self):
        self.server_ws: WebSocketRoute = None
        self.page_ws: WebSocketRoute = None
        self.inbound_handlers: List[Callable[[str],Any]] = []
        self.outbound_handlers: List[Callable[[str],Any]] = []

        self.logger, self.listener = create_logger("data/logs/websocket_log.log", "wslog")


    def _try_pretty_msg(self, msg):
        '''
        Попробовать форматировать сообщение к "красивому" виду json
        '''
        try:
            return json.dumps(json.loads(msg), indent=4)
        except json.JSONDecodeError:
            return msg

    
    def send_message_to_server(self, message: str, sender: str = "PAGE"):
        '''
        Отправить сообщение в сторону сервера
        '''
        self.server_ws.send(message)
        self.logger.info(
            "["+sender+"->SERVER] payload=%s",
            self._try_pretty_msg(message)
        )


    def send_message_to_page(self, message: str, sender: str = "SERVER"):
        '''
        Отправить сообщенине в сторону страницы
        '''
        self.page_ws.send(message)
        self.logger.info(
            "["+sender+"->PAGE] payload=%s",
            self._try_pretty_msg(message)
        )
        

    def add_inbound_handler(self, handler: Callable[[str], Any]):
        '''
        Зарегистрировать обработчик входящих сообщений
        '''
        self.inbound_handlers.append(handler)


    def add_outbound_handler(self, handler: Callable[[str], Any]):
        '''
        Зарегистрировать обработчик исходящих сообщений
        '''
        self.outbound_handlers.append(handler)


    def _apply_inbound_handlers(self, message):
        '''
        Пропустить сообщение в сторону страницы и инициировать выполнение всех зарегистрированных обработчиков
        '''
        self.send_message_to_page(message)
        for handler in self.inbound_handlers:
            handler(message)


    def _apply_outbound_handlers(self, message):
        '''
        Пропустить сообщение в сторону сервера и инициировать выполнение всех зарегистрированных обработчиков
        '''
        self.send_message_to_server(message)
        for handler in self.outbound_handlers:
            handler(message)


    async def set_websocket(self, ws: WebSocketRoute):
        '''
        Инициализировать веб-сокет для управления
        '''
        self.page_ws = ws
        self.server_ws: WebSocketRoute = ws.connect_to_server()

        # Пропускаем сообщения сервера в страницу
        self.server_ws.on_message(self._apply_inbound_handlers)

        # Пропускаем сообщения страницы на сервер
        self.page_ws.on_message(self._apply_outbound_handlers)
