from urllib.parse import urljoin
from bs4 import BeautifulSoup
import re
#from multiprocessing import Pool, Process
import os
import time
import pandas as pd
import requests
import json
import pandas as pd
import Lib.URLM3
import Lib.SCRAPM3

EXPORT_FILE = "M3urls3.txt"
HTML_FOLDER = "../urls/"
DATA_FOLDER = "../data/"

Lib.URLM3.getURLSM3(EXPORT_FILE, HTML_FOLDER, DATA_FOLDER)

EXPORT_FOLDER = "../data2/"

Lib.SCRAPM3.scrapM3(EXPORT_FOLDER, HTML_FOLDER, DATA_FOLDER, EXPORT_FILE)


