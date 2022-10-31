from aiogram import types
async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота'),
        types.BotCommand('register', 'регистрация Авто'),
        types.BotCommand('menu', 'Кнопки'),
        types.BotCommand('help', 'Помощь'),
        types.BotCommand('sellary', 'Заработок'),
    ])