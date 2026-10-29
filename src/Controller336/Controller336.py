from lakeshore import Model336
ip='192.168.1.7'
controller = Model336(ip_address = ip)

class device:
    def __init__(self,
                 channel_ColdPlate,
                   channel_FreeLength,
                   channel_RadShield,
                   channel_2ndStage):
        self.channel_ColdPlate=channel_ColdPlate
        self.channel_FreeLength=channel_FreeLength
        self.channel_RadShield=channel_RadShield
        self.channel_2ndStage=channel_2ndStage
        

    def getTemperature(self):
        T_ColdPlate= controller.get_kelvin_reading(self.channel_ColdPlate)
        T_FreeLength= controller.get_kelvin_reading(self.channel_FreeLength)
        T_RadShield= controller.get_kelvin_reading(self.channel_RadShield)
        T_2ndStage= controller.get_kelvin_reading(self.channel_2ndStage)
        
        return T_ColdPlate,T_FreeLength,T_RadShield,T_2ndStage

    def prepareHeaters(self):

        controller.set_heater_output_mode(2,
                                           controller.HeaterOutputMode.CLOSED_LOOP,
                                             controller.InputChannel.CHANNEL_A)

        controller.set_heater_output_mode(1,
                                           controller.HeaterOutputMode.CLOSED_LOOP,
                                             controller.InputChannel.CHANNEL_C)


    def startControlColdPlate(self,T):
        controller.set_control_setpoint(2,T)
        controller.set_heater_range(2, controller.HeaterRange.MEDIUM)
    
    def startControlRadShield(self,T):
        controller.set_control_setpoint(1,T)
        controller.set_heater_range(1, controller.HeaterRange.MEDIUM)

    def stopControl(self):
        controller.all_heaters_off()
