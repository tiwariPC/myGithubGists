# Fig pre block. Keep at the top of this file.
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
    source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="${HOME}/.oh-my-zsh"


# Set name of the theme to load --- if set to "random", it will
# load a random theme each time oh-my-zsh is loaded, in which case,
# to know which specific one was loaded, run: echo $RANDOM_THEME
# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes

# Set list of themes to pick from when loading at random
# Setting this variable when ZSH_THEME=random will cause zsh to load
# a theme from this variable instead of looking in $ZSH/themes/
# If set to an empty array, this variable will have no effect.
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )
# ZSH_THEME="robbyrussell"
# Uncomment the following line to use case-sensitive completion.
CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion.
# Case-sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to automatically update without prompting.
# DISABLE_UPDATE_PROMPT="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line if pasting URLs and other text is messed up.
# DISABLE_MAGIC_FUNCTIONS="true"

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# Caution: this setting can cause issues with multiline prompts (zsh 5.7.1 and newer seem to work)
# See https://github.com/ohmyzsh/ohmyzsh/issues/5765
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load?
# Standard plugins can be found in $ZSH/plugins/
# Custom plugins may be added to $ZSH_CUSTOM/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git
  macos
  zsh-autosuggestions
  zsh-syntax-highlighting
  )


source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
# Alias's to modified commands
alias cp="cp -v"
alias mv="mv -i"
alias rm="rm -iv"
alias mkdir="mkdir -p"
alias ping="ping -c 10"
alias less="less -R"
alias cls="clear"
alias apt-get="sudo apt-get"
alias multitail="multitail --no-repeat -c"
alias freshclam="sudo freshclam"
alias vi="vim"
alias svi="sudo vi"
alias vis="vim "+set si""

# Change directory aliases
alias home="cd ~"
alias cd..="cd .."
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."
alias .....="cd ../../../.."

# # Alias"s for multiple directory listing commands
# alias la="ls -Alh" # show hidden files
# alias lx="ls -lXBh" # sort by extension
# alias lk="ls -lSrh" # sort by size
# alias lc="ls -lcrh" # sort by change time
# alias lu="ls -lurh" # sort by access time
# alias lr="ls -lRh" # recursive ls
# alias lt="ls -ltrh" # sort by date
# alias lm="ls -alh |more" # pipe through "more"
# alias lw="ls -xAh" # wide listing format
# alias ll="ls -Fls" # long listing format
# alias labc="ls -lap" #alphabetical sort
# alias lf="ls -l | egrep -v "^d"" # files only
# alias ldir="ls -l | egrep "^d"" # directories only

## Install exa package with brew install exa

#List all files equivalent to ls command
alias ls="exa --icons --tree -L 1 --color always"
# List all files, including hidden files, with extended details and a header row, colorized, sorted by modification time, and displayed as a tree with a depth of 1
alias la="exa --long --icons --all --header --color always --time-style default --tree -L 1"

# List all files with extended details, colorized, sorted by extension, and displayed as a tree with a depth of 1
alias lx="exa --long --icons --sort=extension --color always --tree -L 1"

# List all files with extended details, colorized, sorted by size, and displayed as a tree with a depth of 1
alias lk="exa --long --icons --sort=size --color always --tree -L 1"

# List all files with extended details, colorized, sorted by change time, and displayed as a tree with a depth of 1
alias lc="exa --long --icons --sort=changed --color always --tree -L 1"

# List all files with extended details, colorized, sorted by access time, and displayed as a tree with a depth of 1
alias lu="exa --long --icons --sort=accessed --color always --tree -L 1"

# List all files, including hidden files, with extended details and a header row, colorized, sorted by modification time, and displayed as a tree recursively
alias lr="exa --long --icons --recurse --all --header --color always --time-style default --tree"

# List all files with extended details, colorized, sorted by modification time, and displayed as a tree with a depth of 1
alias lt="exa --long --icons --sort=modified --color always --tree -L 1"

# List all files with extended details, colorized, and displayed as a tree with a depth of 1, paginated using "more"
alias lm="exa --long --icons --all --color always --tree -L 1 | more"

# List all files with extended details, colorized, and displayed as a tree with a depth of 1, with a trailing slash on directories
alias ll="exa --long --icons --classify --color always --tree -L 1"

# List all files, including hidden files, with extended details and a header row, colorized, and displayed as a tree with a depth of 1
alias labc="exa --long --icons --all --header --color always --tree -L 1"


