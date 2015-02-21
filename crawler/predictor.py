import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from pattern.web import abs, extension
import re
from collections import Counter

languages = {
    'ASP.NET' : {
        'type': 'backend',
        'extensions' : ['asp', 'aspx', 'axd', 'asx', 'asmx', 'ashx', 'axd', 'asx', 'asmx', 'ashx'],
        'frameworks' : [
            'ASP.NET MVC Framework',
            'Base One Foundation Component Library',
            'Component-based Scalable Logical Architecture',
            'MonoRail',
            'OpenRasta',
        ]
    },
    'CSS' : {
        'type': 'frontend',
        'extensions' : ['css'],
        'frameworks' : [],
    },
    'Coldfusion' : {
        'type': 'backend',
        'extensions' : ['cfm'],
        'frameworks' : ['CFWheels', 'ColdBox Platform', 'ColdSpring', 'Fusebox', 'Mach-II', 'Model-Glue'],
    },
    'Erlang' : {
        'type': 'backend',
        'extensions' : ['yaws'],
        'frameworks' : [],
    },
    'Flash' : {
        'type': 'frontend',
        'extensions' : ['swf'],
        'frameworks' : [],
    },
    'HTML' : {
        'type': 'frontend',
        'extensions' : ['html', 'htm', 'xhtml', 'jhtml'],
        'frameworks' : [],
    },
    'Java' : {
        'type': 'backend',
        'extensions' : ['jsp', 'jspx', 'wss', 'do', 'action'],
        'frameworks' : [
            'Apache Click'
            'Apache OFBiz'
            'Apache Shale'
            'Apache Sling'
            'Apache Struts 2'
            'Apache Tapestry'
            'Apache Wicket'
            'AppFuse'
            'Brutos Framework'
            'Crux'
            'Eclipse RAP'
            'FormEngine'
            'Grails'
            'Google Web Toolkit'
            'Hamlets'
            'ItsNat'
            'JavaServer Faces (Mojarra)'
            'JBoss Seam'
            'Jspx-bay'
            'JVx'
            'OpenLaszlo'
            'OpenXava'
            'Oracle ADF'
            'Play'
            'RIFE'
            'Spark'
            'Spring'
            'Stripes'
            'ThinWire'
            'Vaadin'
            'VRaptor'
            'Wavemaker'
            'WebObjects'
            'WebWork'
            'Ze Framework'
            'ZK'
            'ztemplates',
        ],
    },
    'JavaScript' : {
        'type': 'frontend',
        'extensions' : ['js'],
        'frameworks' : [],
    },
    'Perl' : {
        'type': 'backend',
        'extensions' : ['pl'],
        'frameworks' : [],
    },
    'PHP' : {
        'type': 'backend',
        'extensions' : ['php', 'php4', 'php5', 'phtml'],
        'frameworks' : [],
    },
    'Python' : {
        'type': 'backend',
        'extensions' : ['py'],
        'frameworks' : [],
    },
    'Ruby' : {
        'type': 'backend',
        'extensions' : ['rb', 'rhtml'],
        'frameworks' : [],
    },
    'XML' : {
        'type': 'frontend',
        'extensions' : ['xml', 'rss', 'svg'],
        'frameworks' : [],
    },
    'C++' : {
        'type': 'backend',
        'extensions' : ['c', 'cgi', 'dll'],
        'frameworks' : ['Saetta Web Server', 'CppCMS', 'Poco', 'Tntnet', 'Wt'],
    },
}


