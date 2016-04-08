# Tmux-Parallel

Run commands in parallel using tmux.

Design for speed up brew installation, but also helpful in other situations maybe.

## Usage

Assume that we have a text file with brew install commands, whichi named `./brew1`.

```bash
#! /bin/bash
# file: brew1
brew cask install evernote
brew cask install inboard
brew cask install macvim
brew cask install macdown
# brew cask install qq
brew cask install qq
brew cask install qq
brew cask install qq
brew cask install qq
brew cask install qq
brew cask install qq
brew cask install qq
```

We can comment lines using `#` just like shell scripts.

Then we run this installation in parallel with tmux-parallel.

```bash
python ./tmux-parallel.py -f ./brew1
```

Following is a snapshot of the install progress.

![](https://i.imgur.com/Zr5voF6.png)

However, commands can be fail or interrupted and return a non-zero code. We can decide to retry it or not.

![](https://i.imgur.com/od0sZoj.png)

Isn't it cool?
