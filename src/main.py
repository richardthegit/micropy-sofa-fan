import time

from rb.core import PowerSource
from rb.core.richtext import rt
from rb.dev.ahtx0 import new_soft_aht20
from rb.dev.display import Display, DisplayContext

display = Display(scl = 7, sda = 6, driver = 'ssd1306')
sensor_pwr = PowerSource(vcc_pin = 2, gnd_pin = 4)
th_sensor = new_soft_aht20(scl = 5, sda = 3)

while True:
    with DisplayContext(display):
        display.text(f'{th_sensor.temperature} degrees', 0, 0)
        display.text(f'{th_sensor.relative_humidity} %', 0, 12)

    time.sleep(1)