class Predictor():

    def __init__(self, url, dom):
        """
        :type url: pattern.web.URL
        :type dom: pattern.web.DOM
        """

        self.url = url
        self.dom = dom

        self.backend_languages = []
        self.frontend_languages = []

        self.css = [] #list of css files
        self.js = [] #list of js files
        self.local_links = []
        self.logo = None
        self.css_images = []

        self.name = None #name of the website


    def predict_name(self):

        title_words = []
        #domain + title
        title1 = plaintext(str(self.dom('title')[0]))
        title1 = re.sub("[\W\d]+", " ", title1.strip())
        title_words.extend(title1.split(' '))

        title2 = self.url.domain
        #open another link other than the index

        limit = 5
        i = 0
        if self.local_links:
            for u in self.local_links:

                if i >= limit:
                    break

                url = URL(u)
                if url.path != self.url.path:
                    dom2 = DOM(url.download(cached=True, unicode=True))
                    title2 = plaintext(str(dom2('title')[0]))

                    title2 = re.sub("[\W\d]+", " ", title2.strip())
                    title_words.extend(title2.split(' '))

                    i += 1

        #i am sleep, I dont know what am doing, 
        #get the name of the company from the most repeated word in titles
        self.name = Counter(title_words).most_common(1)[0][0]
        


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
                else:
                    self.local_links.append(link)

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

        #remove duplicates
        self.backend_languages = list(set(self.backend_languages))
        
    def predict_frontend(self):
        used_extensions = set()
        #check urls
        #if local and ends with one of the extentions, predict language
        for link in self.dom.by_tag("link"):
            link = link.attrs.get("href","")
            link = abs(link, base=self.url.redirect or self.url.string)
            if self.url.domain in link: 
                e = extension(link)
                if e:
                    used_extensions.add(e[1:]) #add extension, and omit the .
                    if 'css' in e:
                        self.css.append(link)

        #forms
        for link in self.dom.by_tag("script"):
            link = link.attrs.get("src","")
            link = abs(link, base=self.url.redirect or self.url.string)
            if self.url.domain in link: 
                e = extension(link)
                if e:
                    used_extensions.add(e[1:]) #add extension, and omit the .
                    if 'js' in e:
                        self.js.append(link)

        for lang in languages.keys():
            for e in list(used_extensions):
                if e in languages[lang]['extensions']:
                    if languages[lang]['type'] == 'frontend':
                        self.frontend_languages.append(lang)

        #remove duplicates
        self.frontend_languages = list(set(self.frontend_languages))


    def find_logo_in_css(self, css):
        import tinycss
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet(css)
        for rule in stylesheet.rules:
                if type(rule) is not tinycss.css21.RuleSet:
                    continue
                selector = str(rule.selector).lower()
                #if 'logo' in selector.as_css():
                for dec in rule.declarations:
                    if 'background' in dec.name:
                        img_url = None
                        for token in  dec.value:
                            if token.type == 'URI':
                                img_url = token.value

                        if not img_url:
                            continue

                        link = abs(img_url, base=self.url.redirect or self.url.string)
                        if link: # and self.url.domain in link:
                            link = link.lower()
                            if '?' in link:
                                link = link[:link.find('?')]

                            e = extension(link)

                            if e and e[1:] in ['png', 'jpg', 'jpeg']: #if has extension and it is an image
                                #does any have logo? 
                                if 'logo' in link:
                                    self.logo = link
                                    return
                                elif 'logo' in selector:
                                    self.logo = link
                                    return
                                if 'brand' in link:
                                    self.logo = link
                                    return
                                elif 'brand' in selector:
                                    self.logo = link
                                    return
                                #not in the full url! because domain might be there
                                else:
                                    self.css_images.append((img_url, link)) #0 base, 1 full

    def predict_logo(self):
        '''
        get the logo of a website from css
        '''
        for css_url in self.css:
            url = URL(css_url)
            content = url.download(cached=True)
            self.find_logo_in_css(content)

        if self.logo:
            return
        #:\ STILL NOT FOUND!!!
        #maybe they are hiding it inside html style!

        for style in self.dom('style'):
            content = plaintext(style.content)
            self.find_logo_in_css(content)            

        if self.logo:
            return

        #if not found yet!! they are doing it using inline-css -.- WHY?
        for div in self.dom('div'):
            style = div.attrs.get('style', "")

            content = 'div { ' + str(style) + ' }'
            self.find_logo_in_css(content)                    

        if self.logo:
            return

        name_lower = self.name.lower()
        #get images
        for img in self.dom('img'):
            src = img.attrs.get('src', '')
            if 'logo' in src.lower() or name_lower in src.lower():
                self.logo =  abs(src, base=self.url.redirect or self.url.string)
                return

        if self.logo:
            return

        #logo is not found yet :O!!
        #does any of the images have company name?
        for img_url, full_url in self.css_images:
            if name_lower in img_url:
                self.logo = full_url
                return


    def get_webserver(self):
        if 'server' in self.url.headers:
            return self.url.headers['server']
        else:
            return None
