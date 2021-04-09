from dataclasses import dataclass
import datetime


@dataclass
class Model:
    current_temperature: float
    num_tea_boils: int
    wake_up_time: datetime.datetime
