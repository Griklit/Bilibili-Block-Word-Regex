import csv
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
    type: str
    regex: str
    remarks: str | None

    def to_item(self):
        s = f'<item enabled="true">r={xml_escape(self.regex)}</item>'
        if self.remarks is not None:
            s += f'<!-- {self.remarks} -->'
        return s


def load_rule(csv_file: Path) -> Generator[Rule, None, None]:
    type_ = csv_file.stem
    with open(csv_file, newline='', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter='\t')
        for row in csv_reader:
            row: dict
            yield Rule(type_, row['正则'], row['备注'])


def load_all_rule() -> Generator[Rule, None, None]:
    for csv_file in CSV_DIR.glob('*.csv'):
        yield from load_rule(csv_file)


def build_xml_file(rules: Iterable[Rule], xml_file_path: Path):
    last_type: str | None = None
    with open(xml_file_path, 'w', encoding='utf-8') as f:
        f.write('<filters>\n')
        for rule in rules:
            if rule.type != last_type:
                f.write(f'    <!-- {rule.type} -->\n')
                last_type = rule.type
            f.write(f'    {rule.to_item()}\n')
        f.write('</filters>')


def build():
    for csv_file in CSV_DIR.glob('*.csv'):
        build_xml_file(load_rule(csv_file), XML_DIR / f'{csv_file.stem}.xml')
    build_xml_file(load_all_rule(), XML_DIR / 'All.xml')


if __name__ == '__main__':
    build()
