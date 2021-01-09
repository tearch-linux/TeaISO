# üşengeçlik
alias c='clear'
alias e='export'
alias a='alias'
alias t='touch'
alias m='mkdir -pv'
alias r='rm -rfv'
alias x='chmod +x -R'
alias h='history'
alias e='exit'
alias j='jobs -l'
alias s='sync'
alias rm='rm -I --preserve-root'
alias chown='chown --preserve-root'
alias chmod='chmod --preserve-root'
alias chgrp='chgrp --preserve-root'
alias clear='echo -ne "\033c" ; clear'
alias hs='history | grep'
alias ~="cd ~"
alias ..='cd ..'
alias ...="cd ../../"
alias ....="cd ../../../"
#diyarbakır keranesi modu (bol renkli çıktı)
alias grep='grep --color=auto'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
if ls --color -d . >/dev/null 2>&1; then  # GNU ls
  export COLUMNS  # Remember columns for subprocesses.
  eval "$(dircolors)"
  function ls {
    command ls -F -h --color=always -v --author --time-style=long-iso -C "$@" | less -R -X -F
  }
  alias ll='ls -l'
  alias l='ls -l -a'
  alias la='ls -a'
fi
#PS1 PS2 
export PS1="\[\033[1m\]\u@\h \[\033[0;31m\]\W \$ \[\033[00m\]"
export PS2="\[\033[1m\]>\[\033[00m\] "
# bazı önemli ama gereksiz işler
alias vi=nano
alias vim=nano
ğ(){
    rm -fv ~/.bash_history
    rm -rfv /tmp/* 2>/dev/null
    rm -rfv ~/.cache 2>/dev/null
}

