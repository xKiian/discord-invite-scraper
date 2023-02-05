from re         import findall
from os         import system
from time       import sleep
from httpx      import get
from random     import choice
from threading  import Thread, active_count
from colorama   import Fore

class Scraper:
    def __init__(self):
        self.proxies    = open("proxies.txt", "r").read().splitlines()
        self.invites    = []
        self.valid      = []
        self.categories = [
            "gaming",
            "streamer",
            "programming",
            "community",
            "anime",
            "roleplay",
            "social",
            "nsfw",
            "minecraft",
            "chill",
            "music",
            "roblox",
            "nft",
            "games",
            "furry",
            "crypto",
            "art",
            "hangout",
        ]

    def checkinvite(self, url):
        while True:
            try:
                invite = url.split("/")[-1]

                headers = {
                    "authority"          : "discord.com",
                    "accept"             : "*/*",
                    "accept-language"    : "en-US;q=0.8,en;q=0.7",
                    "content-type"       : "application/json",
                    "pragma"             : "no-cache",
                    "sec-ch-ua"          : '"Chromium";v="108", "Google Chrome";v="108", "Not;A=Brand";v="99"',
                    "sec-ch-ua-mobile"   : "?0",
                    "sec-ch-ua-platform" : '"Windows"',
                    "sec-fetch-dest"     : "empty",
                    "sec-fetch-mode"     : "cors",
                    "sec-fetch-site"     : "same-origin",
                    "user-agent"         : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
                }

                data = {
                    "with_expiration": True,
                    "inputValue": invite,
                    "with_counts": True,
                }

                req = get(
                    f"https://discord.com/api/v9/invites/{invite}",
                    headers=headers,
                    params=data,
                    proxies="http://" + choice(self.proxies),
                )
                if req.status_code == 404:
                    print(f"[{Fore.RED}-{Fore.RESET}] discord.gg/{invite}")
                else:
                    print(f"[{Fore.GREEN}+{Fore.RESET}] discord.gg/{invite}")
                    self.valid.append(invite)
                break
            except:
                pass

    def getinvites(self, category):
        res = get(f"https://search.discordservers.com/?size=250&from=0&keyword={category}").text

        found_invites = findall(r"discord\.com\/invite\/\w+|discord\.gg\/\w+", res)
        self.invites.extend(found_invites)

        print(f"[{Fore.GREEN}+{Fore.RESET}] Scraped {len(found_invites)} invites")

    def waitfrothreads(self):
        while active_count() > 1:
            sleep(0.1)

    def start(self):
        for category in self.categories:
            Thread(target=self.getinvites, args=(category,)).start()

        self.waitfrothreads()

        self.invites = list(set(self.invites))
        print(f"[{Fore.CYAN}!{Fore.RESET}] Checking {len(self.invites)} invites...")


        for invite in self.invites:
            Thread(target=self.checkinvite, args=(invite,)).start()

        self.waitfrothreads()

        print(f"[{Fore.GREEN}+{Fore.RESET}] Found {len(self.valid)} valid invites")
        with open("valid.txt", "w") as f:
            f.write("\n".join(self.valid))


if __name__ == "__main__":
    system('naiK yb - reparcS etivnI eltit && slc'[::-1])
    Scraper().start()
