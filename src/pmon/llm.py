import mimetypes
import os

import openai

from .text import extract_diff


def create_patch(files, requirement, model_name="gpt-3.5-turbo"):
    code = ""
    for path in files:
        with open(path, 'r') as file:
            content = file.read()
            code += f"```{path}" + "\n" + content + "\n```\n"
    prompt = [
        {"role": "system", "content": "You are the assistant to write source code. You generate patches according to requirement from user." +
    "The output should be a single markdown code snippet formatted:" +
"""```diff
--- path/to/file.orig
+++ path/to/file
@@ -1,5 +1,5 @@
 def main():
-    print("Hello, World!")
+    print("Hello, New World!")
 
 if __name__ == "__main__":
     main()
```"""},
        {"role": "user", "content": f"""Code: 
{code}
Requirement: {requirement}

Patch:"""}
    ]
    response = openai.ChatCompletion.create(model=model_name, temperature=0.0, stream=True, messages=prompt)

    collected_messages = []
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']
        print(chunk_message.get('content', ''), end="")
        collected_messages.append(chunk_message)

    full_reply_content = ''.join([m.get('content', '') for m in collected_messages])
    return extract_diff(full_reply_content)


def recursive_create_patch(path, requirement, model_name="gpt-3.5-turbo") -> str:
    paths = []
    if os.path.isfile(path):
        paths.append(path)
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                mimetype, _ = mimetypes.guess_type(file)
                if not mimetype:
                    continue
                file_path = os.path.join(root, file)
                paths.append(file_path)
    return create_patch(paths, requirement, model_name)