# List all directories, including hidden directories, with extended details, colorized, sorted by modification time, and displayed as a tree with a depth of 1
alias ldir="exa --long --classify --color always --tree -L 1 | grep '/$'"


# alias chmod commands
alias mx="chmod a+x"
alias 000="chmod -R 000"
alias 644="chmod -R 644"
alias 666="chmod -R 666"
alias 755="chmod -R 755"
alias 777="chmod -R 777"

# Search command line history
alias h="history | grep "

# Search running processes
alias p="ps aux | grep "
alias topcpu="/bin/ps -eo pcpu,pid,user,args | sort -k 1 -r | head -10"

# Search files in the current folder
alias f="find . | grep "

# Count all files (recursively) in the current folder
alias countfiles="for t in files links directories; do echo \`find . -type \${t:0:1} | wc -l\` \$t; done 2> /dev/null"

# To see if a command is aliased, a file, or a built-in command
alias checkcommand="type -t"

# Show open ports
alias openports="netstat -nape --inet"

# Alias"s for safe and forced reboots
alias rebootsafe="sudo shutdown -r now"
alias rebootforce="sudo shutdown -r -n now"

# Alias"s to show disk space and space used in a folder
alias diskspace="du -S | sort -n -r |more"
alias folders="du -h --max-depth=1"
alias folderssort="find . -maxdepth 1 -type d -print0 | xargs -0 du -sk | sort -rn"
alias tree="tree -CAhF --dirsfirst"
alias treed="tree -CAFd"
alias mountedinfo="df -hT"

# Alias"s for archives
alias mktar="tar -cvf"
alias mkbz2="tar -cvjf"
alias mkgz="tar -cvzf"
alias untar="tar -xvf"
alias unbz2="tar -xvjf"
alias ungz="tar -xvzf"

# SHA1
alias sha1="openssl sha1"

# Extracts any archive(s) (if unp isn't installed)
extract () {
    for archive in $*; do
        if [ -f $archive ] ; then
            case $archive in
                *.tar.bz2)   tar xvjf $archive    ;;
                *.tar.gz)    tar xvzf $archive    ;;
                *.bz2)       bunzip2 $archive     ;;
                *.rar)       rar x $archive       ;;
                *.gz)        gunzip $archive      ;;
                *.tar)       tar xvf $archive     ;;
                *.tbz2)      tar xvjf $archive    ;;
                *.tgz)       tar xvzf $archive    ;;
                *.zip)       unzip $archive       ;;
                *.Z)         uncompress $archive  ;;
                *.7z)        7z x $archive        ;;
                *)           echo "don't know how to extract '$archive'..." ;;
            esac
        else
            echo "'$archive' is not a valid file!"
        fi
    done
}
compress () {
	for item in "$@"; do
		if [ -e "$item" ] ; then
			if [ -f "$item" ]; then
				tar czvf "$item.tar.gz" "$item"
			elif [ -d "$item" ]; then
				tar czvf "$item.tar.gz" "$item"
			else
				echo "'$item' is not a valid file or folder!"
			fi
		else
			echo "'$item' does not exist!"
		fi
	done
}



# Searches for text in all files in the current folder
ftext ()
{
    # -i case-insensitive
    # -I ignore binary files
    # -H causes filename to be printed
    # -r recursive search
    # -n causes line number to be printed
    # optional: -F treat search term as a literal, not a regular expression
    # optional: -l only print filenames and not the matching lines ex. grep -irl "$1" *
    grep -iIHrnF --color=always "$1" . | less -r
}

# Copy file with a progress bar
cpp()
{
    set -e
    strace -q -ewrite cp -- "${1}" "${2}" 2>&1 \
    | awk '{
    count += $NF
    if (count % 10 == 0) {
        percent = count / total_size * 100
        printf "%3d%% [", percent
        for (i=0;i<=percent;i++)
            printf "="
            printf ">"
            for (i=percent;i<100;i++)
                printf " "
                printf "]\r"
            }
        }
    END { print "" }' total_size=$(stat -c '%s' "${1}") count=0
}

# Copy and go to the directory
cpg ()
{
    if [ -d "$2" ];then
        cp $1 $2 && cd $2
    else
        cp $1 $2
    fi
}

# Move and go to the directory
mvg ()
{
    if [ -d "$2" ];then
        mv $1 $2 && cd $2
    else
        mv $1 $2
    fi
}

# Create and go to the directory
mkdirg ()
{
    mkdir -p $1
    cd $1
}

