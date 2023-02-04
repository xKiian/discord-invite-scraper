import re, httpx

mhm = httpx.get("https://discordservers.com")
print(re.findall(r'discord\.com\/invite\/\w+|discord\.gg\/\w+', mhm))