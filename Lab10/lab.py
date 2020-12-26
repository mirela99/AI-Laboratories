import json

stop_words= set()

with open("stopwords.txt", "r", encoding="UTF-8") as file:
    for word in file.read().splitlines():
        stop_words.add(word)

symbols = [",", "!" , "?", ":", ".", ";","\"", "(",")" , "[", "]"];

def get_wordfile(file_in, file_out):
    words_dict= dict()
    w_count=0

    with open(file_in, "r", encoding="UTF-8") as file:
        for line in file.read().splitlines():
            for word1 in line.split():
                for s in symbols:
                    word1=word1.replace(s, "")

            for word in word1.split("-"):
                word=word.lower()
                if word not in stop_words and word !="":
                    if word in words_dict:
                        words_dict[word] +=1
                    else:
                        words_dict[word] = 1
                    w_count += 1;

       
    for key in words_dict.keys():
            
         words_dict[key] = int (words_dict[key] * 1000000 /w_count)

    json.dump(words_dict, open(file_out, "w"))

    return words_dict

if __name__ == "__main__":

    wd_eminescu = get_wordfile("eminescu.txt", "eminescu.json")
    wd_stanescu = get_wordfile("stanescu.txt", "stanescu.json")
    wd_blaga = get_wordfile("blaga.txt", "blaga.json")

    join_words=set()

    for x in wd_eminescu.keys():
        join_words.add(x)
    for x in wd_stanescu.keys():
        join_words.add(x)
    for x in wd_blaga.keys():
            join_words.add(x)

    scor=0
    scorr=0

    for w in join_words:
        scor1, scor2, scor3 = 0,0,0
        if w in wd_eminescu:
            scor1=wd_eminescu[w]
        if w in wd_stanescu:
            scor2= wd_stanescu[w]
        if w in wd_blaga:
                scor2= wd_blaga[w]

        scor += abs(scor1-scor2)
        scorr += abs(scor1-scor3)
 
    print("\n")
    print("Scorul Eminescu-Stanescu :", scor)

    medie =scor/ len(join_words)
    print("Media Eminescu-Stanescu : ", medie)
    print("\n")

    print("Scorul Eminescu-Blaga :", scorr)

    medie =scorr/ len(join_words)
    print("Media Eminescu-Blaga : ", medie)

    pass