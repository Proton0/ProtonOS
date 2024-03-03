import time
import __main__
import logging
import shutil
import json

if __main__.enviorment_tables["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("Watchdog")

def watchdog(package_name, last_imported_module):
    counter = 0
    while counter < 5:
        time.sleep(1)  # Wait for 300ms
        if last_imported_module != package_name:
            break  # Module has been successfully imported, exit watchdog
        else:
            counter += 1

    if counter == 10:
        logger.error(f"Module {package_name} is causing an issue.")
        shutil.rmtree(f"os_filesystem/ppm/{package_name}")
        logger.info("Deleted package from filesystem")
        logger.info("opening ppm")
        f = open("os_filesystem/system/ppm.json", "r+")
        logger.info("parsing")
        data = json.load(f)
        logger.info("deleting entries")
        del data[package_name]
        f.seek(0)
        logger.info("writing ppm with new data")
        f.write(json.dumps(data))
        f.truncate()
        logger.info("closing ppm")
        f.close()
        print("ProtonOS Recovery")
        print(f"Watchdog has detected an issue with the package '{package_name}', because of this '{package_name}' has been uninstalled")
        print("If the system is exiting then please restart ProtonOS")
        exit()