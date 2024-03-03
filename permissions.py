import __main__
import logging

if __main__.enviorment_tables["debug_mode"]:
    logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
else:
    logging.basicConfig(level=logging.WARNING, format='[%(asctime)s] [%(name)s/%(levelname)s] %(message)s')
logger = logging.getLogger("User Permissions")

# Permissions will be implemented once User adding / removing


# Level 1 = Full access of the OS
# Level 2 = Cannot access system but can access PPM
# Level 3 = Cannot access both system and PPM
