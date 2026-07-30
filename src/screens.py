from fonts import ezFBfont_helvR08_ascii_11
from fonts import ezFBfont_helvB18_num_24
from fonts.ezFBfont import ezFBfont

from rb.dev.display import DisplayContext

spinner = (
    (0, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
    (1, 2),
    (0, 2),
    (0, 1),
)

class Screens:
    def __init__(self, display, sensor):
        self.display = display
        self.sensor = sensor
        self.sml = ezFBfont(display.fb, ezFBfont_helvR08_ascii_11)
        self.big = ezFBfont(display.fb, ezFBfont_helvB18_num_24)
        self.spin_state = 0

    def main(self, fan_level):
        """
        The main screen shows current temps/humidity and fan speed.
        """
        sml, big, sensor = self.sml, self.big, self.sensor
        fb = self.display.fb

        with DisplayContext(self.display):
            x, y = 0, 0
            sml.write('Temp', x, y)
            big.write(f'{sensor.temp}°', x, y + 12)

            x, y = 64, 0
            sml.write('Dew', x, y, halign = 'center')
            big.write(f'{sensor.dew_point}°', x, y + 12, halign = 'center')

            x, y = 128, 64
            big.write(f'{sensor.rh}%', x, y, halign = 'right', valign = 'bottom')
            sml.write('R/H', x, y - 24, halign = 'right', valign = 'bottom')

            w, h = 20, 24
            y = 64 - h
            for x in range(3):
                fb.rect(x * (w + 4), y, w, h, 1, x <= fan_level) 

            # Draw the spinner.
            self.spin_state += fan_level + 1
            spin_len = len(spinner)
            spin_index = int(self.spin_state / 3) % spin_len

            # width, spacing
            w, s = 5, 7
            x, y = 128 - (s * 3), 0
            for i in range(spin_len):
                if i == spin_index or i == (spin_index + 4) % spin_len:
                    px, py = spinner[i]
                    fb.rect(x + (px * s), y + (py * s), w, w, 1, True)
