import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from pattern.web import URL, DOM, plaintext
from pattern.web import NODE, TEXT, COMMENT, ELEMENT, DOCUMENT
from pattern.web import abs, extension
import re
from collections import Counter
from w3techs import W3Techs
from whois import whois
from urlparse import urlparse
import models


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
            'Apache Click',
            'Apache OFBiz',
            'Apache Shale',
            'Apache Sling',
            'Apache Struts 2',
            'Apache Tapestry',
            'Apache Wicket',
            'AppFuse',
            'Brutos Framework',
            'Crux',
            'Eclipse RAP',
            'FormEngine',
            'Grails',
            'Google Web Toolkit',
            'Hamlets',
            'ItsNat',
            'JavaServer Faces (Mojarra)',
            'JBoss Seam',
            'Jspx-bay',
            'JVx',
            'OpenLaszlo',
            'OpenXava',
            'Oracle ADF',
            'Play',
            'RIFE',
            'Spark',
            'Spring',
            'Stripes',
            'ThinWire',
            'Vaadin',
            'VRaptor',
            'Wavemaker',
            'WebObjects',
            'WebWork',
            'Ze Framework',
            'ZK',
            'ztemplates',
        ],
    },
    'JavaScript' : {
        'type': 'frontend',
        'extensions' : ['js'],
        'frameworks' : [
            'AngularJS',
            'KnockoutJS',
            'Backbone.js',
            'Ember.js',
        ],
    },
    'Perl' : {
        'type': 'backend',
        'extensions' : ['pl'],
        'frameworks' : [
            'Catalyst',
            'Dancer',
            'Mason',
            'Maypole',
            'Mojolicious',
        ],
    },
    'PHP' : {
        'type': 'backend',
        'extensions' : ['php', 'php4', 'php5', 'phtml'],
        'frameworks' : [
            'Agavi',
            'Aiki Framework',
            'AppFlower',
            'Ayoola Framework',
            'CakePHP',
            'Cgiapp',
            'ClanCatsFramework',
            'CodeIgniter',
            'Drupal',
            'Fat-Free',
            'FuelPHP',
            'Hazaar MVC',
            'Joomla',
            'Kajona',
            'Laravel',
            'Lithium',
            'Nette Framework',
            'Phalcon',
            'PHPixie',
            'PRADO',
            'Qcodo',
            'Seagull',
            'Silex',
            'Symfony',
            'TYPO3 Flow',
            'Xyster Framework',
            'Yii',
            'Zend Framework',
        ],
    },
    'Python' : {
        'type': 'backend',
        'extensions' : ['py'],
        'frameworks' : [
            'BlueBream',
            'Bottle',
            'CherryPy',
            'CubicWeb',
            'Django',
            'Flask',
            'Grok',
            'Nagare',
            'Pyjamas',
            'Pylons',
            'Pyramid',
            'TACTIC',
            'Tornado',
            'TurboGears',
            'web2py',
            'Webware',
            'Zope 2'
        ],
    },
    'Ruby' : {
        'type': 'backend',
        'extensions' : ['rb', 'rhtml'],
        'frameworks' : [
            'Camping',
            'Padrino',
            'Ruby on Rails',
            'Sinatra',
            'Merb',
            'PureMVC',
            'Volt'
        ],
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
        self.all_js = []
        self.all_css = []
        self.local_links = []
        self.logo = None
        self.css_images = []
        self.frameworks = {}

        self.name = None #name of the website

        self.domain = self.url.domain
        self.w3 = None #W3Techs(self.domain)
        #self.w3.analyze()



    def predict_name(self):

        title_words = []
        #domain + title
        title1 = plaintext(str(self.dom('title')[0]))
        title1 = re.sub("[\W\d]+", " ", title1.strip())
        title_words.extend(title1.split(' '))

        title2 = self.url.domain
        #title_words.extend(title2.split('.'))
        #open another link other than the index

        limit = 5
        i = 0
        if self.local_links:
            for u in self.local_links:

                if i >= limit:
                    break
                try:
                    url = URL(u)
                    if url.path != self.url.path:
                        dom2 = DOM(url.download(cached=True, unicode=True))
                        title2 = plaintext(str(dom2('title')[0]))

                        title2 = re.sub("[\W\d]+", " ", title2.strip())
                        title_words.extend(title2.split(' '))

                        i += 1
                except:
                    pass

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

        if self.w3 and 'Server-side Programming Language' in self.w3.data:
            self.backend_languages.append(self.w3.data['Server-side Programming Language'])

        #remove duplicates
        self.backend_languages = list(set(self.backend_languages))

        
    def predict_frontend(self):
        used_extensions = set()
        #check urls
        #if local and ends with one of the extentions, predict language
        for link in self.dom.by_tag("link"):
            link = link.attrs.get("href","")
            link = abs(link, base=self.url.redirect or self.url.string)
            
            e = extension(link)
            if e:
                used_extensions.add(e[1:]) #add extension, and omit the .
                if 'css' in e:
                    if self.url.domain in link: 
                        self.css.append(link)
                    else:
                        self.all_css.append(link)

        #forms
        for link in self.dom.by_tag("script"):
            link = link.attrs.get("src","")

            if link.startswith('.') or link.startswith('/'):
                link = abs(link, base=self.url.redirect or self.url.string)
            
            e = extension(link)
            if e:
                used_extensions.add(e[1:]) #add extension, and omit the .
                if 'js' in e:
                    if self.url.domain in link: 
                        self.js.append(link)
                    self.all_js.append(link)



        for lang in languages.keys():
            for e in list(used_extensions):
                if e in languages[lang]['extensions']:
                    if languages[lang]['type'] == 'frontend':
                        self.frontend_languages.append(lang)

        if self.w3 and 'Client-side Programming Language' in self.w3.data:
            self.frontend_languages.append(self.w3.data['Client-side Programming Language'])

        #remove duplicates
        self.frontend_languages = list(set(self.frontend_languages))


    def find_logo_in_css(self, css, url=None):

        if not url:
            url = self.url

        import tinycss
        parser = tinycss.make_parser('page3')
        stylesheet = parser.parse_stylesheet(css)
        for rule in stylesheet.rules:
                if type(rule) is not tinycss.css21.RuleSet:
                    continue
                selector = rule.selector.as_css().lower()
                #if 'logo' in selector.as_css():
                for dec in rule.declarations:
                    if 'background' in dec.name:
                        img_url = None
                        for token in  dec.value:
                            if token.type == 'URI':
                                img_url = token.value

                        if not img_url:
                            continue

                        link = abs(img_url, base=url.redirect or url.string)
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
            src = img.attrs.get('src', '').lower()
            img_id = img.attrs.get('id', '').lower()
            img_class = img.attrs.get('class', '').lower()
            if 'logo' in src or name_lower in src.lower() \
                or 'logo' in img_id or 'logo' in img_class:
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

        if self.logo:
            return

        #if still not found, they are mostly using CDN with diff domain
        #check all other css files
        for css_url in self.all_css:
            url = URL(css_url)
            content = url.download(cached=True)
            self.find_logo_in_css(content, url)



    def predict_frameworks(self):
        # after we did get the languages used
        #lets do the trivial thing.. ... ... ... 
        # look if the any of the frameworks in the list are in the html page :D

        #contents of html
        html_content = str(self.dom).lower()
        js_content = ""
        for js in self.all_js:
            content = URL(js).download()
            js_content += str(content)

        js_content = js_content.lower()


        for lang in self.backend_languages + self.frontend_languages:
            for framework in languages[lang]['frameworks']:
                frm_lower = framework.lower()
                #also check js content! Sometimes they are written in licenses..etc

                if languages[lang]['type'] == 'backend':
                    if frm_lower in html_content:
                        if lang not in self.frameworks:
                            self.frameworks[lang] = []
                        self.frameworks[lang].append(framework)
                elif languages[lang]['type'] == 'frontend':
                    if frm_lower in js_content: 
                        if lang not in self.frameworks:
                            self.frameworks[lang] = []
                        self.frameworks[lang].append(framework)
                    
                        


    def get_webserver(self):
        if 'server' in self.url.headers:
            server = self.url.headers['server']
            if '/' in server:
                return server.split('/', 1)[0]
            return
        else:
            return None

    def predict_location(self):
        o = urlparse(self.url.__str__())
        w = whois(o.hostname)
        # names of fields which might got a country name
        country_fields = ['countrycode:', 'registrant country:']
        country_name = None
        # names of fields which might got a city name
        city_fields = ['address:', 'registrant city:']
        city_names = []
        for line in w.text.lower().split('\n'):
            for field_name in country_fields:
                if field_name in line:
                    try:
                        country_name = line.split(field_name, 1)[1].strip()
                    except KeyError:
                        continue
            for field_name in city_fields:
                if field_name in line:
                    try:
                        city_names.append(line.split(field_name, 1)[1].strip())
                    except KeyError:
                        continue
        for city_name in city_names:
            if country_name:
                cities = models.Location.objects.filter(city=city_name, country=country_name).order_by('-population')
            else:
                cities = models.Location.objects.filter(city=city_name).order_by('-population')
            if cities.exists():
                return cities[0]
        return None