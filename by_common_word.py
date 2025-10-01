from random import shuffle
from colorama import Fore
from random import choice


def two_offer_with_same_word(name_phrases_file):
    while 1:
        s = [i for i in open(name_phrases_file, encoding='utf-8').read().split('\n') if i != ""] # список с фразами
        shuffle(s)
        for ofr in s:
            if len(ofr.split())>=3:
                break
        flag = False
        for ofr2 in s:
            if (ofr2 != ofr) and (len(ofr2.split())>=3) and any((i in ofr.split()[1:-1]) for i in ofr2.split()[:-1]):
                flag = True
                break
        if not(flag): # в случае если не нашлось предложения, содержащего хоть одно слово из первого
            continue

        couples_indexes = [] # пары индексов
        for obsh_word_index1 in range(1, len(ofr.split())):
            for obsh_word_index2 in range(len(ofr2.split())):
                if ofr.split()[obsh_word_index1] == ofr2.split()[obsh_word_index2]:
                    couples_indexes.append((obsh_word_index1, obsh_word_index2))
        if len(couples_indexes) == 0:
            continue

        k, k2 = choice(couples_indexes) # индекс общего слова в ofr и индекс общего слова в ofr2
        o = ""
        o2 = ""
        for i in ofr.split()[:k+1]:
            o += i+" "
        for i in ofr2.split()[k2+1:]:
            o2+=i+" "
        o2 = o2.strip()
        generated_offer = o + o2
        if (generated_offer in ofr) or (generated_offer in ofr2):
            continue

        print('"' + Fore.YELLOW + generated_offer + Fore.WHITE + '"')
        print(ofr+"\n"+ofr2)
        print(ofr.split()[k])
        print(couples_indexes)
        print(k, k2)

        return generated_offer

while 1:
    offer = two_offer_with_same_word("phrases.txt")
    print(Fore.RED+"Предложение выведено"+Fore.WHITE)
    otvet = input()
    if otvet == ".изб":
            izbr = open("избранное.txt", 'r+', encoding = 'utf-8')
            izbr.read()
            izbr.write(offer+'\n')
            izbr.close()


