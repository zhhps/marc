#!/bin/env python
# -*- coding: utf-8 -*-

import argparse
import csv
import xml.etree.ElementTree as ET

def join_tag(tags):
    return ''.join(value if value != ' ' else '_' for value in tags.values())

def write_file(xml_name, set_field, output):
    tree = ET.parse(xml_name)
    root = tree.getroot()
    info = dict.fromkeys(set_field, '')
    last_tag = None
    with open(output, 'w', encoding='utf_8_sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list(set_field))
        for elem in root.iter():
            tag = elem.tag.split('}')[1]
            attrib = join_tag(elem.attrib)
            if tag == 'controlfield':
                info[attrib] = elem.text
            elif tag == 'datafield':
                last_tag = attrib
            elif tag == 'subfield':
                attrib = last_tag + attrib
                info[attrib] += (';' if info[attrib] else '') + elem.text
            elif tag == 'leader' and last_tag:
                writer.writerow(info.values())
                info = dict.fromkeys(list(set_field), '')

        writer.writerow(info.values())

def parse_marc(xml_name):
    tree = ET.parse(xml_name)
    root = tree.getroot()
    record_count = 0
    controlfield_count = 0
    datafield_count = 0
    subfield_count = 0
    fields = set()
    last_tag = ''

    for elem in root.iter():
        tag = elem.tag.split('}')
        if len(tag) < 2:
            print("Unknown tag", elem.tag)
            continue

        attrib = join_tag(elem.attrib)
        if tag[1] == 'controlfield':
            controlfield_count += 1
            fields.add(attrib)
        elif tag[1] == 'datafield':
            last_tag = attrib
        elif tag[1] == 'subfield':
            subfield_count += 1
            fields.add(last_tag + attrib)
        elif tag[1] == 'record':
            record_count += 1
        elif tag[1] != 'collection' and tag[1] != 'leader':
            print("********", tag[1])

    print("record_count =", record_count, "controlfield_count =", controlfield_count, "subfield_count =", subfield_count)
    return fields

def main(args):
    fields = parse_marc(args.xml)
    write_file(args.xml, sorted(fields), args.csv)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MARC xml to csv')
    parser.add_argument('--xml', help='xml file path')
    parser.add_argument('--csv', help='output csv name')
    args = parser.parse_args()
    main(args)
