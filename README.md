# COVID-MAP (COVID19 TRACKER)

## Introduction

Welcome to COVID-MAP, the COVID19 Tracker.

This script sends an email of the latest COVID19 data for your chosen country and saves the data to a csv.

It uses the [Worldometers.info](https://www.worldometers.info/coronavirus/) website for the data.

The script can be run for any country on the website, and for any number of days.

---

## Prerequisites

* Uses the latest version of python
* Have a Gmail account and add your Gmail details to your environment variables (see [this](https://www.youtube.com/watch?v=IolxqkL7cD8) excellent video tutorial for how to do this)

## Installation

1. Clone this repository
2. Navigate to the cloned location
3. Run: `python setup.py install`
4. Run: `python run_covid_map.py`

## Usage

When running `covid_map.py`, it first asks the user if they want to start in debugging mode. If the answer is "Y" then debugging is set to True and it will print the data found to the console and not send an email or save the data.

The script then asks the user for the country from which the data is to be gathered (see the Worldometers website linked above for the full list).

Finally asks for number of days to run.

## Issues

Feel free to submit issues and enhancement requests.

## Contributing

To contribute to COVID-MAP, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b development/<change_type>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the development branch: `git push origin COVID-MAP/master`
5. Create the pull request.

## Ideas

Here are some ideas I have for the future of this project:

* Add ability to gather all rows in the table
* Add time to the csv data
* Mulithreading to speed up sending email and saving to csv
* Add a GUI for creating graphs and other visual data
* Add tests

Feel free to suggest more. See the Contributing section if you would like to implement my ideas or your own.
