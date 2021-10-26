#!C:\Users\mario\Documents\GitHub\AmbakitiShop\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'pimp==0.3.1.dev0','console_scripts','pimp'
__requires__ = 'pimp==0.3.1.dev0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pimp==0.3.1.dev0', 'console_scripts', 'pimp')()
    )
