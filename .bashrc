################################################################################
# push this content at the end of your ~/.bashrc file

# enable 256 colors for terminal
if [ "$TERM" == "xterm" ]; then
    # No it isn't, it's gnome-terminal
    export TERM=xterm-256color
fi

# add path to java
export JAVA_HOME=/usr/lib/jvm/java-7-oracle

# shorthand to binaries
PATH=$PATH:$HOME/bin
