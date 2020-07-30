#!/usr/bin/python3
import rpI2C

INDENT = '  '

chip_address = 0x60
register_address = 0x03
bus = rpI2C.I2C(chip_address)

print("reading data from chip {:02X}, register {:02X}"
  .format(chip_address, register_address))
#data = bus.read_raw_byte()
data = bus.read_unsigned_byte(register_address)
print(INDENT + "found {:02X}".format(data))
#bus.write_raw_byte(0x00)
bus.clean_up()