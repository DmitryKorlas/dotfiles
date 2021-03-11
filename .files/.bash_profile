# required for tmux sessions init. see https://unix.stackexchange.com/questions/320465/new-tmux-sessions-do-not-source-bashrc-file/541352
# source "$HOME/.bashrc"
# does not work unfortunately

# Load ~/.extra, ~/.bash_prompt, ~/.exports, ~/.aliases and ~/.functions
# ~/.extra can be used for settings you don’t want to commit
for file in ~/.{bashrc,extra,bash_prompt,exports,aliases,functions}; do
	[ -r "$file" ] && source "$file"
done
unset file
