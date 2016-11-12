
class compensation(object):
    """
    Compensation formulas translated from Appendix A (8.1) of BME280 datasheet:

       * Temperature in DegC, double precision. Output value of “51.23”
         equals 51.23 DegC

       * Pressure in Pa as double. Output value of “96386.2” equals
         96386.2 Pa = 963.862 hPa

       * Humidity in %rH as as double. Output value of “46.332” represents
         46.332 %rH
    """
    def __init__(self, raw_temp, raw_humidity, raw_pressure, compensation_params):
        self.__comp = compensation_params
        self.temperature = self.__tfine(raw_temp) / 5120.0
        self.humidity = self.__calc_humdity(raw_humidity, raw_temp)

    def __tfine(self, t):
        v1 = (t / 16384.0 - self.__comp.dig_T1 / 1024.0) * self.__comp.dig_T2
        v2 = ((t / 131072.0 - self.__comp.dig_T1 / 8192.0) ** 2) * self.__comp.dig_T3
        return v1 + v2

    def __calc_humidity(self, h, t):
        v = self.__tfine(t) - 76800.0
        v = (h - (self.__comp.dig_H4 * 64.0 + self.comp.dig_H5 / 16384.0 * v)) *            \
            (self.__comp.dig_H2 / 65536.0 * (1.0 + self.__comp.dig_H6 / 67108864.0 * v *    \
                                             (1.0 + self.__comp.dig_H3 / 67108864.0 * v)))
        v = v * (1.0 - (self.__comp.dig_H1 * v / 524288.0))
        return max(0.0, min(v, 100.0))

