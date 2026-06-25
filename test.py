from email import message

# create 24 Mar 2025
print("Selamat datang di modul pembelajaran ulang buku 'PYTHON CRASH COURSE'")
print(" A + B = C")
A = 9
B = 10
C = A + B
print(C)

# methhod string case
message = "ini adalah latihan changing case in string with method"
print(message)
name = "ardx"
print(name)
name = "ardx"
print(name.title())
name = "ardx"
print(name.upper())
name = "ardx"
print(name.lower())
print("Hello " + name.title() + "!")

# whitespace to strinng tabs or newlines
message = "whitespace to string tabs or newlines"
print(message)
print("Languages:\nPython\nC\nJavaScript")
Languages = "Python\nC\nJavaScript" 
bahasa_kesukaan = 'python~chan'
bahasa_kesukaan = bahasa_kesukaan.rstrip()
print(bahasa_kesukaan)

#modul removing prefixes
print("Modul Removing Prefixes")
nostarch_url = 'https://www.rucoyonline.com/characters/Cprs%20Knight'
nostarch_url.removeprefix('https://')
simple_url = nostarch_url.removeprefix('https://')
print("https://www.rucoyonline.com/characters/Cprs%20Knight")

#integer
print("modul integer")
print (10 + 20 ** 5 / 7)
print ( 1 + 1)
print (2 / 1)
print ( 5 - 1 )
print ( 2 ** 2)

#pemahaman list
print("Pembahasan list")
waifu_ardx_azurlane = ['noshiro', 'roon', 'newjersey', 'bismarck', 'Agir', 'scylaa', 'Gouden Leeuw', 'prinz eugen', 'Kala Ideas', 'friedrich der grobe', 'duisburg']
print(waifu_ardx_azurlane)
# ambil waifu urus 0 - akhir
print(waifu_ardx_azurlane[0])
print(waifu_ardx_azurlane[7])
#ambil ke dari belakang waifu
print(waifu_ardx_azurlane[-1])
print(waifu_ardx_azurlane[-3])
message = f"waifu pertama saya adalah {waifu_ardx_azurlane[0].title()}."
message1 = f"waifu oath pertama saya {waifu_ardx_azurlane[-4].title()}."
print(message)
print(message1)

#modifying element in a list
print(".")
print("modifying element in a list")
# waifu besar dw
waifu_iron_blood = 'Agir', 'Bismarck', 'Roon', 'Fiedrich der grobe', 'Mecklenburg', 'Duisburg'
waifu_royal_navy = 'Lion', 'Implacable', 'Trafalgar', 'Perseus', 'Sirius', 'Scylaa', 'Plymouth'
waifu_eagle_union = 'Kearsarge', 'Anchorage', 'Kansas', 'Newjersey', 'Franklin', 'Santafe', 'Hornet'
waifu_sakura_empire = 'Azuma', 'Hakuryuu', 'Daisen', 'Izumo', 'Shimanto', 'Akagi', 'Mushashi', 'Shinano', 'Kaga', 'Owari', 'Taihou'
waifu_northern_parliament = 'Admiral nakhimov', 'Chikavol', 'Sovetsky soyuz', 'Kazan', 'Kursk', 'Oleg', 'Poltava'
waifu_dragon_empery = 'Harbin', 'Chenwu', 'Chian', 'Hwahjah'
waifu_iris_libre = 'Brest', 'bayard', 'Sait louis', 'Alsace', 'Brennus'
waifu_vichya_dominion = 'Mogador'
waifu_sardegna_empire = 'Napoli', 'Raffaello', 'Andrea doria', 'Guillio cesare muse'
waifu_kingdom_tulipa = 'Gouden Leeuw', 'De zenev provincien'
waifu_tempesta = 'Fancy', 'Goldenhind', "Ganji sawai", 'Royal fortune', 'Mary celeste'

