
# bus is an instance of SMBus
# default is little endian

class reader(object):
    """
    Wraps a I2C SMBus instance to provide methods for reading
    signed/unsigned bytes and 16-bit words
    """
    def __init__(self, bus, address):
        self._bus = bus
        self._address = address

    def unsigned_short(self, register):
        self._bus.read_word_data(self._address, register) & 0xffff

    def signed_short(self, register):
        word = self.unsigned_short(register)
        return word if word < 0x8000 else word - 0x10000

    def unsigned_byte(self, register):
        self._bus.read_byte_data(self._address, register) & 0xff

    def signed_byte(self, register):
        byte = self.unsigned_byte(register) & 0xff
        return byte if byte < 0x80 else byte - 0x100
