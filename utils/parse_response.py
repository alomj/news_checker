from typing import List, Dict
import re
from utils.basic_cleanup import basic_cleanup
import json


def parse_response(dictionary: Dict) -> List[str]:
    content = dictionary['choices'][0]['message']['content']
    lines = content.strip().split("\n")
    return [
        basic_cleanup(re.sub(r"^\s*\d+\s*[.):\-]*\s*", "", line)) for line in lines if line.strip()
    ]


def parse_response_with_credibility(dictionary: Dict) -> List | None:
    content = dictionary['choices'][0]['message']['content']
    try:

        parsed = json.loads(content)
        if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
            return parsed
    except json.JSONDecodeError as e:
        raise ValueError(f'Wrong JSON format {e.msg}')