# Goes up a specified number of directories  (i.e. up 4)
up ()
{
    local d=""
    limit=$1
    for ((i=1 ; i <= limit ; i++))
        do
            d=$d/..
        done
    d=$(echo $d | sed 's/^\///')
    if [ -z "$d" ]; then
        d=..
    fi
    cd $d
}

#Automatically do an ls after each cd
cd ()
{
    if [ -n "$1" ]; then
        # builtin cd "$@" && ls -ltrh
        builtin cd "$@" && exa --long --sort=modified --color always --tree -L 1 --icons
    else
        # builtin cd ~ && ls -ltrh
        builtin cd "$@" && exa --long --sort=modified --color always --tree -L 1 --icons
    fi
}

# Returns the last 2 fields of the working directory
pwdtail ()
{
    pwd|awk -F/ '{nlast = NF -1;print $nlast"/"$NF}'
}


HOSTNAME="$(hostname)"  # Conda clobbers HOST, so we save the real hostname into another variable.

precmd() {
    OLDHOST="${HOST}"
    HOST="${HOSTNAME}"
}

preexec() {
    HOST="${OLDHOST}"
}

codelxplus()
{
    code --folder-uri=vscode-remote://ssh-remote+lxplus.cern.ch/$1
}
codelxplus8()
{
    code --folder-uri=vscode-remote://ssh-remote+lxplus8.cern.ch/$1
}

codeuscms()
{
    code --folder-uri=vscode-remote://ssh-remote+login-el7.uscms.org/$1
}

# configure fzf with your cd command
cdf()
{
  local dir
  dir=$(find * -type d 2>/dev/null | fzf +m) && cd "$dir" || return
}
[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

alias conda_deact="conda deactivate"

# alias for using system kinit
alias kinit='/usr/bin/kinit'
alias kdestroy='/usr/bin/kdestroy'

# To initialize and mount the EOS
function mounteos()
{
  # kinit -kt ~/.keytab ptiwari@CERN.CH
  export EOS_MGM_URL=root://eos$1.cern.ch
  export EOS_FUSE_MGM_ALIAS=eos$1.cern.ch
  export EOS_FUSE_MOUNTDIR=/Users/ptiwari/eos$1
  eos fuse mount /Users/ptiwari/eos$1
};

function umounteos()
{
    killall eosd; eos fuse umount /Users/ptiwari/eos$1
};

alias mounteosall='mounteos project-l; mounteos home-e'
alias umounteosall='umounteos project-l; umounteos home-e'

#nvim to vim
alias vim='nvim'

# alias to log in to servers
alias lxplus='ssh ptiwari@lxplus.cern.ch'
alias lxplus8='ssh ptiwari@lxplus8.cern.ch -q'
alias lxplus7='ssh ptiwari@lxplus7.cern.ch -q'
alias cmsusrtunnel='ssh -D 9215 -f -C -q -N ptiwari@cmsusr.cern.ch'
alias lxplustunnel='ssh -D 1080 -f -C -q -N ptiwari@lxplus.cern.ch'
alias cernOffice='ssh ptiwari@128.141.188.170 -q'

alias cmsusr='ssh ptiwari@cmsusr.cern.ch -q'
alias uscms='ssh ptiwari@login-el7.uscms.org -q'
alias tifr='ssh ptiwari@ui3.indiacms.res.in -q'
alias tifrtunnel='ssh -D 9220 -f -C -q -N ptiwari@ui3.indiacms.res.in'

alias reset="clear && printf '\e[3J'"
alias root="root -l --web=firefox" # --web=off"
alias confdb="open /Users/ptiwari/computation/ConfDB/start.jnlp"


# django aliases
alias makemigrations='python manage.py makemigrations'
alias migrate='python manage.py migrate'
alias runserver='python manage.py runserver'
alias reset_db='python manage.py reset_db'
alias django_secret_key="python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
# export Homebrew's path
export PATH="/opt/homebrew/bin:$PATH"

## postgresql paths
export LDFLAGS="-L/opt/homebrew/opt/postgresql@15/lib"
export CPPFLAGS="-I/opt/homebrew/opt/postgresql@15/include"
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"

# brew update
brew-upgrade() {
    brew upgrade $(brew list | grep -v miniforge)
}

source /opt/homebrew/share/powerlevel10k/powerlevel10k.zsh-theme
# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/homebrew/Caskroom/miniforge/base/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh" ]; then
        . "/opt/homebrew/Caskroom/miniforge/base/etc/profile.d/conda.sh"
    else
        export PATH="/opt/homebrew/Caskroom/miniforge/base/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
