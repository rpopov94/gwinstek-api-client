import pyvisa


class Gwinstek:
    """
    Gwinstek commands manager

    The gwinstek class describes how to
    work with the scpi protocol over
    tcp/ip with gwinstek power supplies
    of the GPP-1326/GPP-2323/GPP-3323/GPP-4323 series
    """

    def __init__(self, connection: str):
        """
        Constructor of gwinstek device
        :param device: reference of device
        """
        self.connection = connection
        self.device = None

    def __aenter__(self):
        rm = pyvisa.ResourceManager()
        self.device = rm.open_resource(self.connection)
        self.device.read_termination = '\n'
        self.device.write_termination = '\n'
        return self

    def __aexit__(self, *args, **kwargs):
        self.device.close()

    """ Source commands """

    async def set_current(self, channel: int, value: float | int):
        """
        Set current
        :param channel: number of channel
        :param value: current for channel
        :return: string
        """
        await self.device.query_async(
            "ISET{}:{:.4f}".format(channel, value)
        )

    async def set_voltage(self, channel: int, value: float | int):
        """
        Set voltage
        :param channel: number of channel
        :param value: voltage for channel
        :return: string
        """
        await self.device.query_async(
            "VSET{}:{:.3f}".format(channel, value)
        )

    """ Output commands """

    async def enable_channel(self, channel: int):
        """
        Enable channel
        :param channel: number of channel
        :return: string
        """
        await self.device.query_async(
            ":OUTPut{}:STATe ON".format(channel)
        )

    async def disable_channel(self, channel: int):
        """
        Disable channel №
        :param channel: number of channel
        :return: string
        """
        await self.device.query_async(
            ":OUTPut{}:STATe OFF".format(channel)
        )

    async def enable_all_channels(self):
        """
        Enable all channels
        :return: string
        """
        await self.device.query_async("ALLOUTON")

    async def disable_all_channels(self):
        """
        Disable all channels
        :return: string
        """
        await self.device.query_async("ALLOUTOFF")

    """ Measurement commands """

    async def get_telemetry(self):
        """
        Get channel's state (current, voltage, power)
        :param channel: number of channel
        :return: string
        """
        return await self.device.read_async(":MEASure:ALL?")

    async def get_power(self, channel: int):
        """
        Get channel power
        :param channel: number of channel
        :return: string
        """
        return await self.device.read_async(
            ":MEASure{}:POWEr?".format(channel)
        )

    async def get_voltage(self, channel: int):
        """
        Get channel voltage
        :param channel: number of channel
        :return: string
        """
        return await self.device.read_async(
            ":MEASure{}:VOLTage?".format(channel)
        )

    async def get_current(self, channel: int):
        """
        Get channel current
        :param channel: number of channel
        :return: string
        """
        return await self.device.read_async(
            ":MEASure{}:CURRent?".format(channel)
        )
