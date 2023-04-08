import os
import pathlib
import logging
import sys
from datetime import datetime
import subprocess
import argparse

from .llm import recursive_create_patch


def process_patch(path, requirement, model_name, patch_dir):
    patch_content = recursive_create_patch(path, requirement, model_name)
    patch_path = os.path.join(patch_dir, f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.patch")
    with open(patch_path, "w") as tmpfile:
        tmpfile.write(patch_content)
    print("Do you want to apply this patch? " + patch_path)
    user_input = input(f"Yes or No or Retry or Quit (Y/n/r/q): ") or 'y'
    if user_input.lower() == 'y':
        cmd = f"patch --no-backup-if-mismatch --ignore-whitespace < {patch_path}"
        subprocess.run(cmd, shell=True, check=True)
        print("The patch has been applied.")
        return input('What\'s next?:\n')
    elif user_input.lower() == 'r':
        print("Patch not applied.")
        return requirement
    elif user_input.lower() == 'n':
        return input('Please enter a new requirement:\n')
    elif user_input.lower() == 'q':
        sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="A CLI tool to generate and apply patches based on user requirements.")
    parser.add_argument('path', type=str, help='Path to the file')
    parser.add_argument('--requirement', '-r', type=str)
    parser.add_argument('--model', '-m', type=str, default='gpt-3.5-turbo', help='OpenAI model (default: gpt-3.5-turbo)')
    parser.add_argument('--out-dir', '-o', type=str, default='out/patches', help='Output directory (default: out)')
    parser.add_argument('--retry', type=int, default=3, help='Maximum retry count (default: 3)')
    args = parser.parse_args()

    current_directory = os.getcwd()
    path = args.path
    model_name = args.model

    patch_dir = os.path.realpath(os.path.join(current_directory, args.out_dir))
    pathlib.Path(patch_dir).mkdir(parents=True, exist_ok=True)

    requirement = args.requirement
    if not requirement:
        requirement = input('How do you want to change the code? (e.g. "Add test case for generate()"):\n')

    retry_count = 0
    max_retry_count: int = args.retry

    while retry_count <= max_retry_count:
        try:
            process_patch(path, requirement, model_name, patch_dir)
            retry_count = 0
        except IndexError as e:
            logging.error("Invalid Response：")
            retry_count += 1
        except subprocess.CalledProcessError as e:
            logging.error("Invalid Patch：" + "".join(e.args[-1]))
            retry_count += 1
