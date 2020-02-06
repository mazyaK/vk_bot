import vk_api
import os
from vk_api.upload import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from parser_vk_bot import Parser
from weather_vk_bot import Weather


# API-ключ группы
token = "7afd60fd6fe2645c93bc254f644081b6c6879dd7acf612311d337cf2f2a4054e5b4de6aafc1ca8cfcd990"

# Авторизируемся как сообщество
vk_session = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkBotLongPoll(vk_session, "190075659")
vk = vk_session.get_api()

# Смайлик робота
RS = "&#129302;"

users = {}

# функция загрузки фото на сервак ВК
def upload_photo(vk, photo):
    upload = VkUpload(vk)
    response = upload.photo_messages(photo)[0]

    owner_id = response['owner_id']
    photo_id = response['id']
    access_key = response['access_key']

    return owner_id, photo_id, access_key

# Функция отправки фото пользователю
def send_photo(vk, peer_id, owner_id, photo_id, access_key):
    attachment = f'photo{owner_id}_{photo_id}_{access_key}'
    vk.messages.send(
        random_id=get_random_id(),
        peer_id=peer_id,
        attachment=attachment
    )

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
                    message=f"{RS} Приветствую ")
            elif request == "Пока":
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Буду ждать вашего письма ")
            elif request == "Картинка":
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Какая картинка вас интересует? ")
                # ЗДЕСЬ В НАШ СЛОВАРЬ ДОБАВЛЯЕМ/ОБНОВЛЯЕМ ЗНАЧЕНИЕ У ЮЗЕРА ЧТО ОН ХОЧЕТ КАРТИНКУ И НЕКСТ СООБЩЕНИЕ О КАРТИНКЕ
                users.update({event.obj.from_id: "ЖДЕМ НАЗВАНИЕ КАРТИНКИ"})
            elif request == "Погода":
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=get_random_id(),
                    message=f"{RS} Какого название города, погоду в котором вы хотите узнать? ")
                # ЗДЕСЬ В НАШ СЛОВАРЬ ДОБАВЛЯЕМ/ОБНОВЛЯЕМ ЗНАЧЕНИЕ У ЮЗЕРА ЧТО ОН ХОЧЕТ ПОГОДУ И НЕКСТ СООБЩЕНИЕ О ПОГОДЕ
                users.update({event.obj.from_id: "ЖДЕМ НАЗВАНИЕ ГОРОДА(ПОГОДА)"})

            else:
                if users.get(event.obj.from_id) is None:
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=get_random_id(),
                        message=f"{RS} Не понимаю вас ")
                elif users.get(event.obj.from_id) == "ЖДЕМ НАЗВАНИЕ КАРТИНКИ":
                    # ВОТ ТУТ МЫ ОБРАБАТЫВАЕМ СООБЩЕНИЕ О ТОМ КАКУЮ КАРТИНКУ ИСКАТЬ
                    users.pop(event.obj.from_id)
                    obj = Parser()
                    downl_img = obj.main(request)
                    # путь к скачанной картинке
                    path_to_downl_img = f'img\{request}.jpg'
                    # отправка сообщения перед скачанной картинки
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=get_random_id(),
                        message=f"{RS} Вот, что мне удалось найти ")
                    # отправка скачанной картинки
                    send_photo(vk, event.obj.from_id, *upload_photo(vk, path_to_downl_img))
                    # удаление скачанной картинки
                    os.remove(path_to_downl_img)
                elif users.get(event.obj.from_id) == "ЖДЕМ НАЗВАНИЕ ГОРОДА(ПОГОДА)":
                    # ВОТ ТУТ МЫ ОБРАБАТЫВАЕМ СООБЩЕНИЕ О ТОМ ПОГОДУ В КАКОМ ГОРОДЕ ИСКАТЬ
                    users.pop(event.obj.from_id)
                    obj = Weather()
                    temp = obj.main(request)
                    temp_send = str(round(temp-273.15, 2)) + "°C"
                    # отправка сообщения перед скачанной картинки
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=get_random_id(),
                        message=f"{RS} Температура в городе {request} = {temp_send} ")