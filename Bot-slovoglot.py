from random import choice, randint, shuffle
from colorama import Fore, Back, init


def good_offer(offer):
    if offer.split()[-1] in ("а","к", "в", "с", "у", "о", "об" "ко", "во", "до", "из", "на"): return False, "1. Неродивый конец "+'"'+offer.split()[-1]+'"'+'\n'
    if len(offer.split())<4: return True, 2
    if offer.count(":") > 1 or offer.count(" — ") > 2 or offer.count('"') not in (0,2,4): return False, "3. Много двоеточий или тире\n"
    if any(symbol in offer for symbol in (',', '—', ':', '! ', '? ', '. ')):
        if (len(offer.split()) - offer.count(" — ")) / (sum(offer.count(simvol) for simvol in (',', '—', ':', '! ', '? ', '. '))) > 14:
            return False, "4. На один знак препинания приходится более 14-ти слов\n"
        hren = (", бы ", '— бы ',   ", же ", '— же ',   " в,", " в:", " в —",   " во,", " во:", " во —", \
                " к,", " к:", " к —",   " ко,", " ко:", " ко —",   " на,", " на —", " на:", \
                " до,", " до —", " до:",   " под,", " под:", " под —",   " над,", " над:", " над —", \
                " об,", " об:", " об —",  " за,", " за:", " за —",  \
                " по,", " по —", " по:", " у,", " у —", " у:",  " из,", " из:", " из —",
                " от,", " от —", " от:",   " со,", " со —", " со:", " с,", " с —", " с:")
        return all(not(i in offer) for i in hren), "5. Неродивое сочетание\n"
    elif len(offer.split()) > 12: return False, "6. Более 9-ти слов и нету знаков пунктуации\n"
    return True, 7


def make_offer(name_words_file, name_phrases_file):
    def punctuation(j, n_words): # возвращает случайный пун-ционный знак или пробел
        if j+1==n_words: return choice(["."]*40 + ["!"]*8 + ["!!!"]*2 + ["?"]*3 + ["!?"] + ["?!"] + ["..."]*3) # если последнее слово в предложении
        return choice([" "]*150 + [", "]*40 + [" — "]*6 + [": "]*2 )


    words_spisok = [i[:-1] for i in open(name_words_file, encoding='utf-8')] # список из слов файла
    phrases_spisok = [i[:-1] for i in open(name_phrases_file, "r", encoding='utf-8')] # список из фраз файла
    shuffle(words_spisok)
    line_count = len(phrases_spisok) # кол-во строк в файле с фразами

    # делаем список из кусков фраз и слов
    if line_count > 0:
        offer_spis = words_spisok[: randint(0, 5)] # срез слов из списка
    else:  # но не допускаем чтобы вообще ничего не было
        offer_spis = words_spisok[: randint(1, 5)]
    if line_count > 0 and (randint(0, 8) or len(offer_spis) == 0) : # допускаем вариант без фразы
        for n in range(randint(1,5)): # добавим 1-5 фраз
            while 1: # исключаем ситуацию, в которой из фразы возьмётся одно слово, например: "— ответ", так нельзя
                shuffle(phrases_spisok)
                phrase = phrases_spisok[randint(0, line_count-1)] # выбираем случайную фразу
                start = randint(0, len(phrase.split())-2)      # начало среза
                finish = randint(start+2, len(phrase.split())) # конец среза
                phrase = (" ".join(phrase.split()[start : finish])).strip(",.~;:()*—+_ ") # из конца куска выбранной фразы убираем пункт. Знаки кроме !? (для остатка смысла)
                if len(phrase.split()) != 1 and phrase.count('"') in (0, 2, 4):
                    break
            index_phrase = randint(0, len(offer_spis)) # куда вставим фразу
            offer_spis = offer_spis[: index_phrase] + [phrase] + offer_spis[index_phrase :] # получаем список с кусками фраз и словами
    # делаем строку из списка
    str_offer = ""
    for nw in range(len(offer_spis)):          # чтобы не добавил пробел после последнего слова с  .!? на конце
        if offer_spis[nw][-1] in ('!', '?') and nw != len(offer_spis)-1:
            str_offer += offer_spis[nw]+' '
        else:
            str_offer += offer_spis[nw]+punctuation(nw, len(offer_spis))
    # Делаем первые слова предложений с заглавной буквы
    str_offer2 = str_offer
    for i in range(len(str_offer)-1):
        if str_offer[i] in ("!", "?", ".") and i<len(str_offer)-1:
            if str_offer[i+1] == " ":
                str_offer2=str_offer2[:i+2]+str_offer[i+2].upper()+str_offer2[i+3:]
    str_offer=str_offer2.replace(str_offer[0], str_offer[0].upper(), 1)
    return str_offer


