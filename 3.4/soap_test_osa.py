import osa

URL_DISTANCE = 'http://www.webservicex.net/length.asmx?WSDL'
URL_TEMPERATURE = 'http://www.webservicex.net/ConvertTemperature.asmx?WSDL'
URL_CURRENCY = 'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL'
FILES = ['currencies.txt', 'temps.txt', 'travel.txt']


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


print('Convert temperature:', convert_temperature(10, 'degreeFahrenheit', 'degreeCelsius'))
print('Convert distance:', convert_distance(10, 'Feet', 'Meters'))
print('Convert currency:', convert_currency(10, 'EU', 'RUB'))
