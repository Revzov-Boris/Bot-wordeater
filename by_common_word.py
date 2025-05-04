from random import shuffle
from colorama import Fore


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
        k = None
        k2 = None
        for obsh_word in ofr2.split():
            if obsh_word in ofr.split():
                k = ofr.split().index(obsh_word)
                k2 = ofr2.split().index(obsh_word)
                break
        o = ""
        o2 = ""
        for i in ofr.split()[:k+1]:
            o += i+" "
        for i in ofr2.split()[k2+1:]:
            o2+=i+" "
        o2 = o2.strip()
        if (o+o2 == ofr) or (o+o2 == ofr2) or (o+o2 in ofr) or (o+o2 in ofr2):
            continue

        print('"'+Fore.YELLOW+o+o2+Fore.WHITE+'"')
        print(ofr+"\n"+ofr2)
        print(obsh_word)
        print(k, k2)

        return o+o2

while 1:
    offer = two_offer_with_same_word("phrases.txt")
    print(Fore.RED+"Предложение выведено"+Fore.WHITE)
    otvet = input()
    if otvet == ".изб":
            izbr = open("избранное.txt", 'r+', encoding = 'utf-8')
            izbr.read()
            izbr.write(offer+'\n')
            izbr.close()


