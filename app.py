from decouple import config
from app.telegram_bot import TelegramBot
from app.scraping import ScrapingMagicEmperor
from app.db.models import MangaData, User
from app.db import DB


TOKEN = config("TOKEN")

# Instance DB
db = DB()
session = db.get_session

# Create Manga Object
manga = session.query(MangaData).first()
if not manga:
    manga = MangaData(
        name="Mo Huang Da Guan Jia – Magic Emperor",
        last_chapter=449,
        link="https://imperiodabritannia.com/manga/magic-emperor/cap-449/",
    )
    session.add(manga)
    session.commit()

# Instance Telegram Bot
telegram_bot = TelegramBot(TOKEN)

# Instance Scraping
scraping = ScrapingMagicEmperor()


while True:
    clients_telegram = telegram_bot.get_updates()
    clients_telegram = clients_telegram.get("result") or []
    data_manga = scraping.get_data()

    name_manga = data_manga.get("name")
    last_chapter = data_manga.get("last_chapter")
    link = data_manga.get("link")

    last_chapter = int(last_chapter) if last_chapter else 0
    last_chapter_old = int(manga.last_chapter)

    # Add Clientes and Response
    for client in clients_telegram:
        message = client["message"].get("text")
        chat_data = client["message"]["chat"]
        message_id = client["message"]["message_id"]

        client_name = f'{chat_data["first_name"]} {chat_data["last_name"]}'
        chat_id = chat_data["id"]

        if message == "/start":
            telegram_bot.send_message(
                chat_id,
                f"Bem Vindo {client_name}, Você Recebera Atualização de Novos Cap de Magic Emperor..",
                message_id,
            )
            user = session.query(User).filter_by(chat_id=chat_id).first()
            if not user:
                user = User(name=client_name, chat_id=chat_id)
                session.add(user)
                session.commit()

        elif message == "/exit":
            telegram_bot.send_message(chat_id, "Agora você não recebera mais atualizações.", message_id)

            user = session.query(User).filter_by(chat_id=chat_id).first()
            session.delete(user)
            session.commit()
        else:
            telegram_bot.send_message(chat_id, "Desculpe, não reconheço este comando.", message_id)

    # Send Notifications
    if last_chapter > last_chapter_old:
        # Refresh Informations
        manga.last_chapter = last_chapter
        manga.link = link
        session.commit()

        # Get Clients Subcribers
        users = session.query(User).all()
        msg = f"Novo Capitulo Lançado de {name_manga}, Cap. {last_chapter}, link: {link}"
        for user in users:
            chat_id_client = user.chat_id
            telegram_bot.send_message(chat_id_client, msg)
