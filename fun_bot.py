import telebot
import os
import cv2
import numpy as np

bot = telebot.TeleBot('6250880300:AAGOgIftKxgzDcmKZU0UupGmsf8PgusP1EM')

@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id, 'Привет, я бот для настройки'
                                ' резкости отображения картинок(.jpeg, .bmp, .png...)'
                                '\nТакже для настройки резкости введите значение резкости'
                                ' от 0 до 10')

@bot.message_handler(content_types=['photo', 'text'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'files/' + file_info.file_path.split('/')[-1]
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        my_photo = cv2.imread(src)
        shapeness = 0
        try:
            shapeness = int(message.caption)
            if(shapeness < 0 or shapeness > 10):
                raise ValueError
        except:
            raise ValueError
        kernel = np.array([[-1, -1, -1],
                           [-1, 5 + shapeness, -1],
                           [-1, -1, -1]])
        im = cv2.filter2D(my_photo, -1, kernel)
        cv2.imwrite("files/out.jpg", im)
        img = open("files/out.jpg", "rb")
        bot.send_photo(chat_id, img)
    except Exception as e:
        bot.send_message(message.chat.id, 'Похоже некорректно был введён критерий резкости'
                                    ' или некорректный формат картинки'
                                    '\n Перепроверьте и поробуйте ещё раз!!!!!!')


bot.polling(none_stop=True, interval=0)

