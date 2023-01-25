from aiogram import executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.deep_linking import get_start_link

import markups
from config import dp, db, bot
from markups import product_menu

param_to_change = []
dialog_states = {}


async def process_ref_args(user_id: int, inviter_id):
    if inviter_id != '':
        try:
            inviter_id = int(inviter_id)
        except:
            return
        if (inviter_id != user_id) and not (str(user_id) in db.get_invited_users(inviter_id)) and not (
                db.user_exists(user_id)):
            db.add_user(user_id)

            db.set_inviter_id(user_id=user_id, inviter_id=inviter_id)
            db.update_invited_users(user_id, inviter_id)


@dp.message_handler(commands=['start'])
async def reply_menu(msg: types.Message):
    print(msg.from_user.id)
    args = msg.get_args()
    await process_ref_args(user_id=msg.from_user.id, inviter_id=args)

    db.add_user(msg.from_user.id) if not db.user_exists(msg.from_user.id) else None
    video = open("on_start.png", "rb")

    await bot.send_photo(photo=video, chat_id=msg.from_user.id,
                         caption=f"""Привет {msg.from_user.first_name} ✌️ Мы команда MPHelp Club, хотим познакомить Вас с топовыми сервисами аналитиками для МАРКЕТПЛЕЙСОВ, чтобы вы выбрали самый оптимальный для вас и сэкономили свой бюджет!""",
                         reply_markup=markups.get_main_keyb(msg.from_user.id))


@dp.callback_query_handler(Text("show_categories"))
async def show_categories(call: types.CallbackQuery):
    keyb = markups.get_category_keyb(call.from_user.id)
    await call.message.edit_text("Здесь представлены категории товаров", reply_markup=keyb)


@dp.callback_query_handler(Text(startswith='watch'))
async def watch_logic(callback: types.CallbackQuery):
    act, current_num, category = callback.data.split('-')[1:]
    current_num = int(current_num)

    current_num += 1 if act == 'next' else -1

    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await watch_all_products_process(current_num, callback.from_user.id, category=category)


@dp.message_handler(content_types=['text'])
async def get_text_from_user(msg: types.Message):
    if msg.text == "Реферальная программа":
        await bot.send_message(msg.from_user.id,
                               f"В боте включена реферальная система. Приглашайте друзей и зарабатывайте на этом!\n"
                               f"Вы будете получать: 500р от каждой покупки вашего реферала\n"
                               f"Ваша реферальная ссылка:\n"
                               f"`{await get_start_link(payload=msg.from_user.id)}`\n\n",
                               reply_markup=markups.ref_keyb, parse_mode="MARKDOWN"
                               )
    elif msg.text == "Сервисы аналитики":
        await bot.send_message(msg.from_user.id, "Сервисы", reply_markup=markups.services)

    else:
        await bot.send_message(msg.from_user.id, 'Я не понимаю, что это значит')


@dp.callback_query_handler(Text(startswith="ref"))
async def ref_operations(call: types.CallbackQuery):
    match call.data.split("-")[1]:
        case "money_history":
            pass
        case "referals":
            invited_users_amount = len(db.get_invited_users(call.from_user.id).split())
            await bot.send_message(call.from_user.id, f"Всего приглашено: {invited_users_amount}")
        case "get_ref_link":
            await bot.send_message(call.from_user.id, f'Ваша реферальная ссылка:\n'
                                                      f'`{await get_start_link(payload=call.from_user.id)}`',
                                   parse_mode="MARKDOWN")


@dp.message_handler(content_types=['photo'])
async def get_photo_id(msg: types.Message):
    photo_id = msg.photo[0].file_id
    await bot.send_message(msg.from_user.id, photo_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
