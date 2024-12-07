import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatWriteForbidden, PeerIdInvalid, FloodWait

# Дані для вашого акаунта
API_ID_YOURS = 24588949  # Ваш API_ID
API_HASH_YOURS = "590483254d766bec4b18abdc7354d503"  # Ваш API_HASH
SESSION_NAME_YOURS = "my_account_session"  # Сесія вашого акаунта

# ID груп для розсилки
GROUP_IDS_YOURS = [
    -1001950993408,
    -1002061972274,
    -1001822629837,
    -1001156898558,
    -1002432287541,
    -1001878801745,
    -1001833194440,
    -1001603442308,
    -1001571671475,
    -1001612144132,
    -1001928009530,
    -1001910048499,
    -1001678758320,
    -1002134057899,
    -1001871218088,
    -1001501665029,
    -1001634840836,
    -1001591908042
]  # Замініть на ваші групи

# Повідомлення для розсилки
MESSAGE = """
💥 Aegis VoIP – связь, которая работает для вас!
📊 Средний дозвон 55% – ваш бизнес всегда на связи.
🔑 Что мы предлагаем?
 • Мобильные тарифы РФ: MTS, MegaFon, Beeline, Yota, Tele2.
 • Премиум маршруты и стабильность.
🎁 $5 на тестирование для новых клиентов!
⚙️ Преимущества:
 • Быстрое подключение.
 • Поддержка 24/7.
🚀 Aegis VoIP – выбирайте надежность.
"""

# Створюємо клієнт Pyrogram
app_yours = Client(SESSION_NAME_YOURS, api_id=API_ID_YOURS, api_hash=API_HASH_YOURS)


async def send_broadcast(client, group_ids):
    """Розсилка повідомлень в конкретні групи та підрахунок кількості чатів."""
    sent_count = 0  # Лічильник надісланих повідомлень
    for group_id in group_ids:
        try:
            await client.send_message(chat_id=group_id, text=MESSAGE)
            sent_count += 1
            print(f"Повідомлення надіслано до групи {group_id}")
        except ChatWriteForbidden:
            print(f"Немає дозволу на відправку в групу {group_id}.")
        except PeerIdInvalid:
            print(f"Неправильний Peer ID для групи {group_id}.")
        except FloodWait as e:
            print(f"Перевищено ліміт: очікуємо {e.value} секунд.")
            await asyncio.sleep(e.value)
        except Exception as e:
            print(f"Помилка з групою {group_id}: {e}")
    return sent_count


async def periodic_broadcast(client, group_ids, interval):
    """Розсилка кожні interval секунд."""
    while True:
        print("Автоматична розсилка...")
        sent_count = await send_broadcast(client, group_ids)
        print(f"Автоматична розсилка завершена. Відправлено у {sent_count} чатів.")
        await asyncio.sleep(interval)


@app_yours.on_message(filters.text & filters.private)
async def handle_message(client, message):
    """Обробка повідомлень для запуску розсилки вручну."""
    if message.text.lower() == "рассылка":
        print("Отримано команду 'Рассылка'. Виконуємо розсилку.")
        sent_count = await send_broadcast(client, GROUP_IDS_YOURS)
        await message.reply(f"Делаю рассылку в {sent_count} чатов.")  # Відповідь у вибраному
        print(f"Розсилку завершено. Відправлено у {sent_count} чатів.")


async def run_client():
    """Запуск клієнта та розсилок."""
    await app_yours.start()

    # Автоматична розсилка кожні 10 хвилин (600 секунд)
    task = asyncio.create_task(periodic_broadcast(app_yours, GROUP_IDS_YOURS, 600))

    # Обробка команд
    await asyncio.gather(task)


if __name__ == "__main__":
    asyncio.run(run_client())