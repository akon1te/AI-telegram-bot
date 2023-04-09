# AI-telegram-bot

AI Bot telegram

```
docker cp utt.mp3 ID_CONTAINER:/root
```
Или можно сделать проще, просто примонтировать само аудио, только назовите его "utt.mp3":

```
docker run -it -v <your path>/utt.mp3:/utt.mp3 stt_image:ver1
```

Если просто хотите проверить работоспособность, то запустите образ stt_image:

![Скрин1](https://github.com/Laitielly/labs_docker/blob/main/images_docker/pic1.png)

Оригинальный текст в аудио отрывке: "I love you, Phoebe".


### Критерии:

- Наличие Dockerfile - 2 балла **[есть](https://github.com/Laitielly/labs_docker/blob/main/lab1/Dockerfile.txt)** (+ [файл с загружаемыми библиотеками](https://github.com/Laitielly/labs_docker/blob/main/lab1/requirements.txt) )

- Верное описание Dockerfile - 4 балла **есть**

Докер файл содержит:
  
    - ос - ubuntu:22.04
    - нужные библиотеки для: сохранения/восстановления сеансов (libsm6), 
    работы с аудио/видео файлами (так как работаем с аудио) (ffmpeg), 
    графического интерфейса (libxext6), работы со строками, списками (libglib2.0-0)
    - установка python3
    - установка pip
    - копирование нужных для работы файлов (open_mer - модель, requirements.txt - нужные модули для работы с моделью stt, 
    utt.mp3 - аудиозапись)
    - установка библиотек из requirements.txt
    - запуск модели open_mer/main.py
  
- Создание Docker-контейнера - 2 балла **есть**

Вот переименование контейнера (создание было с запуском образа):

![Скрин3](https://github.com/Laitielly/labs_docker/blob/main/images_docker/pic3.png)

- Запуск приложения в Docker-контейнере - 2 балла **есть**

Контейнер называется stt_container. Здесь я как раз поменяла запись внутри контейнера и запустила файл из него:

![Скрин2](https://github.com/Laitielly/labs_docker/blob/main/images_docker/pic2.png)


- Проверка работоспособности приложения - 10 баллов (10 за полностью работоспособное приложение, 5 за приложение с некоторыми недоступными функциями, 0 за неработоспособное приложение) **есть, работает полностью, скрины приложены выше**

Скачать образ можно [здесь](https://disk.yandex.ru/d/G27xZUDfXxwvfA). Вот еще картиночки к подтверждению:

![Скрин4](https://github.com/Laitielly/labs_docker/blob/main/images_docker/pic4.png)
![Скрин5](https://github.com/Laitielly/labs_docker/blob/main/images_docker/pic5.png)

У контейнера image python_env:ver3, потому что я переименовала образ чуть позже:
![Скрин6](https://github.com/Laitielly/labs_docker/blob/main/images_docker/pic6.png)


- Качество кода и комментариев - 2 балла **надеюсь есть**

Комментарии вы видите выше, а сам код - [lab1](https://github.com/Laitielly/labs_docker/tree/main/lab1), [open_mer](https://github.com/Laitielly/labs_docker/tree/main/lab1/open_mer).

### Что не получалось:

- Хотела оптимизировать и поставить алпайн питон, но проблемы с установкой модулей. Поэтому для удобной работы с файлами заюзала убунту.
- Сначала думала как лучше примаунтить аудио и просто копировала его в локалхост, но потом исправила на монтирование из любой папки.