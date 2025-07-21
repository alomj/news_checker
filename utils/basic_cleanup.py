def basic_cleanup(text: str) -> str:
    return text.strip().replace('"', '').replace("'", '').replace('\\', '')
