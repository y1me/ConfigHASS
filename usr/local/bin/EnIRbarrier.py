#!/usr/bin/python3

import time
import os.path
from mcp2210 import Mcp2210, Mcp2210GpioDesignation, Mcp2210GpioDirection
mcp = Mcp2210(serial_number="0000406445")
# GPIO 0 : 5V power control
# GPIO 1 : Emit open gate signal 
# GPIO 2 : control relay 2 
# GPIO 3 : control relay 1 
# GPIO 5 : control relay 3 
# GPIO 6 : control relay 4 
POWER=0
REMOTE=1
RELAY1=3
RELAY2=2
RELAY3=5
RELAY4=6

IRBARRIER="/tmp/IrBarrier"




print("Set GPIO")
mcp.set_gpio_designation(POWER, Mcp2210GpioDesignation.GPIO)
mcp.set_gpio_designation(REMOTE, Mcp2210GpioDesignation.GPIO)
mcp.set_gpio_designation(RELAY1, Mcp2210GpioDesignation.GPIO)
mcp.set_gpio_designation(RELAY2, Mcp2210GpioDesignation.GPIO)
mcp.set_gpio_designation(RELAY3, Mcp2210GpioDesignation.GPIO)
mcp.set_gpio_designation(RELAY4, Mcp2210GpioDesignation.GPIO)
print("Set GPIO direction")
mcp.set_gpio_direction(POWER, Mcp2210GpioDirection.OUTPUT)
mcp.set_gpio_direction(REMOTE, Mcp2210GpioDirection.OUTPUT)
mcp.set_gpio_direction(RELAY1, Mcp2210GpioDirection.OUTPUT)
mcp.set_gpio_direction(RELAY2, Mcp2210GpioDirection.OUTPUT)
mcp.set_gpio_direction(RELAY3, Mcp2210GpioDirection.OUTPUT)
mcp.set_gpio_direction(RELAY4, Mcp2210GpioDirection.OUTPUT)

mcp.set_gpio_output_value(POWER, False)
mcp.set_gpio_output_value(REMOTE, False)
mcp.set_gpio_output_value(RELAY1, True)
mcp.set_gpio_output_value(RELAY2, True)
mcp.set_gpio_output_value(RELAY3, True)
mcp.set_gpio_output_value(RELAY4, True)
#time.sleep(3)
print("Power on")
mcp.set_gpio_output_value(POWER, True)
time.sleep(0.5)
mcp.set_gpio_output_value(RELAY2, False)
f= open(IRBARRIER,"w+")
f.close()
exit(0)
