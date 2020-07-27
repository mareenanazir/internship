import plotly.express as px
import pandas as pd


class Calculator:
    def __init__(self, covid_records, safety_measure_records):
        self.covid_records = covid_records
        self.safety_measure_records = safety_measure_records

    def get_recovered_over_total_ratio(self, country):
        country_record = next((record for record in self.covid_records if record.country == country), None)
        if not country_record:
            raise Exception('Country not found!')
        return round(country_record.total_recovered / country_record.total_cases, 2)

    def get_death_average(self, measure):
        total_deaths = 0
        total_countries = 0
        for record in self.covid_records:
            if measure in record.measures:
                total_deaths += record.total_deaths
                total_countries += 1
        if not total_countries:
            raise Exception('Measure Not Found!')
        return round(total_deaths / total_countries, 2)

    def get_safety_measures_efficiency(self):
        self.safety_measure_records.sort(key=lambda x: x.count, reverse=True)
        top_five_measures = self.safety_measure_records[:5]
        measures_efficiency = []

        for measure in top_five_measures:
            efficiency = 0

            for country in measure.countries:
                country_record = next((record for record in self.covid_records if record.country == country), None)
                efficiency += country_record.total_deaths
            measures_efficiency.append({
                'measure': measure.measure,
                'efficiency': efficiency
            })

        return measures_efficiency

    def plot_measure_efficiency(self):
        figure = px.bar(pd.DataFrame(self.get_safety_measures_efficiency()), x='measure', y='efficiency')
        figure.show()

