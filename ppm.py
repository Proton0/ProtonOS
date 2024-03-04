import __main__
import logging
import json
import os
import shutil
import requests

import permissions

if __main__.enviorment_tables["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("Proton Package Manager")

PPM_default = {}

if os.path.exists("os_filesystem/system/ppm.json"):
    logger.info("PPM already exists")
else:
    os.mkdir("os_filesystem/ppm")
    f = open("os_filesystem/system/ppm.json", "w")
    f.write(json.dumps(PPM_default))
    f.close()
    logger.info("Created PPM json succesfully")

__main__.Load_PPM_Modules()  # LoadPPMModules is in Main because of some issues regarding enviorment table and main-definied stuff


def install_package_local(command):
    if command[0] == "install_package_local":
        if not len(command) >= 3:  # ppm install <package name> <package py name>
            print("Not enough arguments provided for the command")
            return
        if not permissions.FSOperationAllowed(__main__.enviorment_tables["logged_in_user"], "ppm"):
            print("permission error")
            return
        print(f"Installing PPM {command[1]} with file {command[2]}")
        logger.info("opened ppm")
        f = open("os_filesystem/system/ppm.json", "r+")
        logger.info("loading ppm")
        k = json.load(f)
        logger.info("putting ppm config")
        k[command[1]] = f"os_filesystem.ppm.{command[2]}"
        logger.info("Writing new ppm config")
        f.seek(0)
        f.write(json.dumps(k))
        f.truncate()
        print("Installed succesfully")
        f.close()


def uninstall_package(command):
    if command[0] == "uninstall_package":
        if not len(command) >= 2:
            print("not enough arguments provided for the command")
            return
        if not permissions.FSOperationAllowed(__main__.enviorment_tables["logged_in_user"], "ppm"):
            print("permission error")
            return
        shutil.rmtree(f"os_filesystem/ppm/{command[1]}")
        logger.info("Deleted package from filesystem")
        logger.info("opening ppm")
        f = open("os_filesystem/system/ppm.json", "r+")
        logger.info("parsing")
        data = json.load(f)
        logger.info("deleting entries")
        del data[command[1]]
        f.seek(0)
        logger.info("writing ppm with new data")
        f.write(json.dumps(data))
        f.truncate()
        logger.info("closing ppm")
        f.close()
        print("Uninstalled package succesfully")


def install_package(command):
    if command[0] == "install_package":
        if not __main__.enviorment_tables["ppm_allow_online"]:
            print("Please set ppm_allow_online to true to use this command")
            return
        if not len(command) >= 2:  # install_package <package name>
            print("Not enough arguments provided for the command")
            return
        if not permissions.FSOperationAllowed(__main__.enviorment_tables["logged_in_user"], "ppm"):
            print("permission error")
            return
        logger.info("Contacting server")
        r = requests.get(f"{__main__.enviorment_tables['ppm_online_server']}/packages.json")
        if r.status_code != 200:
            logger.error(f"Server returned status code : {r.status_code} with message : {r.content}")
        packages = r.json()
        logger.info(packages)
        for pkg, pkgdata in packages.items():
            if pkg == command[1]:
                if os.path.exists(f"os_filesystem/ppm/{pkg}"):
                    print("The package is already installed. Press Y to re-install the package")
                    k = input("Press Y to re-install the package : ")
                    if k.lower() == "y":
                        shutil.rmtree(f"os_filesystem/ppm/{pkg}")
                        logger.info("Deleted package from filesystem")
                        logger.info("opening ppm")
                        f = open("os_filesystem/system/ppm.json", "r+")
                        logger.info("parsing")
                        data = json.load(f)
                        logger.info("deleting entries")
                        del data[pkg]
                        f.seek(0)
                        logger.info("writing ppm with new data")
                        f.write(json.dumps(data))
                        f.truncate()
                        logger.info("closing ppm")
                        f.close()

                logger.info(f"getting data for package {pkg}")
                logger.info(
                    f"Python file is {pkgdata['py_file']} and the items required for the package is {pkgdata['pkg_data']}")
                os.mkdir(f"os_filesystem/ppm/{pkg}")
                for file in pkgdata['pkg_data']:
                    print(f"Downloading {file}")
                    r = requests.get(f"{__main__.enviorment_tables['ppm_online_server']}/{file}")
                    if r.status_code != 200:
                        logger.error(f"Error while downloading {file} : {r.status_code} with message {r.content}")
                    f = open(f"os_filesystem/ppm/{file}", "wb")  # put the data of the file
                    f.write(r.content)
                    f.close()
                print("Download complete")
                print(f"Installing {pkg}")
                logger.info("opening ppm")
                f = open("os_filesystem/system/ppm.json", "r+")
                logger.info("parsing")
                data = json.load(f)
                logger.info("adding entries")
                data[pkg] = pkgdata['py_file']
                f.seek(0)
                logger.info("writing ppm with new data")
                f.write(json.dumps(data))
                f.truncate()
                logger.info("closing ppm")
                f.close()
                print("Installed package succesfully")


# Set the commands up (bug fix)
__main__.system_commands.append(install_package_local)
__main__.system_commands.append(install_package)
__main__.system_commands.append(uninstall_package)
