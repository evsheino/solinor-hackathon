from pattern.web import URL, DOM, plaintext, POST
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from pattern.web import abs, extension

class W3Techs:

    baseurl = 'http://w3techs.com/sites/info/'

    def __init__(self, domain):
        self.domain = domain
        self.data = {}

    def analyze(self):
        url = URL(W3Techs.baseurl + self.domain)
        dom = DOM(url.download(unicode=True))

        if len(dom('.tech_main form')) >= 2: #it is not crawled yet!
            self.crawl()
            url = URL(W3Techs.baseurl + self.domain)
            dom = DOM(url.download(unicode=True))
        

        headers = []
        contents = []
        last_header = None
        #analyze
        for div in dom('.tech_main p')[1:]:
            # if it is header
            if 'si_h' in div.attrs.get('class', ''):
                last_header = plaintext(div.content)
                self.data[last_header] = None
            elif 'si_tech' in div.attrs.get('class', ''):
                content = plaintext(div.content)
                self.data[last_header] = content

            

    def crawl(self):
        #submit the form
        dom = DOM(URL(string=W3Techs.baseurl + self.domain, method=POST, query={'add_site': ' Crawl now! '}).download())
        