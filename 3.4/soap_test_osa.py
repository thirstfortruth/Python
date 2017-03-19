import osa
import math

URL_DISTANCE = 'http://www.webservicex.net/length.asmx?WSDL'
URL_TEMPERATURE = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
URL_CURRENCY = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
FILES = {'CURRENCY_FILE': './data/currencies.txt', 'TEMPERATURE_FILE': './data/temps.txt', 'DISTANCE_FILE': './data/travel.txt'}


def convert_temperature(temp_value, from_temp, to_temp):
    try:
        client = osa.Client(URL_TEMPERATURE)
        response_temp = client.service.ConvertTemp(Temperature=temp_value,
                                              FromUnit=from_temp,
                                              ToUnit=to_temp)
        return response_temp
    except:
        print('ERROR: can\'t convert temperature')
        print('Available temperature units are:'
              'degreeCelsius or degreeFahrenheit or degreeRankine or degreeReaumur or kelvin')


def convert_distance(value, from_length_unit, to_length_unit):
    try:
        client = osa.Client(URL_DISTANCE)
        response_dist = client.service.ChangeLengthUnit(LengthValue=value,
                                                   fromLengthUnit=from_length_unit,
                                                   toLengthUnit=to_length_unit)
        return response_dist
    except:
        print('ERROR: can\'t convert distance')
        print('Available distance units are:'
              'Angstroms or Nanometers or Microinch or Microns or Mils or Millimeters or Centimeters or Inches or Links '
              'or Spans or Feet or Cubits or Varas or Yards or Meters or Fathoms or Rods or Chains or Furlongs '
              'or Cablelengths or Kilometers or Miles or Nauticalmile or League or Nauticalleague')


def convert_currency(amount, from_currency, to_currency):
    try:
        client = osa.Client(URL_CURRENCY)
        response_cur = client.service.ConvertToNum(fromCurrency=from_currency,
                                               toCurrency=to_currency,
                                               amount=amount,
                                               rounding=True)
        return response_cur
    except:
        client = osa.Client(URL_CURRENCY)
        currencies = client.service.Currencies()
        print('ERROR: failed converting currencies. Available currencies are:')
        print(currencies.replace(';', ', '))


def open_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()


def parse_currencies(list_of_lines):
    result_pairs = []
    for line in list_of_lines:
        currency_info = line.split(':')[1].strip().split(' ')
        amount, currency = currency_info[0], currency_info[1]
        result_pairs.append({'AMOUNT': amount, 'CURRENCY': currency})
    return result_pairs


def parse_temperature(list_of_lines):
    result_temps = []
    for line in list_of_lines:
        result_temps.append(float(line.split(' ')[0]))
    return result_temps


def parse_distances(list_of_lines):
    result_distances = []
    for line in list_of_lines:
        result_distances.append(line.split(':')[1].strip().split(' ')[0].replace(',', ''))
    return result_distances

# print('Convert temperature:', convert_temperature(10, 'degreeFahrenheit', 'degreeCelsius'))
# print('Convert distance:', convert_distance(10, 'Feet', 'Meters'))
# print('Convert currency:', convert_currency(10, 'EU', 'RUB'))

# Sub-task 1
lines_temp = open_file(FILES['TEMPERATURE_FILE'])
temperatures = parse_temperature(lines_temp)
print('Sub-task 1. Average week temperature (Celsius degree):',
      convert_temperature(sum(temperatures)/len(temperatures),
                          'degreeFahrenheit',
                          'degreeCelsius'))

# Sub-task 2
lines_cur = open_file(FILES['CURRENCY_FILE'])
currencies = parse_currencies(lines_cur)
print('Sub-task 2. Total money spent (RUB):',
      math.ceil(sum([convert_currency(x['AMOUNT'], x['CURRENCY'], 'RUB') for x in currencies])))

# Sub-task 3
lines_dist = open_file(FILES['DISTANCE_FILE'])
distances = parse_distances(lines_dist)
print('Sub-task 3. Overall distance passed (km):',
      round(sum([convert_distance(x, 'Miles', 'Kilometers') for x in distances]), 2))

