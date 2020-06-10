import numpy as np
import re
import random
import os
import pyttsx3
from gtts import gTTS


def main(n):
    #open file pipe to read file
    with open("obama.txt", "r") as f:
        content = f.read()

    #words = re.findall(r'\w+', content)
    wordsList = content.strip().split(" ")
    wordsSet = set(wordsList)

    entryLength = len(wordsSet)
    freqWordMatrix = np.zeros((entryLength, entryLength))

    #hash table to denote words to indices(count)
    entries = {}
    for count,word in enumerate(wordsSet): 
        entries[word] = count

    wordsListLength = len(wordsList)
    for i in range(wordsListLength-1):
        freqWordMatrix[entries[wordsList[i]]][entries[wordsList[i+1]]] += 1

    #sentenceStarters
    startWords = containsPeriod(wordsList)

    #last word in startWords might be the last 
    startWords.pop()
    startWord = startWords[np.random.randint(len(startWords))]

    #perform randomWalk
    L = randomWalk(freqWordMatrix, n, entries, entries[startWord])

    text = ' '.join(L)
    print(f'\n {text} \n')
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save('text.mp3')
    os.system('mpg321 text.mp3')

#    engine = pyttsx3.init()
#    engine.setProperty('rate', 100)
#    voices = engine.getProperty('voices')
#
#    # to get the info. about various voices in our PC
#    for voice in voices:
#        if voice.id.find('english') != -1:
#            print("Voice:")
#            print("ID: %s" %voice.id, end=', ')
#            print("Name: %s" %voice.name, end=', ')
#            print("Age: %s" %voice.age, end=', ')
#            print("Gender: %s" %voice.gender, end=', ')
#            print("Languages Known: %s" %voice.languages)
#
#    engine.setProperty('voice', 'english-wmids')
#
#    engine.say(text)
#    engine.runAndWait()


def randomWalk(matrix, n, entries, startWord):
    l = len(matrix)

    entries_swapped = {value:key for key, value in entries.items()}
    arrIndex = randomWalkHelper(matrix, l, n, entries_swapped, startWord)

    arr = []
    for i in arrIndex:
        arr.append(entries_swapped[i])

    return arr

'''
REQUIRES: matrix
ENSURES: randomWalk(matrix, l, n, i, arr) returns 
l-sized list(arr) of entries of a n-step 
random walk on matrix starting at entry i
(NOTE: that the it is at least n steps, because a period must be reached)
l,n,i,startWord(index of the start word) : int
arr : list
'''
def randomWalkHelper(matrix, l, n, entries_swapped, startWord):

    arr = []
    x = startWord
    i = 0
    while True:
        S = sum(matrix[x])
        if S == 0: #sink node
            arr.append(np.random.randint(l))
        else: 
            goTo = np.random.randint(S)
            currentSum = -1
            for j in range(l):
                currentSum += matrix[x][j]
                if currentSum >= goTo:
                    arr.append(j)
                    x = j
                    break

        if i >= n:
            noNewLine = entries_swapped[x].strip()
            matchObj = re.search(r'\w+\.{1}', noNewLine)
            if matchObj:
                break
        i += 1

    return arr


'''
REQUIRES: true
ENSURES: a list of words that contain a period
'''
def containsPeriod(wordsList):
    startWords = []
    for w in wordsList:
        matchObj = re.search(r'\w+\.{1}\n{0}', w.strip())
        if matchObj:
            startWords.append(w)

    return startWords




if __name__ == "__main__":
    print("Welcome to the speech generator")
    n = int(input("How many words do you want to read?"))
    main(n)



'''
TODO: Randomly pick a sentence starter and always finish with
a period to make the sentences sound smoother
BUGS: Maximum recursion depth for requesting too many words
'''








