import logging
import sys
import os

from pyneato import (
    Account,
    Neato,
    OrbitalPasswordSession,
)

Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(
    stream = sys.stdout,
    filemode = "w",
    format = Log_Format,
    level = logging.DEBUG
)

vendor = Neato()

email = os.environ['MYNEATO_USER']
password = os.environ['MYNEATO_PASSWORD']

session = OrbitalPasswordSession(
    email,
    password
)
account = Account(session)
robot = account.robots.pop()

for index, floorplan in enumerate(account.floorplans):
    print("%d. %s"%(
        index + 1,
        floorplan.name,
    ))

robot.get_state()

# robot.start_cleaning(account.floorplans[0])
