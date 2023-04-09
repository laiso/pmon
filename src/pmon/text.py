PREFIX = "```diff\n"

def extract_diff(content: str) -> str:
    start =content.find(PREFIX)
    end = content.rfind("\n```")
    if start == -1 or end == -1:
        return ""
    diff = content[start + len(PREFIX):end]
    return diff
