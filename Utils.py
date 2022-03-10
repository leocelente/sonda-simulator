'''
Helper functions that don't have a good place yet
'''

def kelvin(celcius: float) -> float:
  '''
  Converts temperature from degrees Celcius to Kelvin 
  '''
  return celcius + 273.15


def celcius(kelvin: float) -> float:
  '''
  Converts temperature from Kelvin to degrees Celcius
  '''
  return kelvin - 273.15


