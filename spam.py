from requests.sessions import Session
from requests import get
from random import choice
from multiprocessing import Process
from colorama import init,Style,Fore

BANNER = """
"""

USER_AGENTS = ["Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0",
"Mozilla/5.0 (Android 4.4; Tablet; rv:41.0) Gecko/41.0 Firefox/41.0",
"Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0",
"Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
"Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
"Opera/12.0(Windows NT 5.2;U;en)Presto/22.9.168 Version/12.00",
"Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
"Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
"Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
"Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
"Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
"Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
"Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0"]

USER_AGENT = choice(USER_AGENTS)

class Client:
    def __init__(self,username,password,proxy):
        self.ses = Session()
        self.loggedIn = False
        self.username = username
        self.password = password
        self.proxy = proxy
    
    def Login(self):
        if self.loggedIn == True:
            return None
        
        loginData = {
            "password":self.password,
            "username":self.username,
            "queryParams":"{}"
        }
        homePageResponse = self.ses.get("https://www.instagram.com/accounts/login/")
        loginHeaders = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip,deflate,br",
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "Host":"www.instagram.com",
            "Referer":"https://www.instagram.com/accounts/login/",
            "X-Requested-With":"XMLHttpRequest",
            "X-Instagram-AJAX":"1",
            "User-Agent":USER_AGENT,
            "X-CSRFToken":homePageResponse.cookies.get_dict()["csrftoken"],
        }
        loginCookies = {
            "rur":"PRN",
            "csrftoken":homePageResponse.cookies.get_dict()["csrftoken"],
            "mcd":homePageResponse.cookies.get_dict()["mcd"],
            "mid":homePageResponse.cookies.get_dict()["mid"]
        }
        self.ses.headers.update(loginHeaders)
        self.ses.cookies.update(loginCookies)

        loginPostResponse = self.ses.post("https://www.instagram.com/accounts/login/ajax/",data=loginData)
    
        if loginPostResponse.status_code == 200 and loginPostResponse.json()["authenticated"] == True:
            self.loggedIn = True
            mainPageResponse = self.ses.get("https://www.instagram.com/")
            self.ses.cookies.update(mainPageResponse.cookies)
    
    def Spam(self,username,userid):
        if self.loggedIn == False:
            return None   

        link = "https://www.instagram.com/" + username + "/"
        profileGetResponse = self.ses.get(link)
        self.ses.cookies.update(profileGetResponse.cookies)
        spamHeaders = {
            "Accept":"*/*",
            "Accept-Encoding":"gzip,deflate,br",
            "Accept-Language":"en-US,en;q=0.5",
            "Connection":"keep-alive",
            "Content-Type":"application/x-www-form-urlencoded",
            "DNT":"1",
            "Host":"www.instagram.com",
            "X-Instagram-AJAX":"2",
            "X-Requested-With":"XMLHttpRequest",
            "Referer":link,
            "User-Agent":USER_AGENT,
            "X-CSRFToken":profileGetResponse.cookies.get_dict()["csrftoken"],
        }
        spamData = {
            "reason_id":"1",
            "source_name":"profile"
        }

        self.ses.headers.update(spamHeaders)

        spamPostResponse = self.ses.post("https://www.instagram.com/users/"+ userid +"/report/",data=spamData)
        if spamPostResponse.status_code == 200 and spamPostResponse.json()["description"] == "Your reports help keep our community free of spam.":
            self.ses.close()
            return True
        else:
            return False

def Success(username,shit):
    print(Fore.GREEN +"[" + username +"]" + Style.RESET_ALL
    + " " + shit)

def Fail(username,shit):
    print(Fore.RED +"[" + username +"]" + Style.RESET_ALL
    + " " + shit)

def Status(shit):
    print(Fore.YELLOW +" - COLAK - " + Style.RESET_ALL
    + " " + shit)

def DoitAnakin(reportedGuy,reportedGuyID,username,password,proxy):
    try:
        insta = None
        if proxy != None:
            insta = Client(username,password,None)
        else:
            insta = Client(username,password,None)
        insta.Login()
        result = insta.Spam(reportedGuy,reportedGuyID)
        if insta.loggedIn == True and result == True:
            Success(username,"Tamam")
        elif insta.loggedIn == True and result == False:
            Fail(username," HESABLAR  ")
        elif insta.loggedIn == False:
            Fail(username," SIFRE YANLIS VEYA KULLANICNI ADI ")
    except:
        Fail(username," GIRIS YAPILIRKEN HATA OLDU TEKRAR DENEYIN.")

if __name__ == "__main__":
    init()
    userFile = open("account.txt","r")

    USERS = []
    for user in userFile.readlines():
        if user.replace("\n","").replace("\r","\n") != "":
            USERS.append(user.replace("\n","").replace("\r","\n"))


    print(Fore.RED + BANNER + Style.RESET_ALL)
    Status(str(len(USERS)) + " ADET HESAP YÜKLENDİ!\n")
    reportedGuy = input(Fore.GREEN + " HEDEF KULLANICI : " + Style.RESET_ALL)
    reportedGuyID = input(Fore.GREEN + "USER ID : " + Style.RESET_ALL)
    print("")
    Status(" SPAM BASLADI ...\n")

    for user in USERS:
        p = Process(target=DoitAnakin,args=(reportedGuy,reportedGuyID,user.split(" ")[0],user.split(" ")[1],None))
        p.start()
