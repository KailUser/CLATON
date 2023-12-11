import PySimpleGUI as sg
import requests
import zipfile
import io
import os
import shutil
from ext.core import download_linux


def fetch_version_info(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            version_info = response.text.strip()  # Remove leading/trailing whitespaces or newline characters
            return version_info
        else:
            print(f"Failed to fetch version info. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"Request Exception: {e}")
    return None

# URL to the version.txt file
version_url = 'https://raw.githubusercontent.com/KailUser/CLATON/beta/version'

# Fetch version information
version = fetch_version_info(version_url)
installed_version = "0.0.2v-beta"




if installed_version == version or installed_version >= version:
    sg.theme("DarkPurple1")

    layout = [
        [sg.Checkbox('Install hekate', enable_events=True, key='hekate', disabled=True, default=True)],
        [sg.Checkbox('Install kefir', enable_events=True, key='kefir')],
        [sg.Checkbox('Install HBMenu', enable_events=True, key='hbmenu')],
        [sg.Text('Enter device letter:'), sg.Input(key='device_letter')],
        [sg.Text("Linux Distro (Core l4t):"), sg.DropDown(values=["Without Linux","Ubuntu", "Ubuntu Jammy", "Fedora", "Lakka"], key="l4t", default_value="Without Linux")],
        [sg.Button('Start install process')],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='progressbar')]
    ]

    window = sg.Window('CLATON (By @Syirezz)', layout, size=[400, 250])


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

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        if event == 'Start install process':
            device_letter = values['device_letter']
            hekate_installed = values['hekate']
            kefir_installed = values['kefir']
            hbmenu_installed = values['hbmenu']
            destination_folder = f"{device_letter}\\"
            progress_bar = window['progressbar']

            print('Start install process')
            print(f"Device Letter: {device_letter}")
            print(f"Install Hekate: {hekate_installed}")
            print(f"Install Kefir: {kefir_installed}")
            print(f"Install HBMenu: {hbmenu_installed}")

            if device_letter.upper() == 'C:':
                sg.popup("This is a Windows System driver")
            else:
                # Replace with your GitHub release URL
                release_url = 'https://github.com/CTCaer/hekate/releases/download/v6.0.7/hekate_ctcaer_6.0.7_Nyx_1.5.6.zip'

                # Path to the device letter's directory
                destination_folder = f"{device_letter}\\"

                progress_bar = window['progressbar']

                if download_and_extract_archive(release_url, destination_folder, progress_bar):
                    sg.popup("Successful download of hekate!")
                else:
                    sg.popup("Failed to download or extract hekate archive!")

                    # Replace with your GitHub release URL
                    release_url = 'https://github.com/CTCaer/hekate/releases/download/v6.0.7/hekate_ctcaer_6.0.7_Nyx_1.5.6.zip'

                    # Path to the device letter's directory

                    if download_and_extract_archive(release_url, destination_folder, progress_bar):
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
                        else:
                            print('')


                        sg.popup("Successful download of hekate!")
                    else:
                        sg.popup("Failed to download or extract hekate archive!")
            if kefir_installed == True:
                if device_letter.upper() == 'C:':
                    sg.popup("This is a Windows System driver")
                else:
                    # Replace with your GitHub release URL
                    release_url = 'https://codeberg.org/rashevskyv/kefir/releases/download/714/kefir714.zip'

                    # Path to the device letter's directory
                    

                    if download_and_extract_archive(release_url, destination_folder, progress_bar):
                        sg.popup("Download and extraction successful!")
                    else:
                        sg.popup("Failed to download or extract archive!")
            else:
                print("Skip kefir install. Because user choose without kefir")

            if values["l4t"] != "Without Linux":
                if values["l4t"] == "Ubuntu Jammy":
                    if device_letter.upper() == 'C:':
                        sg.popup("This is a Windows System driver!")
                    else:
                        download_linux("https://download.switchroot.org/ubuntu-jammy/theofficialgman-ubuntu-jammy-5.1.2-2023-09-18.7z", destination_folder, window)
                if values["l4t"] == "Ubuntu":
                    if device_letter.upper() == 'C:':
                        sg.popup("This is a Windows System driver!")
                    else:
                        download_linux("https://download.switchroot.org/ubuntu/switchroot-ubuntu-5.1.1-2023-06-12.7z", destination_folder, window)
                if values["l4t"] == "Lakka":
                    if device_letter.upper() == 'C:':
                        sg.popup("This is a Windows System driver!")
                    else:
                        download_linux("https://download.switchroot.org/lakka/Lakka-Switch.aarch64-4.4-devel-20230205105156-84d68bd.tar", destination_folder, window)

                        
    window.close()
else:
    sg.popup(f"New update available\nVersion installed: {installed_version} \nNew version: {version}" ,title="CLATON", button_type=sg.POPUP_BUTTONS_OK)