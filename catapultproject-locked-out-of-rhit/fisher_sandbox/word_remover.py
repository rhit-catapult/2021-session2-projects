# Hacky testing.  Do not use or run. :)

import random


# open file and read the content in a list
with open('common_words.txt', 'r') as filehandle:
    words = filehandle.read().split('\n')

print(len(words))
print(words[random.randrange(0, len(words))])


with open('../words.txt', 'w') as filehandle:
    for word in words:
        if not "'" in word and len(word) < 9 and len(word) > 3 and word[len(word) - 1] != "s":
            filehandle.write('%s\n' % word)
