import os,shutil,csv
import subprocess
import xml.etree.ElementTree as ET

apk_type=0
permissionCollection = set()
packageName=''
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

            # specifying unpacked directory or android manifest file path
            unpackedDir=f"./UnpackedAPK/{name[0]}Extract"
            manifestPath = unpackedDir+"/AndroidManifest.xml"

            # parsing xml file for fetching permissions
            try:
                root = ET.parse(manifestPath).getroot()

                #command for finding package name
                packageName = root.get("package")

                #command for finding permissions
                permissions = root.findall("uses-permission")
                # print(permissions)

                print("  SET STATUS :", end=' ')        # ADD NEW PERMISSION TO THE LIST
                for perm in permissions:
                    for att in perm.attrib:
                        permelement = perm.attrib[att]
                        if permelement in permissionCollection:
                            print("0", end=' ')
                        else:
                            # print("1", end=' ')
                            permissionCollection.add(permelement)
            except:
                print("An exception is encountered")

            shutil.rmtree(unpackedDir)
            # print(permissionCollection)
            permList = list(permissionCollection)

            permList.insert(0,packageName)

            with open(f"UpdatePermList.csv", 'a') as file:        # SAVE LIST IN FILE.
                writer = csv.DictWriter(file,fieldnames=permList)
                # writer.writeheader()
                for i in permList:
                    file.write(f"{i},")
                file.write("\n\n")                    

  
            
if __name__ == "__main__":
    apk_folders = ['./BenignAPK','./MalwareAPK',]
    extract_apks(apk_folders)
