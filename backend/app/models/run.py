from datetime import datetime
from influxdb_client import Point

class Run:
    def __init__(
        self,
        user_id: str,
        heart_rate: int,
        pace: float,
        distance: float,
        timestamp: datetime = None
    ):
        if not user_id:
            raise ValueError("user_id is required")
        self.user_id    = user_id
        self.heart_rate = heart_rate
        self.pace       = pace
        self.distance   = distance
        self.timestamp  = timestamp or datetime.utcnow()

    def to_point(self) -> Point:
        """
        Convert this Run into an InfluxDB Point for writing.
        """
        return (
            Point("run")
            .tag("user_id", self.user_id)
            .field("heart_rate", self.heart_rate)
            .field("pace", self.pace)
            .field("distance", self.distance)
            .time(self.timestamp, write_precision='s')
        )

    @classmethod
    def from_query_record(cls, record) -> "Run":
        """
        Build a Run instance from an InfluxDB query record.
        Assumes record.values contains:
          _time, user_id, heart_rate, pace, distance
        """
        return cls(
            user_id    = record.values.get("user_id"),
            heart_rate = int(record.get_value_by_key("heart_rate")),
            pace       = float(record.get_value_by_key("pace")),
            distance   = float(record.get_value_by_key("distance")),
            timestamp  = record.get_time()
        )
