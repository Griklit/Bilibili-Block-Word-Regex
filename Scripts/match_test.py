import re
import json
import sys


def load_regex_patterns(regex_file):
    patterns = []
    with open(regex_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignore lines starting with '//'
            if line and not line.startswith('//'):
                patterns.append(line)
    compiled_patterns = [(re.compile(pattern), pattern) for pattern in patterns]
    return compiled_patterns


def find_matching_contents(json_file, regex_patterns):
    matching_contents = []
    with open(json_file, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            for obj in data:
                if 'content' in obj:
                    content = obj['content']
                    for pattern, regex_str in regex_patterns:
                        if pattern.search(content):
                            matching_contents.append((content, regex_str))
                            break
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}", file=sys.stderr)
    return matching_contents


if __name__ == "__main__":
    json_file = 'data.json'
    regex_file = 'regex_patterns.txt'

    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    if len(sys.argv) > 2:
        regex_file = sys.argv[2]

    regex_patterns = load_regex_patterns(regex_file)
    matching_contents = find_matching_contents(json_file, regex_patterns)

    # Output matching contents and corresponding regex patterns to a text file
    with open('matches.txt', 'w', encoding='utf-8') as output_file:
        for content, regex_str in matching_contents:
            output_file.write(f"{content:<256} {regex_str}\n")

    print(f"Number of matching contents: {len(matching_contents)}")
    print(f"Matching contents and corresponding regex patterns have been written to matches.txt")
