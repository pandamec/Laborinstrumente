class attoDryControl:
    """Indirect control of the AttoDry800 during heating and cooling down, for sample and cold plate."""

    def __init__(self, Atto, ControlMode,):

        self.Atto= Atto                     # Class provided by Attocube
        self.ControlMode=ControlMode        #1 Sample Plate #2 Sample Plate and Cold Plate
        self.t_limitColdPlate = 0.5 * 3600   # Max time in seconds to reach a constant temperature at cold plate Changed due to the experiment on 21.10.25 from 1 to 0.5.
        self.t_limitSamplePlate = 0.75 * 3600  # Max time in seconds to reach a constant temperature at sample plate, Changed due to the experiment on 21.10.25 from 1.5 to 0.75
        self.dTds_limit=0.001                   # Max gradient of temperature w.r.t time in K/s considered to be constant at the sample plate during Heating up
        self.CoolingRateColdPlate = [(300, 0.005),  # Added after the first measurement
                                (15, 0.002),

                                ]

        self.CoolingRateSamplePlate = [(300, 0.002),
                                  (15, 0.001),

    def getCoolingRateLimitColdPlate(self,T):

        for i in self.CoolingRateColdPlate:

            if T <= i[0]:
                Range = i[1]

        return Range

    def getCoolingRateLimitSample(self,T):

        for i in self.CoolingRateSample:

            if T <= i[0]:
                Range = i[1]

        return Range


    def getcoolingrateSample(t):
        """Compute the cooling rate in a  determined delta time t"""
        TS1 = Atto.sample.getTemperature()
        time.sleep(t)
        TS2 = Atto.sample.getTemperature()

        dTds = (TS2 - TS1) / t

        return dTds

    def getcoolingrateExchange(t):
        """Compute the cooling rate in a  determined delta time t"""
        TS1 = Atto.exchange.getTemperature()
        time.sleep(t)
        TS2 = Atto.exchange.getTemperature()

        dTds = (TS2 - TS1) / t

        return dTds

    def startControl(self,T, T_target):
        """Start the temperature control"""

        Atto.sample.startTempControl()
        Atto.sample.setSetPoint(T)

        if self.ControlMode == 2:
            Atto.exchange.setSetPoint(T - computeColdplateTemperature(T))  # Previously coldplate directly -20 wrt the set temperature. this created an oscillation on the sample temperature value after 10min
            Atto.exchange.startTempControl()

    def stopControl(self):
        """Stop the temperature control"""
        Atto.sample.stopTempControl()
        if self.ControlMode == 2:
            Atto.exchange.stopTempControl()

    def startControlExchange(T):
        """Start the temperature control"""

        Atto.exchange.setSetPoint(T)  # Previously coldplate directly -20 wrt the set temperature. this created an oscillation on the sample temperature value after 10min
        Atto.exchange.startTempControl()

    def startControl(self,T):
        """Start the temperature control"""

        Atto.sample.startTempControl()
        Atto.sample.setSetPoint(Temperature)
        if self.ControlMode == 2:
            Atto.exchange.setSetPoint(T - computeColdplateTemperature(T))  # Previously coldplate directly -20 wrt the set temperature. this created an oscillation on the sample temperature value after 10min
            Atto.exchange.startTempControl()


    def performApproachHeating(self, T_target):

        while n_dTds < 10:

            startControl( T_target)
            dTds = getcoolingrate(2)
            Ts = Atto.sample.getTemperature()
            Delta = T_targetSample - Ts

            print("Target T- Current T: ", Delta)

            if abs(dTds) <= self.dTds_limit:
                n_dTds = n_dTds + 1

    def performApproachCooling(self, T_target):

        dTds = getcoolingrateExchange(1)  # Time step 1s
        T_targetSample = T_target
        T_target = T_target - computeColdplateTemperature(T_target)
        Ts = Atto.exchange.getTemperature()
        Delta = T_target - Ts

        print("performing an approach")
        print("Target value at Cold Plate", T_target)

        count = 0
        n_dTds = 0

        while n_dTds < 5 and count <= self.t_limitColdPlate:

            if 1 < -Delta <= 10:
                    T_set = T_target + dTds * -30

            elif 0.01 < -Delta <= 1:
                    T_set = T_target + dTds * -20

            elif -Delta <= 0.01:
                    T_set = T_target + dTds * -10
            else:
                    T_set = T_target

            print("Target T at Cold Plate", T_set)
            print("Coolingrate ColdPlate: ", dTds)

            startControlExchange(T_set)
            startControl(T_targetSample, T_targetSample)

            LimitColdPlate = getCoolingRateLimitColdPlate(self,T_target)
            print("Coolingrate Limit ColdPlate: ", LimitColdPlate)
            if Ts < 296 and abs(dTds) <= LimitColdPlate:
                    n_dTds = n_dTds + 1

            dTds = getcoolingrateExchange(2)
            Ts = Atto.exchange.getTemperature()
            Delta = T_target - Ts
            print("Target T- Current T at Cold Plate: ", Delta)
            count = count + 1
        startControlExchange(T_target)

        print("Approach finished at Cold Plate")
        n_dTds = 0

        while n_dTds < 10 and count <= self.t_limitSamplePlate:

            startControl(T_targetSample, T_targetSample)

            dTds_Sample = getcoolingrate(2)
            print("Coolingrate SamplePlate: ", dTds_Sample)

            LimitSample = getCoolingRateLimitSample(T_targetSample, CoolingRateSamplePlate)
            print("Coolingrate Limit SamplePlate: ", LimitSample)

            if abs(dTds_Sample) <= LimitSample:
                 n_dTds = n_dTds + 1
            count = count + 1


    def performApproach(self, T_target):
        """Perform an approach to the set temperature value. The transition should be smooth close to the set temperature value"""

        if self.ControlMode == 1: #Heating
            performApproachHeating(T_target)
            print("Approach finished at Sample Plate")

        elif self.ControlMode==2: #Cooling down
            performApproachCooling(T_target)
            print("Approach finished at Sample ad Cold Plate")
