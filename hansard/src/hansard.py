from datetime import datetime, timedelta
from urllib.request import urlopen
from urllib.error import HTTPError
import os
from bs4 import BeautifulSoup
import json


class Hansard:
    """
    Class for gathering and manipulating Hansard data

    Attributes:
        start_date: datetime.date
            First date of interest
        end_date: datetime.date
            Last date of interest
    """

    def __init__(self, start_date, end_date):
        """
        Initialises Hansard class

        Args:
            start_date: str
                First date of interest in YYYY-MM-DD form
            end_date: str
                First date of interest in YYYY-MM-DD form
        """

        # Convert dates from strings to date objects
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        self.start_date = start_date
        self.end_date = end_date

    def download(self):
        """
        Downloads all avaliable Hansard between two dates and stores as .html for
        each day
        """

        date = self.start_date

        while date <= self.end_date:
            date_str = date.strftime("%Y-%m-%d")

            f_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/html/{date_str}.html"

            # If file exists skip
            if os.path.isfile(f_name):
                date += timedelta(days=1)
                continue

            # If no data on that day create empty file regardless to save progress
            try:
                url = f"https://hansard.parliament.uk/html/Commons/{date_str}/CommonsChamber"
                request = urlopen(url)
                html = BeautifulSoup(request, features="lxml")
            except HTTPError:
                html = ""

            f = open(f_name, "w", encoding='utf-8')
            f.write(str(html))
            f.close()

            date += timedelta(days=1)

    def extract(self):
        """
        Converts all .html to json files with member and utterance as values

        Raises:
            RuntimeError:
                html file not found for day within range
        """

        date = self.start_date

        while date <= self.end_date:
            date_str = date.strftime("%Y-%m-%d")

            html_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/html/{date_str}.html"
            json_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/json/{date_str}.json"

            # If file not found raise an error
            if not os.path.isfile(html_name):
                raise RuntimeError(f"No data found downloaded for {date}")

            # If file exists skip
            if os.path.isfile(json_name):
                date += timedelta(days=1)
                continue

            html = open(html_name, encoding="utf-8")
            soup = BeautifulSoup(html, "html.parser")

            # If no data skip
            if soup == "":
                date += timedelta(days=1)
                continue

            # Get all utterance divs
            divs = soup.find_all("div", {"class": "debate-item debate-item-contributiondebateitem"})

            utterances = []

            # Places each utterance into a dict.
            for div in divs:
                # Get member id, if not availiable this is not a valid utterance
                try:
                    member_link = div.find('a', {"class": "attributed-to-details with-link"})['href']
                except TypeError:
                    continue

                member_id = member_link.split("memberId=")[1]
                member_id = int(member_id)

                # Get utterance
                paras = div.find_all("p", {"class": "hs_Para"})

                utterance_texts = [para.getText() for para in paras]
                utterance_text = "".join(utterance_texts)

                utterance_dict = {"member_id": member_id, "text": utterance_text}
                utterances.append(utterance_dict)

            # If no utterances create empty file
            f = open(json_name, "w", encoding="utf-8")
            if len(utterances) != 0:
                json.dump(utterances, f, ensure_ascii=False)
            f.close()

            date += timedelta(days=1)
