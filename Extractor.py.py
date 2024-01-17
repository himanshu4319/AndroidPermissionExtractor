import os
import subprocess

apk_type=0
def extract_apks(folders):
    for folder in folders:
        apk_type = 0 if folder == './BenignAPK' else 1
        apk_path = f"{folder}/"
        apk_names = os.listdir(f"./{folder}")

        if not apk_names:
            print("One of the folders containing APKs is empty")
            return

        for apk_count, data in enumerate(apk_names, start=1):
            target_apk = apk_path + data
            print(target_apk)
            print("------------------------------------------------------------------")
            print(f"\t{folder} \t {data} \t\t {apk_count}/{len(apk_names)}")
            print("------------------------------------------------------------------\n")

            name = data.split(".")
            apktool_path=r".\Helper\apktool.bat"
            subprocess.run([apktool_path, "d", "--no-src", "-f", "-s", "-o", f"./UnpackedApk/{name[0]}Extract", target_apk], check=True)

def writerAndRemover(extractPath):
    
    
    with open("data.csv",'w') as file:
        
        pass     
            
if __name__ == "__main__":
    apk_folders = ['./MalwareAPK', './BenignAPK']
    extract_apks(apk_folders)
