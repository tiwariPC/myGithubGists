Install github cli
```brew install gh```

Then run :
```for repo in $(gh gist list -L 50 | awk '{ print $1 }'); do git clone https://gist.github.com/tiwariPC/$repo 2> /dev/null; done```