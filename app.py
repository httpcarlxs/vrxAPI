import os, requests, json
from datetime import datetime, timedelta
import time
import re
import pandas as pd
from openpyxl.styles import Alignment, Font
import util


if __name__ == "__main__":
    API_KEY, API_URL = util.load_configuration()
    HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
    }
    