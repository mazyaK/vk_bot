import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from parser_vk_bot import Parser

# API-ключ группы
token = "7afd60fd6fe2645c93bc254f644081b6c6879dd7acf612311d337cf2f2a4054e5b4de6aafc1ca8cfcd990"

# Авторизируемся как сообщество
vk_session = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkBotLongPoll(vk_session, "190075659")
vk = vk_session.get_api()

# Смайлик робота
RS = "&#129302;"

# Основной цикл
for event in longpoll.listen():
    # Если пришло новое  сообщение
    if event.type == VkBotEventType.MESSAGE_NEW:
        # Если оно имеет метку для меня(т.е. бота)
        if event.from_user:
            # Сообщение от пользователя
            request = event.obj.text
            if request == "Привет":
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Приветствую {RS}")
            elif request == "Пока":
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Буду ждать вашего письма {RS}")
            elif request == "Картинка":
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Какая картинка вас интересует? {RS}")
                request = "Рыба"
                obj = Parser()
                downl_img = obj.main(request)
            else:
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Не понимаю вас {RS}")

