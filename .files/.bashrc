# OSX skip this file so it loaded from bash_profile. Uncomment the line below in linux distributives
#source ~/.bash_profile

# add brew
export PATH="/usr/local/bin:$PATH"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# load bash complition
if [ -f $(brew --prefix)/etc/bash_completion ]; then
 . $(brew --prefix)/etc/bash_completion
fi

export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

# pyenv init
export PATH="$HOME/.pyenv:$PATH"
eval "$(pyenv init -)"

# added by travis gem
[ -f $HOME/.travis/travis.sh ] && source $HOME/.travis/travis.sh

# The next line updates PATH for the Google Cloud SDK.
if [ -f $HOME'/Downloads/google-cloud-sdk/path.bash.inc' ]; then . $HOME'/Downloads/google-cloud-sdk/path.bash.inc'; fi

# The next line enables shell command completion for gcloud.
if [ -f $HOME'/Downloads/google-cloud-sdk/completion.bash.inc' ]; then . $HOME'/Downloads/google-cloud-sdk/completion.bash.inc'; fi
export PATH="/usr/local/opt/helm@2/bin:$PATH"
