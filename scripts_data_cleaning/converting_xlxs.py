import os
rootdir = "/Users/giovanniabbatepaolo/Downloads/Scuola Open Source"

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        print os.path.join(subdir, file)