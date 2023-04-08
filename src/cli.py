import os
import pathlib
import logging
import sys
from datetime import datetime
import subprocess
import argparse


from llm import recursive_create_patch

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', type=str, help='Path to the file')
    parser.add_argument('--requirement', '-r', type=str)
    parser.add_argument('--model', '-m', type=str, default='gpt-3.5-turbo', help='OpenAI model (default: gpt-3.5-turbo)')
    parser.add_argument('--dir', '-d', type=str, default='out/patches', help='Output directory (default: out)')
    parser.add_argument('--retry', type=int, default=3, help='Maximum retry count (default: 3)')
    args = parser.parse_args()

    current_directory = os.getcwd()
    path = args.path
    model_name = args.model

    patch_dir = os.path.realpath(os.path.join(current_directory, args.dir))
    pathlib.Path(patch_dir).mkdir(parents=True, exist_ok=True)

    requirement = args.requirement
    if not requirement:
        requirement = input('How do you want to change the code? (e.g. "Add test case for generate()"):\n')

    retry_count = 0
    max_retry_count: int = args.retry

    while retry_count < max_retry_count:
        try:
            patch_content = recursive_create_patch(path, requirement, model_name)
            patch_path = os.path.join(patch_dir, f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.patch")
            with open(patch_path, "a") as tmpfile:
                tmpfile.write(patch_content)
            print("Do you want to apply this patch? " + patch_path)
            user_input = input(f"Yes or No or Retry or Quit (Y/n/r/q): ") or 'y'
            if user_input.lower() == 'y':
                cmd = f"patch --no-backup-if-mismatch < {patch_path}"
                subprocess.run(cmd, shell=True, check=True)
                print("The patch has been applied.")
                requirement = input('What\'s next?:\n')
            elif user_input.lower() == 'r':
                print("Patch not applied.")
            elif user_input.lower() == 'n':
                requirement = input('Please enter a new requirement:\n')
                continue
            elif user_input.lower() == 'q':
                sys.exit(0)

            retry_count = 0
        except IndexError as e:
            print("Invalid Response：")
            print(e)
            retry_count += 1
        except subprocess.CalledProcessError as e:
            print("Invalid Patch：" + "".join(e.args[-1]))
            retry_count += 1