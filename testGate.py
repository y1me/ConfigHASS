#!/usr/bin/python3

import time
from mcp2210 import Mcp2210, Mcp2210GpioDesignation, Mcp2210GpioDirection
mcp = Mcp2210(serial_number="0000406445")
print("Set GPIO")
for i in range(2):
    print(i)
    mcp.set_gpio_designation(i, Mcp2210GpioDesignation.GPIO)
print("Set GPIO direction")
for i in range(2):
    print(i)
    mcp.set_gpio_direction(i, Mcp2210GpioDirection.OUTPUT)

mcp.set_gpio_output_value(0, False)
mcp.set_gpio_output_value(1, False)
time.sleep(3)
print("Power on remote")
mcp.set_gpio_output_value(0, True)
time.sleep(3)
print("Send opening gate signal")
mcp.set_gpio_output_value(1, True)
time.sleep(4)
mcp.set_gpio_output_value(1, False)
time.sleep(3)
print("Send opening gate signal")
mcp.set_gpio_output_value(1, True)
time.sleep(4)
mcp.set_gpio_output_value(1, False)
time.sleep(3)
#print("Send opening gate signal")
#mcp.set_gpio_output_value(1, True)
#time.sleep(4)
#mcp.set_gpio_output_value(1, False)
print("Power off remote")
mcp.set_gpio_output_value(0, False)
