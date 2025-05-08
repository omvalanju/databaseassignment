from typing import List
from influxdb_client import Point
from app.database.influxdb import get_write_api, get_query_api, get_bucket, get_org
from app.models.run import Run

class RunRepository:
    @staticmethod
    def insert(run: Run) -> None:
        write_api = get_write_api()
        point = run.to_point()
        write_api.write(bucket=get_bucket(), org=get_org(), record=point)

    @staticmethod
    def get_recent_runs(user_id: str, limit: int = 5) -> List[Run]:
        """
        Query the last N runs for a given user, sorted by time descending.
        """
        query_api = get_query_api()
        flux = f'''
        from(bucket: "{get_bucket()}")
          |> range(start: -30d)                     // adjust window as needed
          |> filter(fn: (r) => r._measurement == "run")
          |> filter(fn: (r) => r.user_id == "{user_id}")
          |> sort(columns: ["_time"], desc: true)
          |> limit(n: {limit})
        '''
        tables = query_api.query(flux, org=get_org())
        runs: List[Run] = []
        for table in tables:
            for record in table.records:
                runs.append(Run.from_query_record(record))
        return runs
