#!/bin/bash

cd "$(dirname "$0")"

#git pull

function resetDotfiles() {
	rsync --exclude ".DS_Store" -av ./.files/ ~
}

if [ "$1" == "--force" -o "$1" == "-f" ]; then
	resetDotfiles
else
	read -p "Existing dot files in Your home directory will be overriten. Continue? (y/n) " -n 1
	echo
	if [[ $REPLY =~ ^[Yy]$ ]]; then
		resetDotfiles
	fi
fi
unset resetDotfiles

# renew env
source ~/.bash_profile