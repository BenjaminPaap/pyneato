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
    print("%d. Floorplan: %s"%(
        index + 1,
        floorplan.name,
    ))

    for index, track in enumerate(floorplan.tracks):
        print(" --> %d. Track: %s"%(
            index + 1,
            track.name
        ))

robot.get_state()


# Clean just a set of rooms
#floorplan = account.floorplans.pop()
#tracks = list(floorplan.tracks)[2:4]
#robot.start_cleaning(floorplan, tracks)

# Clean whole floor
#floorplan = account.floorplans.pop()
#robot.start_cleaning(floorplan)
