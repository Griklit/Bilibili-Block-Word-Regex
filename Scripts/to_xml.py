import csv
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Iterable

CSV_DIR = Path(__file__).parent.parent / 'Regex'
XML_DIR = Path(__file__).parent.parent / 'Regex-XML'


def xml_escape(s: str) -> str:
    """
    XML字符串转义
    https://en.wikipedia.org/wiki/XML#Escaping
    """
    return (
        s
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&apos;')
    )


@dataclass
class Rule:
    regex: str
    remarks: str | None


def load_rule(csv_file: Path) -> Generator[Rule, None, None]:
    with open(csv_file, newline='', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter='\t')
        for row in csv_reader:
            row: dict
            yield Rule(row['正则'], row['备注'])


def build_xml_file(rules: Iterable[Rule], xml_file_path: Path):
    xml_output = ['<filters>']
    for rule in rules:
        xml_output.append(f'    <item enabled="true">r={xml_escape(rule.regex)}</item> <!-- {rule.remarks} -->')
    xml_output.append('</filters>')
    with open(xml_file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(xml_output))


def build():
    for csv_file in CSV_DIR.glob('*.csv'):
        rules = load_rule(csv_file)
        xml_file = XML_DIR / f'{csv_file.stem}.xml'
        build_xml_file(rules, xml_file)


if __name__ == '__main__':
    build()
