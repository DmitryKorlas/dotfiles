#!/usr/bin/env python

import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import datetime
import subprocess
from subprocess import check_output

COLORS = {
    'yellow': '\033[93m',
    'red': '\033[91m',
    'reset': '\033[0m'
}


def get_merged_branches():
    try:
        branches_output = check_output(
            'git branch --remote --merged | grep -iP "[A-Z]{3}-\\d+"',
            stderr=subprocess.STDOUT,
            shell=True
        ).strip()
    except subprocess.CalledProcessError as e:
        print e.output
        branches_output = ''

    branches = []
    for branch in branches_output.split('\n'):
        branch = branch.strip()
        if branch != '':
            branches.append(branch)

    return branches


def write_list_to_file(list_of_messages, filepath):
    with open(filepath, 'w') as output_file:
        for item in list_of_messages:
            output_file.write("%s\n" % item)


def get_branches_from_file(filepath):
    lines = []
    with open(filepath) as input_file:
        for line in input_file:
            line = line.strip()
            lines.append(line)

    return lines


def get_dead_branches(branches, hours):
    dead_branches = []
    now = datetime.datetime.now()
    expiration_time = datetime.timedelta(hours=hours)

    for branch in branches:
        branch_info = check_output(
            'git show -s --format="%ct####%cn####%s####%cr####%cd" ' + branch,
            shell=True
        ).strip().split('####')
        timestamp, committer, subject, commit_relative_date, commit_date = branch_info
        struct = {
            'branch_name': branch,
            'commit_timestamp': int(timestamp),
            'committer': committer,
            'subject': subject,
            'commit_date': commit_date,
            'commit_relative_date': commit_relative_date
        }
        branch_date = datetime.datetime.fromtimestamp(int(timestamp))
        diff = now - branch_date

        if diff > expiration_time:
            dead_branches.append(struct)

    return sorted(dead_branches, key=lambda branch: (branch['commit_timestamp']))


def show_dead_branches(branches):
    for formatted_entry in branches:
        print (formatted_entry)


def format_dead_branches(branches):
    msg = '\n'.join([
        '{colors[yellow]}Branch: {branch[branch_name]}{colors[reset]}',
        'Last commit: \t{branch[commit_relative_date]}, {branch[commit_date]}',
        'Committer: \t{branch[committer]}',
        'Subject: \t{branch[subject]}'
    ]) + '\n'

    output = []

    for branch_info in branches:
        log_entry = msg.format(colors=COLORS, branch=branch_info)
        output.append(log_entry)

    return output


def kill_branches(branches):
    for branch in branches:
        print 'removing branch "{}"'.format(branch)
        print 'remove remote branch'
        run_shell_command('git push origin --delete ' + branch)
        print 'remove local branch'
        run_shell_command('git branch -d ' + branch)

    run_shell_command('git fetch --all --prune')


def run_shell_command(cmd):
    try:
        print check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    except subprocess.CalledProcessError as e:
        print e.output


def strip_branch_name(branch_info):
    branch_name = branch_info['branch_name']
    return branch_name.replace('origin/', '').strip()


def strip_colors(message):
    for color in COLORS.values():
        message = message.replace(color, '')

    return message


def main(hours, file=None):
    retval = 0

    if file is None:
        branches = get_merged_branches()
    else:
        branches = get_branches_from_file(file)

    dead_branches = get_dead_branches(branches, hours)

    if len(dead_branches) > 0:
        formatted_entries = format_dead_branches(dead_branches)
        show_dead_branches(formatted_entries)

        answer = raw_input(
            '{red}Are you sure you want to remove this {amount} branches (y/yes)?{reset}\n'
            .format(
                red=COLORS['red'],
                amount=len(dead_branches),
                reset=COLORS['reset']
            ))

        branch_names = list(map(strip_branch_name, dead_branches))

        now = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

        log_brief_filename = 'killed-brief-{now}.txt'.format(now=now)
        log_detailed_filename = 'killed-detailed-{now}.txt'.format(now=now)

        write_list_to_file(branch_names, log_brief_filename)
        write_list_to_file(list(map(strip_colors, formatted_entries)), log_detailed_filename)

        print 'write log files "{file_brief}", "{file_detailed}"'.format(
            file_brief=log_brief_filename,
            file_detailed=log_detailed_filename
        )

        if answer.lower() == 'y' or answer.lower() == 'yes':
            # ask second time to confirm
            answer = raw_input(
                'Type "Yes" to continue removing branches ({amount})\n'
                .format(amount=len(branch_names))
            )

            if answer == 'Yes':
                kill_branches(branch_names)
            else:
                print 'skip'
                retval = 1
        else:
            retval = 1
    else:
        print 'There are no branches to remove'
    sys.exit(retval)


if __name__ == '__main__':
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--hours',
        help='A duration of branch inactivity in a hours ' +
             '(means the period from the time of last commit in branch to now).',
        default=24 * 14,  # 14 days
        type=int,
        required=False
    )
    parser.add_argument(
        '--file',
        help='A file to kill branches from',
        default=None,
        type=str,
        required=False
    )
    args = parser.parse_args()

    main(args.hours, file=args.file)
