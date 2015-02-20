import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from pattern.web import abs, extension

languages = {
    'ASP.NET' : {
        'type': 'backend',
        'extensions' : ['asp', 'aspx', 'axd', 'asx', 'asmx', 'ashx', 'axd', 'asx', 'asmx', 'ashx']
    },
    'CSS' : {
        'type': 'frontend',
        'extensions' : ['css']
    },
    'Coldfusion' : {
        'type': 'backend',
        'extensions' : ['cfm']
    },
    'Erlang' : {
        'type': 'backend',
        'extensions' : ['yaws']
    },
    'Flash' : {
        'type': 'frontend',
        'extensions' : ['swf']
    },
    'HTML' : {
        'type': 'frontend',
        'extensions' : ['html', 'htm', 'xhtml', 'jhtml']
    },
    'Java' : {
        'type': 'backend',
        'extensions' : ['jsp', 'jspx', 'wss', 'do', 'action']
    },
    'JavaScript' : {
        'type': 'frontend',
        'extensions' : ['js']
    },
    'Perl' : {
        'type': 'backend',
        'extensions' : ['pl']
    },
    'PHP' : {
        'type': 'backend',
        'extensions' : ['php', 'php4', 'php5', 'phtml']
    },
    'Python' : {
        'type': 'backend',
        'extensions' : ['py']
    },
    'Ruby' : {
        'type': 'backend',
        'extensions' : ['rb', 'rhtml']
    },
    'XML' : {
        'type': 'frontend',
        'extensions' : ['xml', 'rss', 'svg']
    },
    'C++' : {
        'type': 'backend',
        'extensions' : ['c', 'cgi', 'dll']
    },
}


class Predictor():

    backend_languages = []
    frontend_languages = []

    def __init__(self, url, dom):
        """
        :type url: pattern.web.URL
        :type dom: pattern.web.DOM
        """
        self.url = url
        self.dom = dom


    def predict_programming_language(self):
        used_extensions = set()
        #check urls
        #if local and ends with one of the extentions, predict language
        for link in self.dom.by_tag("a"):
            link = link.attrs.get("href","")
            link = abs(link, base=self.url.redirect or self.url.string)
            if self.url.domain in link: 
                e = extension(link)
                if e:
                    used_extensions.add(e[1:]) #add extension, and omit the .

        #forms
        for link in self.dom.by_tag("form"):
            link = link.attrs.get("action","")
            link = abs(link, base=self.url.redirect or self.url.string)
            if self.url.domain in link: 
                e = extension(link)
                if e:
                    used_extensions.add(e[1:]) #add extension, and omit the .

        for lang in languages.keys():
            for e in list(used_extensions):
                if e in languages[lang]['extensions']:
                    if languages[lang]['type'] == 'backend':
                        self.backend_languages.append(lang)
                    elif languages[lang]['type'] == 'frontend':
                        self.frontend_languages.append(lang)

        #remove duplicates
        self.backend_languages = list(set(self.backend_languages))
        self.frontend_languages = list(set(self.frontend_languages))

    def get_webserver(self):
        if 'server' in self.url.headers:
            return self.url.headers['server']
        else:
            return None