def processing_phrase(phrase):
    # убираем из фразы лишние пробелы и знак конца предложения (кроме ! и ? и их сочетаний) и делаем первую букву ВСЕЙ фразы строчной
    phrase = " ".join(phrase.split()).replace(" - ", " — ").rstrip(',:;.')
    if phrase.split()[0] != phrase.split()[0].upper() or len(phrase.split()[0]) == 1 : # если первое слово не аббревиатура, то делаем со строчной его
        phrase = phrase.replace(phrase[0], phrase[0].lower(), 1)
    # првевращаем "всмысли что ГОСТу ТаК тО пОЧемУ "Приказ", а как жЕ Игорь из ДПС?"
    #           в "всмысли что ГОСТу так то почему "Приказ", а как же Игорь из ДПС?"
    phrase_str=phrase
    phrase = phrase.split()
    for word in phrase:
        word = word.strip('"')
        if word != word[0].upper() + word[1:].lower() and (word != word.upper()) and (word != word[:-1].upper()+word[-1]):
            phrase_str = phrase_str.replace(word, word.lower(), 1)
    phrase = phrase_str
    # если есть в середине .!? то что за ними сделаем со строчной буквы всё равно # например "эх, а не плохо тут! Так ведь?" =>  "эх, а не плохо тут! так ведь?"
    phrase2=phrase
    for i in range(len(phrase)-1):
        if phrase[i] in ".?!" and not(phrase[i+1] in '"!?'):
            phrase2 = phrase2[:i+2]+phrase2[i+2].lower()+phrase2[i+3:]
    phrase=phrase2
    return phrase


def addendum(phrase, name_words_file, name_phrases_file):
    # добовляем фразу
    phrases_file = open(name_phrases_file, "r+", encoding='utf-8')
    if 1000 > len(phrase.split()) > 1 and not('\n'+phrase+'\n' in phrases_file.read()):
        phrases_file.write(phrase+"\n")
    phrases_file.close()
    # добавим незнакомые слова в файл
    for sym in ",.!?~`|[];:—–'":
        phrase = phrase.replace(sym, "") # оставляем только слова
    for word in phrase.split():
        if (word[0] == '"') or (word[-1] == '"'):
            if word[0] == '"':
                word = word.strip('"')
                word = word.replace(word[0], word[0].lower(), 1)
            word = word.strip('"')
        words_file = open(name_words_file, "r+", encoding='utf-8')
        if ('\n'+word+"\n" not in words_file.read()): # проверка наличия слов из фразы в файле
            words_file.write(word+'\n')
        words_file.close()


init()
words_file = open("words.txt", "a+", encoding='utf-8');
phrases_file = open("phrases.txt", "a+", encoding='utf-8')
print(Fore.BLACK,end=""); print("\t\t"+Back.RED+"Бот словоглот готов к диалогу")
offer=""
while True:
    print(Back.BLACK,end=""); print(Fore.WHITE,end="")
    phrase = input()
    if phrase == ".изб":
        if offer != "":
            izbr = open("избранное.txt", 'r+', encoding = 'utf-8')
            izbr.read()
            izbr.write(offer+'\n')
            izbr.close()
            continue
        else:
            phrase=""
    if phrase == ".з":
        break
    if any(sym.isalnum() for sym in phrase): # Если в фразе есть буквы или цифры, то обрабатываем дальше
        phrase = processing_phrase(phrase)
    addendum(phrase, "words.txt", "phrases.txt") # добавляем новые слова и фразы

    while 1: # создание ответа
        offer = make_offer("words.txt", "phrases.txt")
        if good_offer(offer.rstrip('!?.'))[0]:
            print(Fore.GREEN+offer)
            break
        else: print(Fore.RED+offer, Fore.YELLOW+"\nКод ошибки:", good_offer(offer.rstrip('!?.'))[1] )
input("Диалог кончен, всего тебе хорошего")
