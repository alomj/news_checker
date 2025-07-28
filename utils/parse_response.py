from typing import List, Dict
import re
from utils.basic_cleanup import basic_cleanup
import json


def parse_response(dictionary: Dict) -> List[str]:
    try:
        content = dictionary['choices'][0]['message']['content']
    except KeyError as e:
        raise ValueError(f"Missing key in OpenAI response: {e}")

    except IndexError as e:
        raise ValueError(f"Empty  array in OpenAI response {e}")

    except Exception as e:
        raise ValueError(f'Something went wrong {e}')

    try:
        lines = content.strip().split("\n")
        return [
            basic_cleanup(re.sub(r"^\s*\d+\s*[.):\-]*\s*", "", line))
            for line in lines if line.strip()
        ]
    except Exception as e:
        raise ValueError(f"Failed to parse lines from content: {e}")


def parse_response_with_credibility(dictionary: Dict) -> List | None:
    try:
        content = dictionary['choices'][0]['message']['content']
    except KeyError as e:
        raise ValueError(f"Missing key in OpenAI response: {e}")
    except IndexError as e:
        raise ValueError(f"Empty  array in OpenAI response {e}")

    if not content or not content.strip():
        raise ValueError("Empty content from OpenAI")

    try:
        parsed = json.loads(content)

        if isinstance(parsed, list) and all(isinstance(item, dict) for item in parsed):
            return parsed
        else:
            raise ValueError("Response is not a list of dictionaries")

    except json.JSONDecodeError as e:
        raise ValueError(f'Wrong JSON format {e.msg}')
