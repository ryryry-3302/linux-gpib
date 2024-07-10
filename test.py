import pyvisa
rm = pyvisa.ResourceManager()
print(rm.list_resources())
print((rm.open_resource('GPIB0::11::INSTR')).query('*IDN?'))

