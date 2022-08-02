tracked = []


def remove_product(message, bot):
    if message.text in tracked:
        tracked.remove(message.text)
    bot.send_message(
        message.chat.id,
        f"Объявление с текстом {message.text} "
        f"успешно удалено. "
        f"Теперь Вы отслеживаете {tracked}"
    )


def add_product(message, bot):
    tracked.append(message.text)
    bot.send_message(
        message.chat.id,
        f"Объявление с текстом {message.text} "
        f"успешно добавлено. "
        f"Теперь Вы отслеживаете {tracked}"
    )
