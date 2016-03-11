import argparse
import glob
import logging
import lxml.html
import pprint


def project_information(path):
    doc = lxml.html.parse(path)

    tmpl = ('.//table[preceding-sibling::h3[contains(text(),'
            '"Project Information")]]//%s//text()')

    keys = doc.xpath(tmpl % 'th')
    values = doc.xpath(tmpl % 'td')

    if len(keys) != len(values):
        return None

    return dict(zip(keys, values))


def experiment(directory, show=False):
    bad = 0
    good = 0

    for path in glob.glob(directory):
        print path
        table = project_information(path)
        if not table:
            bad += 1
            continue
        good += 1
        if show:
            pprint.pprint(table)
    print 'bad: %s, good: %s (%f)' % (bad, good, bad / (good + bad))


def main():
    p = argparse.ArgumentParser()

    p.add_argument('directory')

    a = p.parse_args()
    logging.basicConfig(level=logging.INFO)

    experiment(a.directory)


main()
