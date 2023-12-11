import requests
import shutil
import zipfile
import os

def download_and_extract_archive(url, destination_folder, progress_bar):
    response = requests.get(url, stream=True)
    total_length = response.headers.get('content-length')
    if total_length is None:  # No content length header
        return False
    total_length = int(total_length)
    bytes_downloaded = 0
    with open('temp.zip', 'wb') as f:
        for data in response.iter_content(chunk_size=4096):
            bytes_downloaded += len(data)
            f.write(data)
            progress_bar.UpdateBar((bytes_downloaded / total_length) * 100)
    with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
        zip_ref.extractall(destination_folder)
    os.remove('temp.zip')
    return True

def download_linux(url, disk, window):
    release_url = url

                        # Path to the device letter's directory
    destination_folder = f"{disk}\\"

    progress_bar = window['progressbar']

    if download_and_extract_archive(release_url, destination_folder=destination_folder , progress_bar=progress_bar):
        f = open(destination_folder + '/bootloader/nyx.ini', mode="w")
        f.write("""[config]
themebg=0
themecolor=177
entries5col=0
timeoff=4650
homescreen=0
verification=1
umsemmcrw=0
jcdisable=0
jcforceright=0
bpmpclock=1

""")
        f.close()
        url = "https://gcdnb.pbrd.co/images/DrsS9a9JAMt3.bmp?o=1"
        file_name = "background.bmp"
        res = requests.get(url, stream = True)
        if res.status_code == 200:
            with open(f"{destination_folder}/bootloader/res/" + file_name,'wb') as f:
                shutil.copyfileobj(res.raw, f)
                # print('Image sucessfully Downloaded: ',file_name)