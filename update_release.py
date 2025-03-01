import requests
import pathlib
from google import genai

client = genai.Client(api_key="AIzaSyAUq_ZTk_bm0k9dmGLZERlAMVCmrO7qISc")


link = ["https://api.github.com/repos/VSCodium/vscodium/releases/latest",
        'https://api.github.com/repos/junegunn/fzf/releases/latest'
        ]
# Download file

for i in link:
    response = requests.get(
        i
    )
    pathlib.Path('a11.txt').write_text(response.text)

    my_file = client.files.upload(file='a11.txt')
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=[
            'In this file, if there is a .deb file, give it first priority and return me the download link. Howveer if it doesnt exist, return me a tar.gz. file and it must support x86/amd. always use 64 bits. Return ur answer to me in 1 word (which is the link). If it dosent satisfy anything return nil.After that finished successfully, answer me in 1 word the version number of that latest release. Give ur response in the form of [ver.no, link]' , 
            my_file
        ]
    )
    print(response.text)
