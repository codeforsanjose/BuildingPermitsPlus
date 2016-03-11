import csv
import logging
import collections
import os
import requests

HEADERS_LINES = '''\
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://www.sjpermits.org
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36
Content-Type: application/x-www-form-urlencoded
Referer: http://www.sjpermits.org/permits/general/permitquery1.asp
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.8'''


def makeSession():
    session = requests.Session()

    for line in HEADERS_LINES.splitlines():
        k, v = line.split(':', 1)
        session.headers[k.strip()] = v.strip()
    return session


Action = collections.namedtuple('Action', 'method url data')


class DetailsAction(Action):
    URL = 'http://www.sjpermits.org/permits/general/generalfolder.asp'

    def __new__(cls, rsn):
        return super(DetailsAction, cls).__new__(
            cls, 'POST', cls.URL, {'folderrsn': rsn})


class Script(object):
    preamble = (
        Action('GET',
               'http://www.sjpermits.org/permits/general/permitquery.asp',
               None),
        Action('POST',
               'http://www.sjpermits.org/permits/general/permitquery1.asp',
               # this is garbage just to advance to the right spot in
               # the cookie sequence
               {'permitnum': ' 2000-072012-000', 'B1': 'Search'}),
    )

    def __init__(self, saveDir):
        self.saveDir = saveDir
        self.session = makeSession()

    def scrapeAction(self, action):
        logging.info('%r', action)
        response = self.session.request(action.method, action.url, action.data)
        if response.status_code != 200:
            raise ValueError("FAILED: %r %r" % (action, response,))
        return response

    def run(self, folderrsns):
        for action in self.preamble:
            self.scrapeAction(action)

        for folderrsn in folderrsns:
            action = DetailsAction(folderrsn)
            self.save(folderrsn, self.scrapeAction(action))

    def save(self, rsn, response):
        with open(os.path.join(self.saveDir, rsn) + '.html', 'w') as f:
            f.write(response.content)


def rsnsFromCSV(csvpath):
    with open(csvpath) as f:
        for line in csv.DictReader(f, delimiter='\t'):
            rsn = line['FOLDERRSN']
            if not (rsn and rsn.isdigit()):
                logging.info('DROPPING RSN %r', rsn)
                continue
            yield rsn


def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('csv')
    p.add_argument('save_dir')

    args = p.parse_args()
    logging.basicConfig(level=logging.INFO)

    Script(args.save_dir).run(rsnsFromCSV(args.csv))


if __name__ == '__main__':
    main()
