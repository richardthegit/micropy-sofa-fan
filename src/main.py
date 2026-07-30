import asyncio
from machine import Pin, PWM

from rb.core import duty, PowerSource
from rb.core.richtext import rt
from rb.core.store import store
from rb.dev.ahtx0 import new_soft_aht20, dew_point
from rb.dev.buttons import fake_gnd_pushbutton
from rb.dev.display import Display

from screens import Screens


class Btn:
    def __init__(self, pin1, pin2, total_states = 3):
        btn = fake_gnd_pushbutton(pin1, pin2)
        btn.press_func(self.button_pressed)

        self.state = store.get('state', 0)
        self.total_states = total_states

    def button_pressed(self):
        self.state += 1
        if self.state >= self.total_states:
            self.state = 0
        store.set('state', self.state)


class Sensor:
    def __init__(self, vcc = 2, gnd = 4, scl = 5, sda = 3):
        self.sensor_pwr = PowerSource(vcc_pin = vcc, gnd_pin = gnd)
        self.sensor = new_soft_aht20(scl = scl, sda = sda)
        self.temp = round(self.sensor.temperature)
        self.rh = round(self.sensor.relative_humidity)
        self.dew_point = dew_point(self.temp, self.rh)

    async def run(self):
        state = 0
        while True:
            # We don't update both states at one as it takes a while for each.
            state += 1
            if state % 2:
                self.temp = round(self.sensor.temperature)
            else:
                self.rh = round(self.sensor.relative_humidity)

            self.dew_point = dew_point(self.temp, self.rh)

            await asyncio.sleep(1) 


async def main():
    display = Display(scl = 7, sda = 6, driver = 'ssd1306')
    sensor = Sensor()
    screens = Screens(display, sensor)
    btn = Btn(8, 9)
    fan_pwm = PWM(Pin(8), freq = 25000, duty_u16 = 0)

    asyncio.create_task(sensor.run())

    while True:
        screens.main(btn.state)
        await asyncio.sleep_ms(10)


if __name__ == '__main__':
    asyncio.run(main())
