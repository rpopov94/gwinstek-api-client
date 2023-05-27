from fastapi import FastAPI

from gwinstek.gwinstek import Gwinstek

app = FastAPI()

device = Gwinstek(connection='TCPIP0::169.254.129.17::1026::SOCKET')
