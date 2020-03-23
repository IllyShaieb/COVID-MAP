"""comap.py - This script sends an email of the latest COVID19 data for your chosen country and saves the data to a csv."""

# BUILT-IN MODULES
import csv
from datetime import date, datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

# INSTALLED MODULES
from bs4 import BeautifulSoup
import requests


class Coronovirus():
    """Class for getting coronavirus data for a country and sending the data as a message 

    ...

    Attributes
    ---------
    debugging (boolean) : If debugging is set to True then it will print the data found to the console without writing to the file or sending an email.

    country (string) : The country used in the search for the data.

    page (object) : The response from the GET request sent to the website used for getting COVID19 data. https://www.worldometers.info/coronavirus/

    soup (object) : Instance of the BeautifulSoup class.

    data (dictionary) : The dictionary containing the gathered table data.

    message (string) : The output message formatted with the gathered data. 

    Methods
    -------

    get_time_now() : Gets the current time and formats in HH:MM:SS

    get_data() : Scrapes the data from a page.

    format_value() : If the values is empty then set the value to 0 else return original text.

    send_email() : Sends an email using the subject and message specified.

    write_to_csv() : Gets the data specified and saves to csv.

    """

    def __init__(self, debugging=False, country="UK"):
        """If debugging is set to True then it will print the data found to the console (Default = False). Country default is UK. """

        self.debugging = debugging
        self.country = country

        print(f"{self.get_time_now()} | Accessing website...")
        self.page = requests.get("https://www.worldometers.info/coronavirus/")
        self.soup = BeautifulSoup(self.page.text, "html.parser")

        self.data = {}
        self.message = ""

    def get_time_now(self):
        """Gets the current time and formats in HH:MM:SS """

        now = datetime.now()

        time_now = datetime.strftime(now, "%H:%M:%S")

        return time_now

    def get_data(self):
        """Scrapes the data from a page."""

        print(f"{self.get_time_now()} | Finding table...")
        table = []
        table = self.soup.find("table")

        print(f"{self.get_time_now()} | Finding headers...")
        table_head = table.find("thead")
        table_head_row = table_head.find_all("tr")
        headers = []
        for header in table_head_row[0].find_all('th'):
            header = header.text.replace("\xa0", " ")
            header = header.replace(",", " ")
            headers.append(header)

        headers.append("Date")

        print(f"{self.get_time_now()} | Finding {self.country} row...")
        table_body = table.find("tbody")
        row_data = []
        table_rows = table_body.find_all("tr")
        for table_row in table_rows:
            row_data = table_row.find_all("td")
            if self.country in row_data[0].text:
                row_data = row_data
                break

        country = row_data[0].text.strip()
        total_cases = row_data[1].text.strip()
        new_cases = self.format_value(row_data[2].text.strip())
        total_deaths = self.format_value(row_data[3].text.strip())
        new_deaths = self.format_value(row_data[4].text.strip())
        total_recovered = self.format_value(row_data[5].text.strip())
        active_cases = self.format_value(row_data[6].text.strip())
        serious_critical = self.format_value(row_data[7].text.strip())
        tot_cases_per_million = self.format_value(row_data[8].text.strip())

        data = {
            headers[0]: country,
            headers[1]: total_cases,
            headers[2]: new_cases,
            headers[3]: total_deaths,
            headers[4]: new_deaths,
            headers[5]: total_recovered,
            headers[6]: active_cases,
            headers[7]: serious_critical,
            headers[8]: tot_cases_per_million,
            "Date": date.today()
        }

        subject = f"Coronovirus Updates for {country} on {date.today()}"
        message = f"""\
            Total Cases: {total_cases}
            New Cases: {new_cases}
            Total Deaths: {total_deaths}
            New Deaths {new_deaths}
            Total Recovered: {total_recovered}
            Active Casses: {active_cases}
            Serious Critical: {serious_critical}
            Total Cases/1M pop: {tot_cases_per_million}
            
            Data gathered from: https://www.worldometers.info/coronavirus/
            """

        if self.debugging == True:
            print(message)
        else:
            self.write_to_csv(headers, data)
            self.send_email(subject, message)

    def format_value(self, text):
        """If the values is empty then set the value to 0 else return original text."""

        if text == " ":
            return '0'
        else:
            return text

    def send_email(self, subject, message):
        """Sends an email using the subject and message specified."""

        email = os.environ.get('GMAIL_ADDRESS')
        password = os.environ.get('GMAIL_PASSWORD')

        msg = MIMEMultipart()

        msg['From'] = email
        msg['To'] = email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email, password)
            server.send_message(msg)

        print(f"{self.get_time_now()} | Email sent to: {email}")

    def write_to_csv(self, headers, data):
        """Gets the data specified and saves to csv."""

        if not os.path.exists("data"):
             os.makedirs("data")

        filename = f"data/covid_map.csv"

        if os.path.exists(filename):
            with open(filename, mode='a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writerow(data)
        else:
            with open(filename, mode='w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=headers)
                writer.writeheader()
                writer.writerow(data)

        print(f"{self.get_time_now()} | Data written to: {filename}")


def main():
    """Starts the COVID19 tracker. First asks the user if they want to start in debugging mode. Then asks the user for the country (default is UK). Then asks the user to choose whether to run in debug mode (which only prints the results but does not send an email or save the results). Also asks for number of days to run."""

    try:

        print("--------------------------\nStart of COVID19 tracking.\n--------------------------")

        counter = 0
        number_of_seconds = 86400

        while True:
            debug = input(
                "Do you want to run in debugging mode? Y/N: ").lower()
            if debug == "y" or debug == "n":
                break

        if debug == "y":
            debugging = True
        elif debug == "n":
            debugging = False

        while True:
            country = input(
                "Enter the country you want to get data for: ")
            if country != "":
                break

        number_of_days = int(input("Enter the number of days to run: "))
        answer = "Y"

        while True:

            if counter >= number_of_days:

                while True:
                    answer = input(
                        "Do you want to continue tracking? Y/N: ").lower()
                    if answer == "y" or answer == "n":
                        break

                if answer == "y":
                    counter = 0
                    continue
                elif answer == "n":
                    break
            else:

                counter += 1

                print(f"----------- Day: {counter} ------------")
                cv = Coronovirus(debugging, country)
                cv.get_data()
                print("----------------------------------------")

    except TimeoutError:
        print("Could not establish a connection with the website.")

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        print("--------------------------\nEnd of COVID19 tracking.\n--------------------------")


if __name__ == "__main__":

    main()
