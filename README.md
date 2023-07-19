# Бот для переноса постов из группы Telegram в группу VK
Программа по реализации бота, для переноса постов из группы Telegram в группу VK.

Бот умеет принимать разные посты из Телеграма (ссылки, фотографии, видео, описания) и транслирует их в указанную группу ВК
# Установка
- Установить `Python 3.10`
- Скачать репозиторий проекта:
```shell
git clone https://github.com/AndreyShukatka/Transferring_post_from_telegram_to_VK.git
```
- Создайте и активируйте виртуальное окружение в корневой папке проекта:
```shell
cd verb_game/
python3 -m venv venv
source venv/bin/activate
```
- Установить рекомендации:
```shell
pip install -r requirements.txt
```
- Создайте в корне проекта файл `.env` и запишите в него необходимые ключи:
```shell
nano .env
```
- Создать группу ВК, можете это сделать по [этой ссылке](https://vk.com/groups?tab=admin&w=groups_create).
- Создать приложение ВК. Создать приложение можно в разделе Мои приложения. Ссылка на него в шапке [данной страницы](https://vk.com/dev).
- В качестве типа приложения ВК следует указать `standalone` — это подходящий тип для приложений, которые просто запускаются на компьютере.
- Получите `client_id` созданного приложения. Если нажать на кнопку `Редактировать` для нового приложения, в адресной строке вы увидите его `client_id`
- Узнать `group_id` можно по [этой ссылке](https://regvk.com/id/)
### Заполнение файла `.env`
- TGM_TOKEN = тут указывается токен вашего телеграм бота [Иснтрукция по получению](https://way23.ru/регистрация-бота-в-telegram.html)
- VK_CLIENT_ID = - id вашего приложения, который вы получили выше, указывается со знаком `-` в начале
- VK_GROUP_ID = id вашей группы, который вы получили выше
- VK_CLIENT_SECRET = Защищённый ключ вашего приложения, находится в настройках приложения ВК
- VK_APP_CLIENT_ID = id вашего приложения, который вы получили выше, указывается без знака `-` В начале

# Запуск
## Запускается коммандой
```Shell
python3 tg_bot.py
```
## Запуск Docker
- Установите Докер, инструкция по [ссылке](https://docs.docker.com/desktop/install/linux-install/)
- Поместите заполненный файл `.env` в основную директорию
-  Запустите комманду
```Shell
docker-compose up
```
# Автоматическое включение приложения на Linux
- Переносите файл `tg_bot.service` в каталог `systemd` путь: `etc/systemd/system`
- Прописываем его в системе:
```Shell
systemctl enable tg_bot
```
- Запускаем
```Shell
systemctl start tg_bot
```
- Проверяем статус:
```Shell
systemctl -l status tg_bot
```
Если все прошло успешно то увидим:
![image](https://github.com/AndreyShukatka/Transferring_post_from_telegram_to_VK/assets/106096891/acf5da57-2e7a-4eb7-8843-18baceffaf62)


# Работа бота:
- Пишите пост в Telegramm канале
- Заходите в бота и пишите комманду `/start`
- Ваш пост автоматически перемещается в указанную в файле `.env` группу, на стену

