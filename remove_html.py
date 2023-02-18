sentence = ' Tweet 0. .Skrillex is back with new album Quest For Fire featuring a tracklist of legends 🔥 https://t.co/QhzDL6Xvhf https://t.co/pkvHlQXb1N.' \
           + '\nTweet 1. Rumor has it that listening to JordanCWDavis\'s BluebirdDays is a surefire way to turn any overcast day into the p… https://t.co/zuv78PDZe5.'\
           + '\nTweet 2. RT SpotifyUSA: .iconapop and wearegalantis join forces on the new single I Want You ✨ https://t.co/tWtf4k2Zro https://t.co/1GYa0HeVje.'\
           + '\nTweet 3. No thoughts just Lana https://t.co/JvjDbKVpdo/'\
           + '\nTweet 4. .lorde is the newest member of the BillionsClub ✨ Royals takes the crown with 1 Billion streams 👑… www.ee.ucl.ac.uk'

# text = re.sub(r'^https?:\/\/.*[\r\n]*', '', sentence, flags=re.MULTILINE)

def removeURL(text):
    import re
    text_without_url = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
    return text_without_url

print(removeURL(sentence))
# print(text)
# # print(sentence.split())
# for i in sentence.split():
#     # print(i.split())
#     for j in range(0, len(i.split())):
#         print(i.split()[j].split('http'))