from datetime import datetime, timedelta
import os
import json


class Corpus:
    """
    Class for creating corpus of words to train on

    Attributes:
        start_date: datetime.date
            First date of interest
        end_date: datetime.date
            Last date of interest
    """

    def __init__(self, start_date, end_date):
        """
        Initialise corpus class

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

    def full(self):
        """
        Creates a .txt file containing all utterances

        Raises:
            RuntimeError:
                No json file found for a date in range
        """

        date = self.start_date
        f_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/corpus/{self.start_date}_{self.end_date}.txt"

        # If file exists skip
        if os.path.isfile(f_name):
            return

        while date <= self.end_date:
            date_str = date.strftime("%Y-%m-%d")

            json_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/json/{date_str}.json"

            # If file not found raise an error
            if not os.path.isfile(json_name):
                raise RuntimeError(f"No data found downloaded for {date}")

            # If file empty skip
            if os.stat(json_name).st_size == 0:
                date += timedelta(days=1)
                continue

            f = open(json_name, encoding="utf-8")
            utterances = json.loads(f.read())
            f.close()

            for utterance in utterances:
                text = utterance["text"]

                # Opens corpus file
                f = open(f_name, 'a', encoding="utf-8")

                f.write(text)
                f.write('\n')

                f.close()

            date += timedelta(days=1)

    def members(self):
        """
        Creates a .txt for each member found containing all their utterances

        Raises:
            RuntimeError:
                No json file found for date in range
        """
        date = self.start_date

        while date <= self.end_date:
            date_str = date.strftime("%Y-%m-%d")

            json_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/json/{date_str}.json"

            # If file not found raise an error
            if not os.path.isfile(json_name):
                raise RuntimeError(f"No data found downloaded for {date}")

            # If file empty skip
            if os.stat(json_name).st_size == 0:
                date += timedelta(days=1)
                continue

            f = open(json_name, encoding="utf-8")
            utterances = json.loads(f.read())
            f.close()

            for utterance in utterances:
                member_id = utterance["member_id"]
                text = utterance["text"]

                # Opens member corpus
                corpus_name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + f"/data/corpus/{member_id}.txt"
                f = open(corpus_name, 'a', encoding="utf-8")

                f.write(text)
                f.write('\n')

                f.close()

            date += timedelta(days=1)

