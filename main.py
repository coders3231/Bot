from aiogram import types, Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from databese import DataBase
from keyboard import inmenu
from aiogram.types import CallbackQuery
from states import TestState

TOKEN = "5769873844:AAF_ASHuCb-7ghVxolv6EmM8bRBZABptMvs"
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase(db_name="main.db")
db.create()
db.create2()
db.create3()

channels = ['-1001833496792']


async def check_sub_channels(channels: list, user_id:int) -> bool:
    status = False
    for channel in channels:
        data = dict(await bot.get_chat_member(channel, user_id))
        if data["status"] != "left":
            status = True
            continue
        else:
            status = False
            break
    return status

@dp.message_handler(commands="start")
async def hello(message: types.Message):
    if await check_sub_channels(channels=channels, user_id=message.from_user.id):
        await message.answer(f"Salom <b>{message.from_user.full_name}</b>\n\nQuyidagilardan birini tanlang:", reply_markup=inmenu)
    else:
        javob = "Botdan to'liq foydalanish uchun quyidagi kanallarimizga obuna bo'ling:\n\n"
        for channel in channels:
            chat = await bot.get_chat(channel)
            invite_link = await chat.export_invite_link()
            javob += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"
        await message.answer(javob)


@dp.callback_query_handler(text="checktest")
async def insta_services(call: CallbackQuery):
    await call.message.answer("<b>Testga quyidagicha javob yuboring:\n\n<u>tartib raqam#harflar</u></b>")
    await call.message.delete()
    await TestState.checker.set()


@dp.callback_query_handler(text="jointest")
async def insta_services(call: CallbackQuery):
    await call.message.answer("Test javoblarini kiriting.\n\nNamuna: aaabbabbabba")
    await TestState.joined.set()
    await call.message.delete()


@dp.message_handler(state=TestState.joined)
async def joined_test(message: types.Message, state: FSMContext):
    testlar = message.text
    j = 0
    for i in testlar.lower():
        if i != 'a' and i != 'b' and i != 'c' and i != 'd' and i != 'e':
            j += 1
    if j != 0 and testlar != "/cancel":
        await message.answer("Test javoblarida quyidagi harflar qatnashishi mumkin:\n\n"
                             "✅ a,b,c,d,e\n✅ A,B,C,D,E\nQaytadan kiritib ko'ring:\n\n"
                             "Bekor qilish uchun /cancel buyrug'ini kiriting!")
    elif testlar == "/cancel":
        await message.answer(f"Salom, {message.from_user.full_name}!\n\nQuyidagilardan birini tanlang! 👇",
                             reply_markup=inmenu)
        await state.finish()
    else:
        db.add_task(test=testlar, admin=message.from_user.id)
        await message.answer(f"Foydalanuvchi javobni quyidagi tartib raqam orqali tekshirib olishi mumkin."
                             f" <code>{db.get_taskid()[0]}</code>", reply_markup=inmenu)
        await state.finish()


@dp.message_handler(state=TestState.checker)
async def check_test(message: types.Message, state: FSMContext):
    test1 = message.text.split("#")
    ucid = message.from_user.id
    name = ""
    for i in str(message.from_user.full_name):
        if i != "'":
            name += i
    try:
        dcc = db.get_stop(taskid=test1[0])
        if dcc == None:
            testkey = str(db.get_task(taskid=test1[0])[1])
            b = db.check_submit(task_id=test1[0])
            n = False
            for i in b:
                if i[1] == str(ucid):
                    n = True
                    break
            if n:
                await message.answer("Siz bu testga javob bergansiz!", reply_markup = inmenu)
                await state.finish()
            else:
                if len(test1[1]) == len(testkey):
                    testlar = test1[1]
                    j1 = 0
                    for i in testlar.lower():
                        if i != 'a' and i != 'b' and i != 'c' and i != 'd' and i != 'e':
                            j1 += 1
                    if j1 == 0:
                        j = 0
                        t = ""
                        n = ""
                        for i in range(len(testkey)):
                            if testkey[i] == test1[1][i]:
                                j += 1
                                t += str(i+1) + ', '
                            else:
                                n += str(i+1) + ', '
                        await message.answer(f"{name} siz bergan javoblar qabul qilindi. "
                                             f"Natijangiz quyidagicha: \n\n"
                                             f"✅ To'g'ri javoblar: {j} ta\n\n❌ Noto'g'ri javoblar: {len(testkey)-j} ta\n\n"
                                             f"❌ Noto'g'ri topilganlar: \n➖ {n}", reply_markup=inmenu)
                        db.add_submit(id2=test1[0], us_id=message.from_user.id, fullname=name, true=j, false=len(testkey)-j)
                        await state.finish()
                    else:
                        await message.answer("Test javoblarida quyidagi harflar qatnashishi mumkin:\n\n"
                                 "✅ a,b,c,d,e\n✅ A,B,C,D,E\nQaytadan kiritib ko'ring:\n\n")
                else:
                    await message.answer(f"<b>Testga to'liq javob berilmadi! Qayta urinib ko'ring:\n\n"
                                         f"Testlar soni {len(testkey)} ta!</b>")
        else:
            await message.answer("Bu test yakunlangan!", reply_markup=inmenu)
            await state.finish()

    except Exception as e:
       print(e)
       await message.answer("<b>Testga quyidagicha javob yuboring:\n\n<u>tartib raqam#harflar</u></b>")


@dp.callback_query_handler(text="stoptest")
async def insta_services(call: CallbackQuery):
    await call.message.answer("<b>Test tartib raqamini kiriting:</b>")
    await TestState.delete.set()
    await call.message.delete()


@dp.message_handler(state=TestState.delete)
async def delete_test(message: types.Message, state: FSMContext):
    testid = message.text
    usid = message.from_user.id
    try:
        b = db.get_task(taskid=int(testid))
        if b == None:
            await message.answer("<b>Bunday test mavjud emas!</b>", reply_markup=inmenu)
            await state.finish()
        else:
            if usid != b[2]:
                await message.answer("<b>Testni siz yaratmagansiz!!!\n\nTestni faqat uni yaratgan o'chirishi mumkin!</b>",
                                     reply_markup=inmenu)
                await state.finish()
            else:
                s = 1
                a = db.check_submit(task_id=testid)
                a = sorted(a)
                j = "Test natijalari bilan tanishing:\n\n"
                for i in a[::-1]:
                    j += str(s) + ') ' + str(i[2]) + f" ✅ {i[3]},  ❌ {i[4]} \n"
                    s += 1
                await message.answer(j)
                s1 = 1
                j1 = "Tog'ri Javoblar bilan tanishing:\n\n"
                for i in b[1]:
                    j1 += str(s1) + ') ' + i + '\n'
                    s1 += 1
                await message.answer(j1, reply_markup=inmenu)
                try:
                    db.add_stop(id3 = testid)
                except:
                    pass
                await state.finish()
    except:
        await message.answer(f"Salom <b>{message.from_user.full_name}</b>\n\nQuyidagilardan birini tanlang:", reply_markup=inmenu)
        await state.finish()
executor.start_polling(dispatcher=dp, skip_updates=True)
