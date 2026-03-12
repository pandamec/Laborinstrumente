import time
import numpy as np

class attoDryControl:
    """Indirect control of the AttoDry800 during heating and cooling down, for sample and cold plate."""

    def __init__(self, Atto, ControlMode,AttoMode):

        self.AttoMode=AttoMode              #1 Heating #2 Cooling
        self.Atto= Atto                     # Class provided by Attocube
        self.ControlMode=ControlMode        #1 Sample Plate #2 Sample Plate and Cold Plate
        self.t_limitColdPlate = 0.5 * 3600   # Max time in seconds to reach a constant temperature at cold plate Changed due to the experiment on 21.10.25 from 1 to 0.5.
        self.t_limitSamplePlate = 0.75 * 3600  # Max time in seconds to reach a constant temperature at sample plate, Changed due to the experiment on 21.10.25 from 1.5 to 0.75
        self.dTds_limit=0.001                   # Max gradient of temperature w.r.t time in K/s considered to be constant at the sample plate during Heating up
        self.CoolingRateColdPlate = [(300, 0.005),  # Added after the first measurement
                                (15, 0.002)]

        self.CoolingRateSamplePlate = [(300, 0.002),
                                  (15, 0.001)]

    def computeColdplateTemperature(self,T):
        """Set the minimum delta required between the sample and coldplate based september 25 measurement"""
        ## von Oyuka bis 250917 Heizung 1
        if 75 < T <= 300:
            delta = 10
        elif 50 < T <= 75:
            delta = 15
        elif 25 < T <= 50:
            delta = 10
        elif 10 < T <= 25:
            delta = 5
        elif T <= 10:  # After Oyukasexperiment.
            delta = T - 3

        return delta

    def getCoolingRateLimitColdPlate(self,T):

        for i in self.CoolingRateColdPlate:

            if T <= i[0]:
                Range = i[1]

        return Range

    def getCoolingRateLimitSample(self,T):

        for i in self.CoolingRateSamplePlate:

            if T <= i[0]:
                Range = i[1]

        return Range


    def getcoolingrateSample(self,seconds):
        """Compute the cooling rate in a  determined delta time t"""
        TS1 = self.Atto.sample.getTemperature()
        time.sleep(seconds)
        TS2 = self.Atto.sample.getTemperature()

        dTds = (TS2 - TS1) / seconds

        return dTds

    def getcoolingrateExchange(self,seconds):
        """Compute the cooling rate in a  determined delta time t"""
        TS1 = self.Atto.exchange.getTemperature()
        time.sleep(seconds)
        TS2 = self.Atto.exchange.getTemperature()

        dTds = (TS2 - TS1) / seconds

        return dTds

    def stopControl(self):
        """Stop the temperature control"""
        self.Atto.sample.stopTempControl()
        if self.ControlMode == 2:
            self.Atto.exchange.stopTempControl()

    def startControlExchange(self,T):
        """Start the temperature control"""

        self.Atto.exchange.setSetPoint(T)  # Previously coldplate directly -20 wrt the set temperature. this created an oscillation on the sample temperature value after 10min
        self.Atto.exchange.startTempControl()

    def startControl(self,T):
        """Start the temperature control"""

        self.Atto.sample.startTempControl()
        self.Atto.sample.setSetPoint(T)
        if self.ControlMode == 2:
            self.Atto.exchange.setSetPoint(T - self.computeColdplateTemperature(T))  # Previously coldplate directly -20 wrt the set temperature. this created an oscillation on the sample temperature value after 10min
            self.Atto.exchange.startTempControl()


    def performApproachHeating(self, T_targetSample):
        """Perform an approach during heating. After testing, a constant value at sample plate includes also a constant value at cold plate"""
        n_dTds=0
        while n_dTds < 10:

            self.startControl(T_targetSample)
            dTds = self.getcoolingrateSample(2)
            Ts = self.Atto.sample.getTemperature()
            Delta = T_targetSample - Ts

            print("dT at Sample Plate: ", Delta)
            print("\n")
            if abs(dTds) <= self.dTds_limit:
                n_dTds = n_dTds + 1

    def performApproachCooling(self, T_targetSample):
        """Perform an approach during cooling down. After testing, a constant value at cold plate must be reached first. Then a constant value at sample plate can be reached"""

        dTds = self.getcoolingrateExchange(1)  # Time step 1s
        T_targetColdPlate = T_targetSample - self.computeColdplateTemperature(T_targetSample)
        Tc = self.Atto.exchange.getTemperature()
        Delta = T_targetColdPlate - Tc

        #print("Target value at Cold Plate", T_targetColdPlate)

        count = 0
        n_dTds = 0

        while n_dTds < 5 and count <= self.t_limitColdPlate:

            if 1 < -Delta <= 10:
                    T_set = T_targetColdPlate + dTds * -30

            elif 0.01 < -Delta <= 1:
                    T_set = T_targetColdPlate + dTds * -20

            elif -Delta <= 0.01:
                    T_set = T_targetColdPlate + dTds * -10
            else:
                    T_set = T_targetColdPlate

            print("Target T at Cold Plate", T_set)
            print("Cooling rate ColdPlate: ", dTds)

            self.startControlExchange(T_set)
            self.startControl(T_targetSample)

            LimitColdPlate = self.getCoolingRateLimitColdPlate(T_targetColdPlate)
            print("Cooling rate Limit ColdPlate: ", LimitColdPlate)
            if Tc < 296 and abs(dTds) <= LimitColdPlate:
                    n_dTds = n_dTds + 1

            dTds = self.getcoolingrateExchange(2)
            Tc = self.Atto.exchange.getTemperature()
            Delta = T_targetColdPlate - Tc
            print("dT at Cold Plate: ", Delta)
            print("\n")
            count = count + 1
        self.startControlExchange(T_targetColdPlate)

        print("Approach finished at Cold Plate")
        n_dTds = 0

        while n_dTds < 10 and count <= self.t_limitSamplePlate:

            self.startControl(T_targetSample, T_targetSample)

            dTds_Sample = self.getcoolingrateSample(2)
            print("Cooling rate SamplePlate: ", dTds_Sample)

            LimitSample = self.getCoolingRateLimitSample(T_targetSample)
            print("Cooling rate Limit SamplePlate: ", LimitSample)
            print("\n")
            if abs(dTds_Sample) <= LimitSample:
                 n_dTds = n_dTds + 1
            count = count + 1


    def performApproach(self, T_target):
        """Perform an approach to the set temperature value. The transition should be smooth close to the set temperature value"""

        if self.AttoMode == 1: #Heating
            print("Performing an Approach during Heating")
            self.performApproachHeating(T_target)
            print("Approach finished at Sample Plate")

        elif self.AttoMode==2: #Cooling down
            print("Performing an Approach during Cooling Down")
            self.performApproachCooling(T_target)
            print("Approach finished at Sample ad Cold Plate")
