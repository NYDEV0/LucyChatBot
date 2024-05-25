import html
import re
import urllib.parse
import urllib.request

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

class Main():
    def __init__(self, text:str, tl:str, sl:str):
        self.text = text
        self.tl = tl
        self.sl = sl

    def translate(self) -> str:
        link = f"https://translate.google.com/m?tl=%s&sl=%s&q=%s"
        to_translate = urllib.parse.quote(self.text)
        link = link % (self.tl,self.sl,to_translate)
        request = urllib.request.Request(link, headers=header)
        raw_data = urllib.request.urlopen(request).read()
        data = raw_data.decode("utf-8")
        expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
        re_result = re.findall(expr, data)

        return self.unescape(re_result[0])

    def unescape(self,text:str) -> str:
        return html.unescape(text)

class Translate():
    def __init__(self, text):
        self.text = text

    def ToAmharic(self):
        return Main(self.text,"am","en").translate()
    
    def ToEnglish(self):
        return Main(self.text,"en","am").translate()
