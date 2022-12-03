import telebot
import mydate_sql0
import date_sql
import stats_data
import time
import token_telebot
import logging
import emoji
import threading

from datetime import date as date_for
import datetime as dt_mg
from datetime import datetime
from telebot import types
from urllib.request import urlopen
from mytoken import *

date_in_sql = {}
comment = {}
f = False
all_users = {} #Словарь со всеми авторизаванными пользователями

def tbot():
    '''Основная функция для работы с ботом'''
    global date_in_sql, comment, all_users
    bot = telebot.TeleBot(token_telebot.token) #Создание объекта класса TeleBot

    '''Создание кнопок, привязанных к клавиатуре пользователя'''
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ev = types.KeyboardButton("📪Мои мероприятия")
    sett = types.KeyboardButton("📕Меню")
    #stats = types.KeyboardButton("Статистика")
    menu.add(sett,ev)
    #menu.add(stats)

    menu_adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ev = types.KeyboardButton("Записи")
    sett = types.KeyboardButton("Настройки бота")
    st = types.KeyboardButton("Зарег. в боте")
    menu_adm.add(sett, ev, st)

    def cheak():
        '''Функция для обработки актуальной даты и сравнения её с датами из sql-таблицы'''
        global date_in_sql
        arr = date_sql.sql_manager().cheak()
        date_in_sql = {}
        if arr !=[]:
            today = date_for.today()
            hour = datetime.now().hour
            today = today + dt_mg.timedelta(days=1)

            back = today + dt_mg.timedelta(days=-1)
            #tomorrow_1 = today + datetime.timedelta(days=2)
            #tomorrow_2 = today + datetime.timedelta(days=3)
            #print(tomorrow)
            for i in arr:
                if i[0] not in date_in_sql:
                    date_time_obj = datetime.strptime(i[1], '%Y-%m-%d %H:%M')
                    if date_time_obj.date() < today:
                        date_sql.sql_manager().delete_once(i[2])
                        cheak()
                    if str(date_time_obj.date()) == str(today) and str(date_time_obj.hour) == str(hour):
                        if i[3] == 0:
                            date_in_sql[i[0]] = [i[1], 0]
                        else:
                            date_in_sql[i[0]] = [i[1], 1]
                    #elif i[1] == str(tomorrow):
                        #date_in_sql[i[0]] = [i[1], 1]
                    #elif (i[1] == str(tomorrow_1):
                        #date_in_sql[i[0]] = [i[1], 2]
                    #else:
                        #date_in_sql[i[0]] = [i[1], 3]
        #print(date_in_sql)

    def cheak_eventer():
        '''Функция для отправки напоминаний'''
        global date_in_sql
        #print(1123, date_in_sql)
        while True:
            #print(11)
            if date_in_sql != {}:
                for users in date_in_sql:
                    arr = date_sql.sql_manager().cheak_event(users, date_in_sql[users][0])
                    #print(arr)
                    for i in arr:
                        arr = ["CЕГОДНЯ через ЧАС", "ЗАВТРА"]
                        events = types.InlineKeyboardMarkup()
                        button1 = types.InlineKeyboardButton(f"Регистрация", url=f'{i[3]}')
                        events.add(button1, types.InlineKeyboardButton(text="🔕Больше не напоминать", callback_data=f"{users}_datestop=dell_{i[5]}"))
                        events.add(types.InlineKeyboardButton(text="Скрыть сообщение", callback_data=f"{users}_dellmess"))
                        bot.send_message(int(i[0]), f"📢Не забудь *{arr[date_in_sql[users][1]]}* ({i[4]}) посетить *{i[2]}*.", reply_markup=events, parse_mode= "Markdown")
                        #bot.register_next_step_handler(message,dd)
                        #bot.delete_message(call.message.chat.id, call.message.message_id)
                        date_sql.sql_manager().delete_once(i[5])
                        #return None
            cheak()
            time.sleep(60)

    def add_new_user(user):
        '''Функция для инициализации пользователя. Создает в all_users словарь с переменными пользователя'''
        global all_users
        all_users[user] ={
            'f' : 0,
            'page' : -1,
            'date' : [],
            'last_photo': 0,
            'mou_date' : "",
            'page_date' : 9,
            'fun' : ["", ""],
            'arr' : [],
            'tp' : 0,
            'xz':0,
            'less' : [],
            'date_in_sql' : {},
            'page_for_less' : 5,
        }
        cheak()

    c = threading.Thread(target = cheak_eventer, args = ())
    c.start()

    @bot.message_handler(commands=['start'])#Обработчик команды start
    def start(message):
        '''Запускает функцию add_new_user и отправляет сообщение с приветствием'''
        global date_in_sql
        user  = message.from_user.id
        add_new_user(str(user))
        bot.send_message(message.from_user.id, emoji.emojize(":thumbs_up: Привет, {0.first_name}! \nЧтобы начать поиск нажми на кнопку 📕Меню. Если хочешь посмотреть избранные мероприятия нажми на 📪Мои мероприятия").format(message.from_user), reply_markup=menu)
        #if str(user) in date_in_sql:
        #c = threading.Thread(target = cheak_eventer, args = ())
        #c.start()

    @bot.message_handler(commands=['adm'])
    def start(message):
        user  = str(message.from_user.id)
        if user in admins:
            bot.send_message(message.from_user.id, emoji.emojize(":ledger: Вы вошли в настройки бота"), reply_markup=menu_adm)

    @bot.message_handler(func=lambda message: message.text =="Записи")
    def adm_stats(message):
        o = date_sql.sql_manager()
        all_event = o.cheak()
        if all_event != []:
            #print(all_event)
            for g in all_event:
                bot.send_message(message.from_user.id, f'Пользователь: {g[0]} \nДата: {g[1]}\n Типы: {g[2]} - {g[3]}')
        else:
            bot.send_message(message.from_user.id, 'Пусто')
    @bot.message_handler(func=lambda message: message.text =="Зарег. в боте")
    def adm_stats(message):
        global all_users

        if all_users != {}:
            #print(all_users)
            for g in all_users:
                bot.send_message(message.from_user.id, f'Пользователь: {g}')
        else:
            bot.send_message(message.from_user.id, 'Пусто')

    '''@bot.message_handler(func=lambda message: str(message.from_user.id) in date_in_sql)
    def cheak_eventer(message):
        global date_in_sql
        #print(1123, date_in_sql)
        if date_in_sql != {}:
            for users in date_in_sql:
                arr = date_sql.sql_manager().cheak_event(users, date_in_sql[users])
                for i in arr:
                    events = types.InlineKeyboardMarkup()
                    button1 = types.InlineKeyboardButton(f"Регистрация", url=f'{i[3]}')
                    events.add(button1, types.InlineKeyboardButton(text="🔕Скрыть и не напоминать", callback_data=f"{users}_datestop=dell_{i[5]}"))
                    bot.send_message(int(i[0]), f"📢Не забудь *{i[4]}* посетить *{i[2]}*.", reply_markup=events, parse_mode= "Markdown")
                    #bot.register_next_step_handler(message,dd)
                    #bot.delete_message(call.message.chat.id, call.message.message_id)
                    date_sql.sql_manager().delete(i[5])
                    cheak()
                    return None'''


    @bot.message_handler(func=lambda message: message.text =="Настройки бота")
    def adm_user(message):
        pass

    @bot.message_handler(func=lambda message: message.text =="📪Мои мероприятия")#Обработчик кнопки Мои мероприятия
    def dd(message):
        '''Обращается к data_sql по id пользователя и отправляет полученную информацию о мероприятиях'''
        global date_in_sql
        arr = date_sql.sql_manager().cheak_user(str(message.from_user.id))
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        if arr != []:
            #bot.send_message(message.from_user.id, "Твои мероприятия:")
            for i in arr:
                events = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(f"Регистрация", url=f'{i[3]}', callback_data=f'{message.from_user.id}_newevent')
                bn = types.InlineKeyboardButton("✅Посетил", callback_data=f'{message.from_user.id}_newevent')
                events.add(button1, types.InlineKeyboardButton(text="🗑️Удалить", callback_data=f"{message.from_user.id}_datestop=dell_{i[5]}"))
                #events.add(button1)
                events.add(types.InlineKeyboardButton(text="Скрыть", callback_data=f"{message.from_user.id}_dellmess"))
                bot.send_message(message.from_user.id, f"*Название:*\n{i[2]}\n*Дата:*\n{i[4]}\n", reply_markup=events, parse_mode= "Markdown")
        else:
            bot.send_message(message.from_user.id, "❌Нет мероприятий")

    @bot.message_handler(func=lambda message: message.text =="📕Меню")# Обработчик кнопки Меню
    def text(message):
        '''Отправляет новое сообщение с настройками выбора мероприятий'''
        global all_users
        user = message.from_user.id

        if str(user) not in all_users:
            add_new_user(str(user))

        st = types.InlineKeyboardMarkup()
        st.add(types.InlineKeyboardButton(text="📋Формат мероприятия", callback_data=f"{user}_settings_1"))
        st.add(types.InlineKeyboardButton(text="📆Дата проведения", callback_data=f"{user}_settings_2"))
        st.add(types.InlineKeyboardButton(text="🎓Выброр ВУЗа", callback_data=f"{user}_settings_3"))

        if all_users[str(user)]['tp'] != 0:
            st.add(types.InlineKeyboardButton(text="✅Начать поиск", callback_data=f"{user}_startsarch"))
        bot.send_message(message.from_user.id, "Настройки: ", reply_markup=st)
    @bot.message_handler(commands=['stats'])# Обработчик кнопки Меню
    def stats(message):
        user = str(message.from_user.id)
        obj = stats_data.sql_manager()
        arr = obj.cheak_stats(user)
        mess1 = f'Ты зарегистрировался на *{arr[0]}* мероприятий '
        mess2 = f'и посетил *{arr[1]}* из них.'
        if arr[0] == 0:
            mess1 = 'Ты не регистрировался на мероприятия '
        if arr[1] == 0:
            mess2 = f'и не посетил ни одного из них.'
        mess = mess1+mess2
        bot.send_message(message.from_user.id, mess, parse_mode="Markdown")

    ''' CALLBACKER FOR ALL DATE_CALL'''
    @bot.callback_query_handler(func=lambda call:True)# Обработчик callback-а кнопок типа InlineKeyboardMarkup
    def callback_query(call):
        global all_users, comment
        user = call.data.split('_')[0]
        if user not in all_users:
            add_new_user(user)
        req = call.data.split('_')[1]

        def add_date():
            '''Добавляет мероприятие в sql-таблицу'''
            global comment
            user = call.data.split('_')[0]
            hours = call.data.split('_')[2].split()[2].split("–")[0].replace(':', ' ')
            time = (datetime.strptime(hours, '%H %M') + dt_mg.timedelta(hours=-1)).time()
            t = datetime.strptime(hours, '%H %M').time()
            f = '17:00:00'
            n_call = 0

            if comment != {}:
                date_arr = comment[user][1]
            else:
                date_arr = ["", ""]

            date_manager = f"{call.data.split('_')[2].split()[0]} {en_sg[ru.index(call.data.split('_')[2].split()[1])]} {datetime.now().year}"
            date1 = datetime.strptime(date_manager, '%d %b %Y')
            date2 = date1 + dt_mg.timedelta(days=-1)

            today = str(date1).split()[0] + ' ' + str(time)[:5]
            #print(today)
            backtomorrow = str(date2).split()[0] + ' '+f[:5]
            #print(today, backtomorrow)
            s = date_sql.sql_manager()
            s.reg(user, today, date_arr, 0)
            return s.reg(user, backtomorrow, date_arr, 1)#[n, [arg[0], arg[2], arg[1]]]

        def pagefolder(page_date, date):
            '''Создает календарь'''
            global all_users
            test1 = types.InlineKeyboardMarkup()
            text = []
            if date != '':
                if f"{call.data.split('_')[2]} {all_users[user]['mou_date']}" not in all_users[user]['date']:
                    all_users[user]['date'].append(f"{call.data.split('_')[2]} {all_users[user]['mou_date']}")
                else:
                    all_users[user]['date'].remove(f"{call.data.split('_')[2]} {all_users[user]['mou_date']}")

            for i in range(1,31)[page_date-9:page_date]:
                #print(all_users['date'])
                if f"{i} {all_users[user]['mou_date']}" in all_users[user]['date']:
                    text.append(f'✅ {i}')
                else:
                    text.append(f' {i}')
                if i % 3 == 0:
                    test1.add(types.InlineKeyboardButton(text=text[0], callback_data=f"{user}_date_"+ str(i-2)),
                    types.InlineKeyboardButton(text=text[1], callback_data=f"{user}_date_"+ str(i-1)),
                    types.InlineKeyboardButton(text=text[2], callback_data=f"{user}_date_"+ str(i)))
                    text = []
            test1.add(types.InlineKeyboardButton(text="<<", callback_data=f"{user}_back"),
            types.InlineKeyboardButton(text=">>", callback_data=f"{user}_next"))
            if all_users[user]['date'] != []:
                test1.add(types.InlineKeyboardButton(text="Сбросить", callback_data=f"{user}_reset_date"))
            test1.add(types.InlineKeyboardButton(text="🔴Назад", callback_data=f"{user}_settings_0"))
            bot.edit_message_text("Выбери дату", reply_markup = test1, chat_id=call.message.chat.id, message_id=call.message.message_id)

        def select_tape_event(tabe, user, chat, message):
            '''Создает страницу для выбора типа мероприятия'''
            global all_users
            if all_users[user]['tp'] != tabe:
                all_users[user]['tp'] = tabe
                events_names = {1:"Проф классам", 2:"Олимпиады", 3:"Дни открытых дверей", 4:"Мероприятия"}
                tp = types.InlineKeyboardMarkup()
                for event in events_names:
                    if event == all_users[user]['tp']:
                        tp.add(types.InlineKeyboardButton(text=f"✅{events_names[event]}", callback_data=f"{user}_tp{event}"))
                    else:
                        tp.add(types.InlineKeyboardButton(text=f"▫{events_names[event]}", callback_data=f"{user}_tp{event}"))
                tp.add(types.InlineKeyboardButton(text="🔴Назад", callback_data=f"{user}_settings_0"))
                all_users[user]['f'] = 0
                all_users[user]['arr'] = []
                all_users[user]['page'] = -1
                bot.edit_message_text("Форматы: ", reply_markup = tp, chat_id=chat, message_id=message)
            else:
                pass

        def text_messages1(message, user):
            '''Функция для поиска мероприятий принимает сообщение и id юзера'''
            global all_users
            if user not in all_users:
                add_new_user(user)
            def send_mess(arg, user):
                '''Функция для создания сообщения с мероприятием'''
                global en, ru, comment, all_users
                url = types.InlineKeyboardMarkup()
                hours = ''
                #print(arg[1])
                if len(arg[1].split(" ")) > 2:
                    hours = arg[1].split(" ")[2]
                #print(arg[3])
                button1 = types.InlineKeyboardButton("Регистрация", url=str(arg[2]))#url=str(arg[2]), callback_data=f'{message.from_user.id}_newevent')
                if len(arg[3].split()) > 1 and arg[3].split()[0] != "--":
                    tape = arg[3].split()[1]
                    spots = arg[3].split()[0]
                else:
                    tape = '-'
                    spots = '-'
                date_call = arg[0]+arg[1]
                if arg[5] != "":
                    if arg[5][0] == "'":
                        arg[5]= arg[5][1:len(arg[5])-1]
                    #print(arg[5])
                    photo = urlopen(arg[5])
                    #print(photo)
                else:
                    photo = 'empty'
                n = 0
                comment[user] = [n, [arg[0], arg[2], arg[1]]]
                if arg[1].split()[0].isdigit() and (arg[1].split()[1] in ru):
                    button2 = types.InlineKeyboardButton("Уведомить", callback_data = f"{user}_settime_{arg[1]}")
                    url.add(button1, button2)
                else:
                    tape = '-'
                    spots = '-'
                    arg[1] = '\n\n'.join(arg[1].split(", "))
                    url.add(button1)
                if tape == '-' and spots == '-':
                    mes = '{page}) *{head}*\n\n▫*Университет:*\n{deskrp}\n\n▫*Дата:*\n{dt}'.format(page=all_users[user]['page']+1, head=arg[0], deskrp=arg[4], dt=arg[1])
                else:
                    mes = '{page}) *{head}*\n\n▫*Университет:*\n{deskrp}\n\n▫*Дата:*\n{dt}\n\n▫*Формат проведения:*\n{tape}\n\n▫*Кол-во мест:*\n{spots}'.format(page=all_users[user]['page']+1, head=arg[0], deskrp=arg[4], dt=arg[1], tape = tape, spots = spots)
                return mes, url, photo

            s = {1:'prof', 2:'olimpiads', 3:"doors", 4:'event'}
            if all_users[user]['tp'] in s:
                d = mydate_sql0.sql_manager(s[all_users[user]['tp']])
                all_users[user]['fun'] = d.cheak_date(all_users[user]['date'], all_users[user]['page'], all_users[user]['less'])
            def edi_mes(user, mes, url, photo):
                global all_users, comment
                bn1 = '-'
                bn2 = '-'
                #print(url)
                if all_users[user]['fun'][1] == 1 and all_users[user]['page'] > 0:
                    bn1 = types.InlineKeyboardButton(text="<<", callback_data=f"{user}_backtsarch")
                    bn2 = types.InlineKeyboardButton(text=">>", callback_data=f"{user}_startsarch")

                elif all_users[user]['fun'][1] == 0 and all_users[user]['page'] > 0:
                    bn1 = types.InlineKeyboardButton(text="<<", callback_data=f"{user}_backtsarch")

                elif all_users[user]['fun'][1] == 1 and all_users[user]['page'] == 0:
                    bn1 = types.InlineKeyboardButton(text=">>", callback_data=f"{user}_startsarch")
                    #comment[str(user)].append(url)
                elif all_users[user]['fun'][1] == 2:
                    pass
                comment[str(user)].append([bn1, bn2])
                #print(comment[str(user)])
                if bn2 != '-' and bn1 != '-':
                    url.add(bn1, bn2)
                elif bn2 == '-' and bn1 != '-':
                    url.add(bn1)
                #url.add(types.InlineKeyboardButton(text="🔧Насторойки", callback_data=f"{user}_settings_0"))
                #print(url)
                if photo != "emoty":
                    bot.delete_message(message.chat.id, message.message_id)
                    #all_users[user]['xz'] +=1
                    url.add(types.InlineKeyboardButton(text="🔧Насторойки", callback_data=f"{user}_settings_0"))
                    mess = bot.send_photo(message.chat.id, photo, caption = mes, reply_markup = url, parse_mode= "Markdown")
                    all_users[user]['last_photo'] = 1
                else:
                    bot.delete_message(message.chat.id, message.message_id)
                    #all_users[user]['xz'] +=1
                    url.add(types.InlineKeyboardButton(text="🔧Насторойки", callback_data=f"{user}_settings_0"))
                    mess = bot.send_message(message.chat.id, text = mes, reply_markup = url, parse_mode= "Markdown")
                    all_users[user]['last_photo'] = 0

                #bot.edit_message_text(mes, reply_markup = url, parse_mode= "Markdown", chat_id=message.chat.id, message_id=message.message_id)
            f = 0
            if all_users[user]['fun'][0] != "empty":
                #print(all_users[user]['fun'][0])
                #print(all_users[user]['fun'][0][5])
                all = send_mess(all_users[user]['fun'][0], user)
                mes = all[0]
                url = all[1]
                photo = all[2]
                edi_mes(user, mes, url, photo)
            else:
                end = types.InlineKeyboardMarkup()
                end.add(types.InlineKeyboardButton(text="🔧Настройки", callback_data=f"{user}_settings_0"))
                bot.edit_message_text("Мероприятий не найдено, поменяй настройки поиска.", reply_markup = end, parse_mode= "Markdown", chat_id=message.chat.id, message_id=message.message_id)


                '''if photo != "emoty":
                    if all_users[user]['last_photo'] == 0:
                        print(11)
                        #bot.delete_message(message.chat.id, message.message_id)
                        bot.send_photo(message.chat.id, photo, caption = mes, reply_markup = url, parse_mode= "Markdown")
                        all_users[user]['last_photo'] = 1
                    else:
                        bot.edit_message_media(media=types.InputMedia(type='photo', media=photo, caption = ''),reply_markup = url, chat_id=message.chat.id, message_id=message.message_id)
                        bot.edit_message_caption(caption = mes,parse_mode="Markdown", chat_id=message.chat.id, message_id=message.message_id)
                    #all_users[user]['last_photo'] = 1
                else:
                    if all_users[user]['last_photo'] == 0:
                        bot.edit_message_text(mes, reply_markup = url, parse_mode= "Markdown", chat_id=message.chat.id, message_id=message.message_id)
                        #all_users[user]['last_photo'] = 0
                    else:
                        bot.delete_message(call.message.chat.id, call.message.message_id)
                        bot.send_message(message.chat.id, mes, reply_markup = url, parse_mode= "Markdown")
                        all_users[user]['last_photo'] = 0'''

                            #bot.send_message(message.from_user.id, "Нажми, чтобы посмотреть другие", reply_markup=reg)
            #bot.send_message(call.message.chat.id, "Теперь нажми на кнопку", reply_markup=markup1)
        def univ(adder):
            '''Функция для создания страницы со списком университетов'''
            all_users[user]['f'] = 0
            all_users[user]['page'] = -1
            if adder not in all_users[user]['less'] and adder != '':
                all_users[user]['less'].append(adder)
            elif adder in all_users[user]['less']and adder != '':
                all_users[user]['less'].remove(adder)
            un = types.InlineKeyboardMarkup()
            for key in list(univer_prof.keys())[all_users[user]['page_for_less']-5:all_users[user]['page_for_less']]:
                if key in all_users[user]['less']:
                    un.add(types.InlineKeyboardButton(text= f'✅ {key}', callback_data=f'{user}_univ_{key}'))
                else:
                    un.add(types.InlineKeyboardButton(text=f'{key}', callback_data=f'{user}_univ_{key}'))
            un.add(types.InlineKeyboardButton(text="<<", callback_data=f"{user}_backforless"),
            types.InlineKeyboardButton(text=">>", callback_data=f"{user}_nextforless"))
            if all_users[user]['less'] != []:
                un.add(types.InlineKeyboardButton(text="Сбросить", callback_data=f"{user}_reset_un"))
            un.add(types.InlineKeyboardButton(text="🔴Назад", callback_data=f"{user}_settings_0"))
            bot.edit_message_text("Список университетов: ", reply_markup = un, chat_id=call.message.chat.id, message_id=call.message.message_id)

        '''Обработчики data.call'''
        if req == "datestop": #Удаляет мероприятие из таблицы
            url = types.InlineKeyboardMarkup()
            bn1 = comment[str(user)][2][0]
            bn2 = comment[str(user)][2][1]
            reg = types.InlineKeyboardButton("Регистрация", url=str(comment[str(user)][1][1]))
            yv = types.InlineKeyboardButton("Уведомить", callback_data = f'{user}_settime_{comment[str(user)][1][2]}_{0}_{user}')
            url.add(reg, yv)
            if bn1!= '-' and bn2!='-':
                url.add(bn1, bn2)
            elif bn1!= '-' and bn2=='-':
                url.add(bn1)
            #print(url)
            url.add(types.InlineKeyboardButton(text="🔧Насторойки", callback_data=f"{user}_settings_0"))
            bot.edit_message_reply_markup(reply_markup=url,chat_id=call.message.chat.id, message_id=call.message.message_id)
            #bot.delete_message(call.message.chat.id, call.message.message_id)
            date_sql.sql_manager().delete(call.data.split('_')[2])
            #date_sql.sql_manager().delete(call.data.split('_')[0], call.data.split('_')[2])
            cheak()
        if req == "datestop=dell":
            bot.delete_message(call.message.chat.id, call.message.message_id)
            date_sql.sql_manager().delete(call.data.split('_')[2])
            cheak()

        if req == "settime":#Добавляет мероприятие в таблицу
            url = types.InlineKeyboardMarkup()
            #print(comment[str(user)][2])
            bn1 = comment[str(user)][2][0]
            bn2 = comment[str(user)][2][1]
            id = add_date()
            reg = types.InlineKeyboardButton("Регистрация", url=str(comment[str(user)][1][1]))
            yv = types.InlineKeyboardButton("🔔Уведомить", callback_data = f'{user}_datestop_{id}')
            url.add(reg, yv)
            if bn1!= '-' and bn2!='-':
                url.add(bn1, bn2)
            elif bn1!= '-' and bn2=='-':
                url.add(bn1)
            url.add(types.InlineKeyboardButton(text="🔧Насторойки", callback_data=f"{user}_settings_0"))
            bot.edit_message_reply_markup(reply_markup = url,chat_id=call.message.chat.id, message_id=call.message.message_id)
            cheak()

        if req in ["tp1", "tp2","tp3","tp4"]:#Добавляет мероприятие в таблицу
            select_tape_event(int(req[2]), user, call.message.chat.id, call.message.message_id)

        if req == "reset":#Сбрасывает выбранные фильтры
            if call.data.split('_')[2] == "un" and all_users[user]['less'] != []:
                all_users[user]['less'] = []
                univ('')
            elif call.data.split('_')[2] == "date"and all_users[user]['date'] != []:
                all_users[user]['date'] = []
                pagefolder(all_users[user]['page_date'], '')
        if req == "univ":#Вызывает функцию для создания стараницу с университетами
            adder = call.data.split('_')[2]
            univ(adder)
        if req == "newevent":
            #print(1111)
            cl = stats_data.sql_manager()
            cl.add_stats(str(user), "count1")

        if req == "settings":#Создает стараницу в зависимости от индекса(0 - Меню, 1 - Выбор типа мероприятия, 2 - Список с университетами)
            if call.data.split('_')[2] == '0':
                st = types.InlineKeyboardMarkup()
                st.add(types.InlineKeyboardButton(text="📋Формат мероприятия", callback_data=f"{user}_settings_1"))
                st.add(types.InlineKeyboardButton(text="📆Дата проведения", callback_data=f"{user}_settings_2"))
                st.add(types.InlineKeyboardButton(text="🎓Выброр ВУЗа", callback_data=f"{user}_settings_3"))
                if all_users[user]['tp'] != 0:
                    st.add(types.InlineKeyboardButton(text="✅Начать поиск", callback_data=f"{user}_startsarch"))
                    #all_users[user]['xz']
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(call.message.chat.id, "Настройки: ", reply_markup = st)
                '''if all_users[user]['last_photo'] == 0:
                    bot.edit_message_text("Настройки: ", reply_markup = st, chat_id=call.message.chat.id, message_id=call.message.message_id)
                else:
                    bot.edit_message_caption("Настройки: ", reply_markup = st, chat_id=call.message.chat.id, message_id=call.message.message_id)'''

            elif call.data.split('_')[2] == '1':
                all_users[user]['page'] = -1
                events_names = {1:"Проф классам", 2:"Олимпиады", 3:"Дни открытых дверей", 4:"Мероприятия"}
                tp = types.InlineKeyboardMarkup()
                for event in events_names:
                    if event == all_users[user]['tp']:
                        tp.add(types.InlineKeyboardButton(text=f"✅{events_names[event]}", callback_data=f"{user}_tp{event}"))
                    else:
                        tp.add(types.InlineKeyboardButton(text=f"▫{events_names[event]}", callback_data=f"{user}_tp{event}"))
                tp.add(types.InlineKeyboardButton(text="🔴Назад", callback_data=f"{user}_settings_0"))
                #all_users[user]['xz']
                mess = bot.edit_message_text("Форматы: ", reply_markup = tp, chat_id=call.message.chat.id, message_id=call.message.message_id)
                all_users[user]['xz'] = mess.message_id

            elif call.data.split('_')[2] == '2':
                all_users[user]['page'] = -1
                mounth = types.InlineKeyboardMarkup()
                for i in range(len(ru))[0::3]:
                    mounth.add(types.InlineKeyboardButton(text=f'{ru[i]}', callback_data=f'{user}_mou_{ru[i]}'),
                    types.InlineKeyboardButton(text=f'{ru[i+1]}', callback_data=f'{user}_mou_{ru[i+1]}'),
                    types.InlineKeyboardButton(text=f'{ru[i+2]}', callback_data=f'{user}_mou_{ru[i+2]}'))
                mounth.add(types.InlineKeyboardButton(text="🔴Назад", callback_data=f"{user}_settings_0"))
                bot.edit_message_text("Календарь", reply_markup = mounth, chat_id=call.message.chat.id, message_id=call.message.message_id)
            else:
                adder = ''
                univ(adder)
        elif req == "dellmess":
            bot.delete_message(call.message.chat.id, call.message.message_id)

        elif req == "mou": # Создает страницу с месяцами
            all_users[user]['page'] = -1
            all_users[user]['mou_date'] = call.data.split('_')[2]
            pagefolder(all_users[user]['page_date'], '')

        elif req == "startsarch":# Вызывает функцию для перехода на новую страницу с мероприятием
            all_users[user]['page']+=1
            text_messages1(call.message, call.data.split('_')[0])

        elif req == "stay":
            text_messages1(call.message, call.data.split('_')[0])

        elif req == "backtsarch":# Вызывает функцию для перехода на прошлую страницу с мероприятием
            all_users[user]['page']-=1
            text_messages1(call.message, call.data.split('_')[0])

        elif req == "back":# Вызывает функцию для перехода на прошлую страницу с выборам даты
            if all_users[user]['page_date'] >9:
                all_users[user]['page_date']-=9
                pagefolder(all_users[user]['page_date'], '')

        elif req == "next":# Вызывает функцию для перехода на новую страницу с выборам даты
            if all_users[user]['page_date'] <31:
                all_users[user]['page_date']+=9
                pagefolder(all_users[user]['page_date'], '')

        elif req == "backforless":# Вызывает функцию для перехода на прошлую страницу с выборам университата
            if all_users[user]['page_for_less'] >5:
                all_users[user]['page_for_less']-=5
                univ('')

        elif req == "nextforless":# Вызывает функцию для перехода на новую страницу с выборам университата
            if all_users[user]['page_for_less'] <16:
                all_users[user]['page_for_less']+=5
                univ('')

        elif req == "date": # Вызывает функцию для обработки выбранной даты
            pagefolder(all_users[user]['page_date'], call.data.split('_')[2])
            all_users[user]['page'] = -1
            all_users[user]['fun'] = ["", ""]
            all_users[user]['arr'] = []
            all_users[user]['f'] = 0
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(e)
            time.sleep(5)
if __name__ != '__main__':
    tbot()
