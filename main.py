from re         import findall
from os         import system
from bs4        import BeautifulSoup
from time       import sleep, time
from httpx      import get
from random     import choice
from threading  import Thread, active_count, Timer
from colorama   import Fore

class Scraper:
    def __init__(self, threads: int = 70):
        self.proxies    = open("proxies.txt", "r").read().splitlines()
        self.threads    = threads
        self.time       = time()
        self.invites    = []
        self.valid      = []
        self.valid      = 0                                                                                                                                                                                                                    #xKian
        self.invalid    = 0
        self.links      = []
        
    def checkinvite(self, invite):
        try:
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
                print(  f"[{Fore.RED}-{Fore.RESET}] discord.gg/{invite}")
                self.invalid += 1
            else:
                print(f"[{Fore.GREEN}+{Fore.RESET}] discord.gg/{invite}")
                self.valid += 1
                open("invites.txt", "a").write(f"discord.gg/{invite}\n")
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] {e}")
                
    def getinvites(self, endpoint: str):
        try:
            res = get(f"https://discadia.com{str(endpoint)}").text
            invite = findall(r"discord\.com\/invite\/\w+|discordapp\.com\/invite\/\w+|discord\.gg\/\w+", res)[0].split("/")[-1]
            
            if invite in self.invites:
                return
            
            self.invites.append(invite)
            self.checkinvite(invite)
            
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] {e}")


    def getlinks(self, page: str):
        self.title()
        try:
            res = get(f"https://discadia.com/?page={page}").text
            soup = BeautifulSoup(res, "html.parser")
            
            links = soup.find_all("a", {"class": "server-join-button flex group px-2.5 py-1 space-x-1 bg-green-700/50 border border-green-600 rounded-lg hover:bg-green-700/75 hover:shadow-xl"})
            
            for link in links:
                if link["href"] in self.links:
                    break
                self.links.append(link["href"])
                self.getinvites(link["href"])
        except Exception as e:
            print(f"[{Fore.RED}-{Fore.RESET}] {e}")


    def title(self):
        system(f"title [Discord Invite Scraper] ^| By Kian#2054 ^| Valid: {self.valid} ^| Invalid: {self.invalid} ^| Threads: {active_count() - 1} ^| Elapsed: {round(time() - self.time, 2)}s")
        Timer(0.1, self.title).start()

    def start(self):
        for page in range(1, 1600):
            while active_count() > self.threads:
                sleep(0.1)
            
            Thread(target=self.getlinks, args=(page,)).start()
        

if __name__ == "__main__":
    system("cls")
    Scraper().start()
