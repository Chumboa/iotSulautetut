from machine import Pin, I2C, ADC
from utime import sleep
from ssd1306 import SSD1306_I2C
from dht20 import DHT20

class EnvironmentSensorSystem:
    ADC_FULL_SCALE = 65535
    VOLTAGE_REF = 3.3
    TEMP_SENSOR_OFFSET = 0.4
    TEMP_SENSOR_SCALE = 0.0195

    def __init__(self):
        self.setup_hardware()
        self.init_display()
        self.init_leds()

    def setup_hardware(self):
        self.i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=400000)
        self.adc_temp = ADC(Pin(28))
        self.adc_potentiometer = ADC(Pin(27))
        self.dht20 = DHT20(0x38, self.i2c)

    def init_display(self):
        self.oled = SSD1306_I2C(128, 64, self.i2c, addr=0x3C)
        self.oled.fill(0)
        self.oled.show()

    def init_leds(self):
        self.leds = {
            'gp14': Pin(14, Pin.OUT),
            'gp15': Pin(15, Pin.OUT),
            'red': Pin(12, Pin.OUT),
            'green': Pin(13, Pin.OUT),
        }

    def read_environment(self):
        try:
            measurements = self.dht20.measurements
            temperature = measurements['t']
            humidity = measurements['rh']
            print(f"Read temperature: {temperature} C, humidity: {humidity} %")
        except Exception as e:
            print(f"Sensor read error: {e}")
            temperature, humidity = None, None  

        pot_value = self.adc_potentiometer.read_u16()
        pot_percentage = (pot_value / self.ADC_FULL_SCALE) * 100

        temperature_threshold = 20 + (pot_percentage / 100) * 10  
        humidity_threshold = 30 + (pot_percentage / 100) * 70     
        
        print(f"Temp threshold: {temperature_threshold} C, Humidity threshold: {humidity_threshold} %")
        adc_temp_value = self.adc_temp.read_u16()
        analog_temperature = self.calculate_analog_temperature(adc_temp_value)

        return temperature, humidity, temperature_threshold, humidity_threshold, analog_temperature

    def calculate_analog_temperature(self, adc_value):
        voltage = (adc_value / self.ADC_FULL_SCALE) * self.VOLTAGE_REF
        return ((voltage - self.TEMP_SENSOR_OFFSET) / self.TEMP_SENSOR_SCALE) if voltage >= 0.4 else None

    def update_display(self, temperature, humidity, temperature_threshold, humidity_threshold, analog_temp):
        lines = [
            f'Temp: {temperature:.1f}C' if temperature is not None else 'Temp: Error',
            f'Humidity: {humidity:.1f}%' if humidity is not None else 'Humidity: Error',
            f'A Temp: {analog_temp:.1f}C' if analog_temp is not None else 'A Temp: Error',
            f'LED t: {temperature_threshold:.1f}C',  
            f'LED h: {humidity_threshold:.1f}%'     
        ]
        self.oled.fill(0)
        for i, line in enumerate(lines):
            self.oled.text(line, 0, i * 10)
        self.oled.show()

    def update_leds(self, temperature, humidity, temperature_threshold, humidity_threshold):

        for led in self.leds.values():
            led.value(0)  

        if temperature is None or humidity is None:
            for led in self.leds.values():
                led.value(1)
        else:
            humidity_led = 'gp15' if humidity >= humidity_threshold else 'gp14'
            temperature_led = 'red' if temperature >= temperature_threshold else 'green'
            self.leds[humidity_led].value(1)
            self.leds[temperature_led].value(1)

    def run(self):
        while True:
            temperature, humidity, temperature_threshold, humidity_threshold, analog_temp = self.read_environment()
            self.update_display(temperature, humidity, temperature_threshold, humidity_threshold, analog_temp)
            self.update_leds(temperature, humidity, temperature_threshold, humidity_threshold)
            sleep(1)


system = EnvironmentSensorSystem()
system.run()

