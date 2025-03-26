

def strip_whitespace(text):
    stripped=[line.strip() for line in text.split("\n")]
    return "\n".join(stripped)