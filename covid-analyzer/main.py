from .argument_parser import ArgumentParser
from .calculator import Calculator
from .file_reader import FileParser


def main():
    args = ArgumentParser.parse_arguments()
    covid_records = FileParser.fetch_covid_cases_stats(args.file_path)
    safety_measures = FileParser.fetch_covid_safety_measures(covid_records, args.file_path)
    calculator = Calculator(covid_records=covid_records, safety_measure_records=safety_measures)

    if args.a:
        print('Recover over total ratio is {}'.format(calculator.get_recovered_over_total_ratio(args.a)))

    if args.b:
        print('Death Average is {}'.format(calculator.get_death_average(args.b)))

    if args.c:
        measures = calculator.get_safety_measures_efficiency()
        for measure in measures:
            print('measure: {} efficiency: {}'.format(measure.measure, measure.efficiency))
    if args.d:
        calculator.plot_measure_efficiency()


if __name__ == 'main':
    main()
