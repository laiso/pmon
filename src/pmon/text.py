def extract_diff(content: str) -> str:
    start =content.find("```diff")
    end = content.rfind("```")
    if start == -1 or end == -1:
        return ""
    return content[start + 7:end]
