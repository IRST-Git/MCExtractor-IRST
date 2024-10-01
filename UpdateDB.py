import requests
import sys
import os

def VersionCheck():
    global DBVersion
    with open("Changelog.txt","r") as file:
        DBlines=file.readlines()
    for line in DBlines:
        if "r" in line:
            DBVersion = line
            break

def VersionFetchGit():
    global FetchedVersion, FetchedData
    url = "https://raw.githubusercontent.com/platomav/MCExtractor/refs/heads/master/Changelog.txt"
    response = requests.get(url)
    if response.status_code == 200:
        FetchedData = response.text
        FecthedLines = response.text.splitlines()
        for line in FecthedLines:
            if "r" in line:
                FetchedVersion = line
                break
    else:
        print(f"Failed to fetch file. Status code: {response.status_code}")
        sys.exit()

def Update():
    VersionCheck()
    VersionFetchGit()
    if DBVersion == (FetchedVersion + "\n") or DBVersion == FetchedVersion or (DBVersion + "\n") == FetchedVersion or (DBVersion + "\n") == (FetchedVersion + "\n"):
        print("No updates found.")
        #os.system('start "" "' + 'MCE.exe' + '"')
    else:
        print("Updating Database...")
        with open("Changelog.txt","w") as file:
            file.writelines(FetchedData)
        url = "https://github.com/platomav/MCExtractor/raw/refs/heads/master/MCE.db"
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open("MCE.db", 'wb') as f:
                for chunk in response.iter_content(chunk_size=102400):
                    if chunk:
                        f.write(chunk)
            print(f"File downloaded successfully: {"MCE.db"}")
            print("Done")
        else:
            print(f"Failed to download the file. Status code: {response.status_code}")
        #os.system('start "" "' + 'MCE.exe' + '"')

Update()