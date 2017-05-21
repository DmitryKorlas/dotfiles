#!/bin/bash

setup_brew_deps() {
	/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

	# Make sure Brew has permissions
	brew doctor


	# Bash 4
	# Note: don’t forget to add `/usr/local/bin/bash` to `/etc/shells` before running `chsh`.
	brew install bash

	brew install bash-completion


	# install cask to be able to install software distributed as binaries 
	brew tap caskroom/cask
	brew install homebrew/completions/brew-cask-completion


	brew install tmux


	brew tap homebrew/dupes

	# GNU core utilities (those that come with OS X are outdated)
	brew install coreutils
	brew install moreutils
	# GNU `find`, `locate`, `updatedb`, and `xargs`, `g`-prefixed
	brew install findutils
	# GNU `sed`, overwriting the built-in `sed`
	brew install gnu-sed --with-default-names

	# Install wget with IRI support
	brew install wget --with-iri

	#brew install vim --with-override-system-vi
	brew install homebrew/dupes/nano
	brew install homebrew/dupes/grep
	brew install homebrew/dupes/openssh

	brew install imagemagick --with-webp
	brew install tree
	brew install watch

	brew install ffmpeg --with-libvpx

	brew install dark-mode

	# node + npm
	brew install node

	# cask

	# browsers
	brew cask install sublime-text
	brew cask install google-chrome
	brew cask install chromium
	brew cask install firefox

	brew cask install dropbox
	brew cask install virtualbox

	# Remove outdated versions from the cellar.
	brew cleanup
}

setup_apt_deps() {
	sudo apt-get install python-setuptools  # ubuntu only
}

IS_OSX=$(uname | grep -i darwin 2> /dev/null)

if [[ "$IS_OSX" ]] ; then
    setup_brew_deps
else
	setup_apt_deps
fi

#
# Installing rest of software

# install node versions manager, I love it https://github.com/tj/n
npm install -g n

# other nodejs friends :)
npm install -g yo bower grunt-cli

# git diffs for humans
npm install -g diff-so-fancy

# for the c alias (syntax highlighted cat)
sudo easy_install Pygments


# cleanup vars
unset setup_brew_deps
unset setup_apt_deps
unset IS_OSX
