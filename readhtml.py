from lxml import etree
import lxml.html
import os
import re
import logging

logger = logging.getLogger('readhtml')

filename = os.path.join(
    'assets',
    '20180309 OutdoorLightingChecklist at 1930.docx',
    '20180309OutdoorLightingChecklistat1930.docx.html',
)


def get_tables(tree):
    el_tables = tree.xpath(
        # '/html/body/table'
        '//table'
    )
    # get titles from TR
    for el_table in el_tables:
        imgs = el_table.xpath('tbody//img')
        if not imgs:
            continue
        el_trs = el_table.xpath('tbody/tr')
        str_trs = etree.tostring(el_table)
        res = re.search(r'Turret Tower \d', str_trs.decode())
        if res:
            title = el_trs[2].xpath('td//span')[1].text
        else:
            title = el_trs[1].xpath('td//span')[1].text

        # get images
        print(title)
        for img in imgs:
            print(img.attrib['src'])


def main():
    f = open(filename, 'r')
    # parser = etree.HTMLParser()
    # tree = etree.parse(f, parser)
    tree = lxml.html.parse(f)
    f.close()

    get_tables(tree)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
    )
    main()
