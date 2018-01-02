# emailorg

Email to Orgmode using python, mbsync (isync) and git

## Motivation

I keep my orgmode files in a git repository and I want to be able to add notes and URLs from my phone.

## How it works

1. emailorg checks the new/ directory made by mbsync
2. For each email: Get the plaintext, strips out the signature, adds it as a list item to the specified .org file
3. Move email to cur/ directory
4. Commit changes to git. Push to origin master


## Requirements

Requires that git, mbsync and git are in your $PATH

### Debian

```
apt install git isync python3
```


## Configuration

TODO - describe how to set it up with mbsync via cron

```
mkdir -p ~/src/emailorg
git clone git@github.com:kzrl/emailorg.git ~/src/emailorg
cd ~/src/emailorg
mv example_config.json config.json
mv example_signature.txt signature.txt
# edit config.json and signature.txt to suit
```