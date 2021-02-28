import argparse
import sys
from datetime import date
import subprocess


CURRENT_YEAR = str(date.today().year)

FIRST_LINE = "# SPDX-License-Identifier: GPL-2.0-only\n"
SECOND_LINE = "# Copyright (c) 2019-" + CURRENT_YEAR + " NITK Surathkal\n"
HEADER_EOL = "\n"


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)

    changed_files = []

    process_files(args, changed_files)

    if changed_files:
        print("Some sources were modified by the hook {} ".format(changed_files))
        print("Now aborting the commit.")
        print(
            'You should check the changes made. Then simply "git add --update ." and re-commit'
        )
        print("")
        return 1
    return 0


def process_files(args, changed_files):

    files_to_be_committed = subprocess.run(
        ["git", "status", "--porcelain"], stdout=subprocess.PIPE
    )
    files_to_be_committed = files_to_be_committed.stdout.decode("utf-8")
    files_to_be_committed = files_to_be_committed.split("\n")[:-1]

    commit_files = []
    for file_path in files_to_be_committed:
        commit_files.append(file_path[3:])

    for src_filepath in args.filenames:
        with open(src_filepath) as src_file:
            src_file_content = src_file.readlines()

        if src_filepath not in commit_files:
            res = subprocess.run(
                ["git", "log", "-1", '--pretty="format:%ci', src_filepath],
                stdout=subprocess.PIPE,
            )
            last_modified_year = res.stdout.decode("utf-8")[8:12]
            # If the file has not been modified this year skip it.
            if last_modified_year != CURRENT_YEAR:
                continue

        if len(src_file_content) >= 2 and src_file_content[0] == FIRST_LINE:
            # License header found. Check the year
            if src_file_content[1] != SECOND_LINE:
                if src_file_content[1].startswith("# Copyright"):
                    # Hopefully only year needs to be changed
                    src_file_content[1] = SECOND_LINE
                else:
                    # Second copyright line missing
                    src_file_content = (
                        src_file_content[:1]
                        + [SECOND_LINE + HEADER_EOL]
                        + src_file_content[1:]
                    )
                with open(src_filepath, "w") as src_file:
                    src_file.write("".join(src_file_content))
                changed_files.append(src_filepath)
        else:
            # License header not found.
            src_file_content = (
                [FIRST_LINE] + [SECOND_LINE + HEADER_EOL] + src_file_content
            )
            with open(src_filepath, "w") as src_file:
                src_file.write("".join(src_file_content))
            changed_files.append(src_filepath)
