#!/usr/bin/python3
import rpI2C

INDENT = '  '

address = 0x60
bus = rpI2C.I2C(address)

print("reading data at address {%h}".format(address))
data = bus.read_raw_byte()
print(INDENT + "found {%h}".format(data))
#bus.write_raw_byte(0x00)
bus.clean_up()