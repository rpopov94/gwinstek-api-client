import logging
import pyvisa


class Gwinstek:
    """
    Gwinstek commands manager

    The gwinstek class describes how to
    work with the scpi protocol over
    tcp/ip with gwinstek power supplies
    of the GPP-1326/GPP-2323/GPP-3323/GPP-4323 series
    """

    def __init__(self, device: object):
        """
        Constructor of gwinstek device
        :param device: reference of device
        """
        self.__device = device
        self.logger = logging.getLogger(__name__)

    """ Source commands """

    async def set_current(self, channel: int, value: float):
        """
        Set current
        :param channel: number of channel
        :param value: current for channel
        :return: string
        """
        try:
            self.logger.info(f"Set {value} A for channel #{channel}")
            await self.__device.query_async(
                "ISET{}:{:.4f}".format(channel, value)
            )
        except pyvisa.errors.VisaIOError as e:
            self.logger.error(
                f"Error while setting current channel {channel}\n{e}")

    async def set_voltage(self, channel: int, value: float):
        """
        Set voltage
        :param channel: number of channel
        :param value: voltage for channel
        :return: string
        """
        try:
            self.logger.info(f"Set {value} V for channel #{channel}")
            await self.__device.query_async(
                "VSET{}:{:.3f}".format(channel, value)
            )
        except pyvisa.errors.VisaIOError as e:
            self.logger.error(f"Error while setting voltage: {e}\n{e}")

    """ Output commands """

    async def enable_channel(self, channel: int):
        """
        Enable channel
        :param channel: number of channel
        :return: string
        """
        try:
            self.logger.info(f"Enable channel #{channel}")
            await self.__device.query_async(
                ":OUTPut{}:STATe ON".format(channel)
            )
        except pyvisa.errors.VisaIOError as e:
            self.logger.error(f"Error enable channel #{channel}\n{e}")

    async def disable_channel(self, channel: int):
        """
        Disable channel №
        :param channel: number of channel
        :return: string
        """
        try:
            self.logger.info(f"Disable channel #{channel}")
            await self.__device.query_async(
                ":OUTPut{}:STATe OFF".format(channel)
            )
        except pyvisa.errors.VisaIOError as e:
            self.logger.error(f"Error disable channel #{channel}\n{e}")

    """ Measurement commands """

    async def get_telemetry(self):
        """
        Get channel's state (current, voltage, power)
        :param channel: number of channel
        :return: string type
            <Channel1 Voltage>, <Channel1 Current>, <Channel1 Power>,
            <Channel2 Voltage>, <Channel2 Current>, <Channel2 Power>,
            <Channel3 Voltage>, <Channel3 Current>, <Channel3 Power>,
            <Channel4 Voltage>, <Channel4 Current>, <Channel4 Power>
        """
        try:
            self.logger.info("Get telemetry")
            await self.__device.read_async(":MEASure:ALL?")
        except pyvisa.errors.VisaIOError as e:
            self.logger.error(f"Error while get telemetry\n{e}")

    # Another commands
    async def close(self):
        """ disconnect device """
        await self.__device.close()