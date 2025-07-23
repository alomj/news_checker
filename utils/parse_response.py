from typing import List
import re
from utils.basic_cleanup import basic_cleanup


def parse_response(dictionary: dict) -> List[str]:
    content = dictionary['choices'][0]['message']['content']
    lines = content.strip().split("\n")
    return [
        basic_cleanup(re.sub(r"^\s*\d+\s*[.):\-]*\s*", "", line)) for line in lines if line.strip()
    ]
