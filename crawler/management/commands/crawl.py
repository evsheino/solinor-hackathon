from django.core.management.base import BaseCommand, CommandError
import sys
from crawler.models import Site


class Command(BaseCommand):
    args = '<site_url site_url ...>'
    help = 'Crawls through the specified URLs'

    def handle(self, *args, **options):
        for url in args:
            self.stdout.write('Crawling site "%s"...' % url)
            s = Site()
            try:
                s.crawl(url)
            except:
                self.stdout.write('Failed to crawl site "%s": %s' % (url, sys.exc_info()[0]))
                continue
            self.stdout.write('Finished crawling site "%s"' % url)
            s.save()

