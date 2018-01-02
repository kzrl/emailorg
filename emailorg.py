#!/usr/bin/env python3
import os
import email
import subprocess
import json

def main():
    config = read_config()

    orgFile=os.path.join(config["orgDir"], config["orgFile"])
    
    sig = read_signature(config["signatureFile"])
    
    newDir = os.path.join(config["mailDir"], "new")
    curDir = os.path.join(config["mailDir"], "cur")

    newfiles = os.listdir(newDir)

    # Loop over new files
    # Open them, parse and append to orgFile
    for n in newfiles:
        newfile = os.path.join(newDir,n)
        curfile = os.path.join(curDir, n)

        with open(orgFile, "a") as of:
            with open(newfile) as f:
                msg = email.message_from_file(f)

                # loop over the parts of the message
                for part in msg.walk():
                    
                    # we only want to append plain text parts
                    if part.get_content_type() == "text/plain":
                        payload = part.get_payload(decode=True).decode()
                        payload = strip_signature(sig,payload)

                        # append the content of the email as an orgmode list item
                        content = "* {}".format(payload)
                        of.write(content)
                        
            # Move the processed email to cur directory
            os.rename(newfile, curfile)
            
    # Shell out to git - commit and push
    cmd = "git add {} && git commit -am 'commit by emailorg.py' && git push origin master".format(orgFile)
    result = subprocess.run(cmd, shell=True, cwd=config["orgDir"], check=True)

    
def read_config():
    with open("config.json") as configFile:
        config = json.load(configFile)
    return config

def read_signature(filename):
    with open(filename) as f:
        sig = f.read()
        return sig

def strip_signature(sig, payload):
    p = payload.replace(sig, "")
    p = p.replace("--", "")
    return p

if __name__ == "__main__":
    main()
