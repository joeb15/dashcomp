import obd
import sys
from classes import Variables, OBD

if not 'jeep_vars' in sys.modules.keys():
    sys.modules['jeep_vars'] = Variables()
variables = sys.modules['jeep_vars']

variables.obd = OBD()
variables.obd.connection = None
variables.obd.speed=None
variables.obd.fuel_rate=None
variables.obd.fuel_type=None
variables.obd.ethanol_percent=None


def update_vars():
    speed = variables.obd.connection.query(obd.commands.SPEED)
    if not speed.is_null():
        variables.obd.speed = speed.value.to('mph').magnitude

    fuel_rate = variables.obd.connection.query(obd.commands.FUEL_RATE)
    if not fuel_rate.is_null():
        variables.obd.fuel_rate = fuel_rate.value

    fuel_type = variables.obd.connection.query(obd.commands.FUEL_TYPE)
    if not fuel_type.is_null():
        variables.obd.fuel_type = fuel_type.value

    ethanol_percent = variables.obd.connection.query(obd.commands.ETHANOL_PERCENT)
    if not ethanol_percent.is_null():
        variables.obd.ethanol_percent = ethanol_percent.value

    error_codes = variables.obd.connection.query(obd.commands.GET_DTC)
    """
    response.value = [
        ("P0104", "Mass or Volume Air Flow Circuit Intermittent"),
        ("B0003", ""), # unknown error code, it's probably vehicle-specific
        ("C0123", "")
    ]
    """
    if not error_codes.is_null():
        variables.obd.error_codes = error_codes.value


def setup():
    variables.obd.connection = obd.Async(portstr='COM3', baudrate=9600)
    if variables.obd.connection.supports(obd.commands.SPEED):
        variables.obd.connection.watch(obd.commands.SPEED)

    if variables.obd.connection.supports(obd.commands.FUEL_RATE):
        variables.obd.connection.watch(obd.commands.FUEL_RATE)

    if variables.obd.connection.supports(obd.commands.FUEL_TYPE):
        variables.obd.connection.watch(obd.commands.FUEL_TYPE)

    if variables.obd.connection.supports(obd.commands.ETHANOL_PERCENT):
        variables.obd.connection.watch(obd.commands.ETHANOL_PERCENT)

    variables.obd.connection.start()

    if variables.obd.connection.status() == obd.OBDStatus.NOT_CONNECTED:
        print('Unable to connect to the OBD adapter, try disconnecting and reconnecting the USB adapter.')
        return

    variables.obd.elm_version = variables.obd.connection.query(obd.commands.ELM_VERSION).value
    variables.obd.elm_voltage = variables.obd.connection.query(obd.commands.ELM_VOLTAGE).value
    print('ELM Adapter loaded. Detected ELM version %s with connected voltage of %s' % (variables.obd.elm_version,
                                                                                        variables.obd.elm_voltage))

    if variables.obd.connection.status() == obd.OBDStatus.ELM_CONNECTED:
        print('Unable to establish a link to the car, try disconnecting and reconnecting the OBD port.')
        return

    print('Successfully connected to car')



def close():
    if variables.obd.connection is not None:
        variables.obd.connection.stop()


setup()
update_vars()
close()
