#!/usr/bin/env python

import sys
import argparse
import datetime
import subprocess
from subprocess import check_output

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--hours',
					help='A duration of branch inactivity in a hours '+
						 '(means the period from the time of last commit in branch to now).',
					default=24*14, # 14 days
					type=int,
					required=False)

args = parser.parse_args()
colors = {
	'yellow': '\033[93m',
	'red': '\033[91m',
	'reset': '\033[0m'
}

def get_merged_branches():
	try:
		branches_output = check_output(
			'git branch --remote --merged | grep -iP "(?:/[A-Z]{3}-\d+|[A-Z]{3}-\d+$)"',
			stderr=subprocess.STDOUT,
			shell=True
		).strip()		
	except subprocess.CalledProcessError as e:
		print e.output
		branches_output = ''

	branches = []
	for branch in branches_output.split('\n'):
		branch_name = branch.strip()
		if branch_name != '':
			branches.append(branch)
	
	return branches

def get_dead_branches(branches):
	dead_branches = []
	now = datetime.datetime.now()
	expiration_time = datetime.timedelta(hours=(args.hours))
	for branch in branches:
		branch_info = check_output(
			'git show -s --format="%ct####%cn####%s####%cr####%cd" '+branch,
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

	return sorted(dead_branches, key = lambda branch: (branch['commit_timestamp']))

def show_dead_branches(branches):
	msg = '\n'.join(['{colors[yellow]}Branch: {branch[branch_name]}{colors[reset]}',
					 'Last commit: \t{branch[commit_relative_date]},  {branch[commit_date]}',
					 'Committer: \t{branch[committer]}',
					 'Subject: \t{branch[subject]}']) + '\n'

	for branch_info in branches:
		print (msg.format(colors=colors, branch=branch_info))

def kill_branches(branches):
	for branch in branches:
		print 'removing branch "{}"'.format(branch)
		print 'remove remote branch'
		run_shell_command('git push origin --delete '+ branch)
		print 'remove local branch'
		run_shell_command('git branch -d '+ branch)

	run_shell_command('git fetch --all --prune')

def run_shell_command(cmd):
	try:
		print check_output(cmd, stderr=subprocess.STDOUT, shell=True)
	except subprocess.CalledProcessError as e:
		print e.output

def main():
	retval = 0
	dead_branches = get_dead_branches(get_merged_branches())

	if len(dead_branches) > 0:
		show_dead_branches(dead_branches)
		answer = raw_input('{red}Are you sure you want to remove this {amount} branches (y/yes)?{reset}\n'
			.format(
				red=colors['red'],
				amount=len(dead_branches),
				reset=colors['reset']
			))

		branch_names = [branch_info['branch_name'] for branch_info in dead_branches]
		branch_names = [name.replace('origin/', '').strip() for name in branch_names]

		if (answer.lower() == 'y' or answer.lower() == 'yes'):
			# ask second time to confirm
			answer = raw_input('Type "Yes" to continue removing branches ({amount})\n'
					   .format(amount=len(branch_names)))

			if (answer == 'Yes'):
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
	main()