class Location:
    def __init__(
        self,
        i: int,
        j: int,
        h: float,
        takeoff: bool = False,
        landing: bool = False,
        landmark: bool = False,
    ):
        self.h: float = h
        self.i: int = i
        self.j: int = j
        self.takeoff: bool = takeoff
        self.landing: bool = landing
        self.landmark: bool = landmark

    def is_takeoff_or_landing(self):
        return self.takeoff or self.landing
