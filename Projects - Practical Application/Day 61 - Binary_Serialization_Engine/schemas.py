# Lead Engineer: Syed Saad Bin Irfan
from dataclasses import dataclass

@dataclass
class SimulatedMetricMessage:
    device_id: int      # Field Token Id: 1, Layout Profile: Varint (Wire Type 0)
    system_load: int    # Field Token Id: 2, Layout Profile: Varint (Wire Type 0)
    service_tag: str    # Field Token Id: 3, Layout Profile: Length-Delimited (Wire Type 2)