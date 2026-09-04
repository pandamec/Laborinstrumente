from lakeshore import Model336
ip='192.168.1.7'
controller = Model336(ip_address = ip)

class device:
    def __init__(self,
                 channel):
        self.channel=channel

    def getTemperature(self):
        T= controller.get_kelvin_reading(self.channel)

        return T



