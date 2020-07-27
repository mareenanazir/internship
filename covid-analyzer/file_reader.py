import csv
from pathlib import Path

from .constants import (TOTAL_CASES, TOTAL_RECOVERED, COUNTRY, COVID_CASES_STATS_FILE, COVID_SAFETY_MEASURES_FILE,
                        MEASURE, TOTAL_DEATHS)


class CovidData:
    def __init__(self, total_cases, total_recovered, total_deaths, country):
        self.total_cases = total_cases
        self.total_recovered = total_recovered
        self.total_deaths = total_deaths
        self.country = country
        self.measures = []


class SafetyMeasure:
    def __init__(self, measure, country):
        self.measure = measure
        self.countries = [country]
        self.count = 0


class FileParser:
    @staticmethod
    def fetch_covid_cases_stats(file_path):
        covid_records = []
        with open(Path(file_path) / COVID_CASES_STATS_FILE, 'rt') as covid_cases_stats:
            covid_cases_stats_records = csv.DictReader(covid_cases_stats)

            for record in covid_cases_stats_records:
                total_cases = record[TOTAL_CASES]
                total_recovered = record[TOTAL_RECOVERED]
                total_deaths = record[TOTAL_DEATHS]
                country = record[COUNTRY]

                if all([total_cases, total_recovered, total_deaths, country]):
                    covid_records.append(CovidData(
                        total_cases=total_cases,
                        total_recovered=total_recovered,
                        total_deaths=total_deaths,
                        country=country
                    ))

        return covid_records

    @staticmethod
    def fetch_covid_safety_measures(covid_records, file_path):
        measures = []
        with open(Path(file_path) / COVID_SAFETY_MEASURES_FILE, 'rt') as covid_safety_measures:
            covid_safety_measures_records = csv.DictReader(covid_safety_measures)

            for record in covid_safety_measures_records:
                measure = record[MEASURE]
                country = record[country]
                is_measure_updated = False
                for i in range(len(measures)):
                    if measures[i].measure == measure:
                        measures[i].countries.append(country)
                        measures[i].count += 1
                        is_measure_updated = True

                if is_measure_updated:
                    measures.append(SafetyMeasure(measure=measure, country=country))

                if all([country, measure]):
                    covid_record = next((record for record in covid_records if record.country == country), None)
                    covid_record.measures.append(measure)

        return covid_records
