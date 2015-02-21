from django.core.management.base import BaseCommand, CommandError
import sys
from crawler.models import Site


class Command(BaseCommand):
    args = '<site_url site_url ...>'
    help = 'Crawls through the specified URLs'

    def handle(self, *args, **options):
        for url in args:
            s = Site()
            try:
                s.crawl(url)
            except:
                self.stdout.write('Failed to crawl site "%s": %s' % (url, sys.exc_info()[0]))
                continue
            self.stdout.write('Crawled site "%s"' % url)
            s.save()

