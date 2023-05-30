import pyvisa
from .gwinstek import Gwinstek


global engine

async def init_device():
    """ init device """
    rm = pyvisa.ResourceManager()
    device = rm.open_resource('TCPIP0::169.254.129.17::1026::SOCKET')
    return Gwinstek(device)
