"""
Copyright 2019 Zeppelin Bend Pty Ltd
This file is part of cimbend.

cimbend is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

cimbend is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with cimbend.  If not, see <https://www.gnu.org/licenses/>.
"""


from zepben.model.meter_reading import Meter


class MetricsStore(object):
    """
    We store buckets of time (5 minute intervals), which map to meters with sets of readings
    If a meter doesn't report for a bucket, it will not have any meter present
    """
    def __init__(self, bucket_duration: int = 5000):
        self.store = dict()
        self.bucket_duration = bucket_duration
        self._ordered_buckets = []
        self._bucket_times = set()

    def _get_bucket(self, timestamp):
        """
        Return the timestamp defining each bucket. These will start from 0 and be in intervals of `self.bucket_duration`
        """
        return timestamp - (timestamp % self.bucket_duration)

    @property
    def meters(self):
        """
        Returns a list of all meters in no particular order.
        You should avoid this and instead prefer to operate on a bucket at a time
        """
        meters = []
        for bucket in self.store.values():
            meters.extend(bucket.values())
        return meters

    def __iter__(self):
        for bucket_time in self.buckets:
            for meter in self.store[bucket_time].values():
                yield meter

    def __next__(self):
        for r in self.ascending_iteration():
            yield r

        raise StopIteration()

    @property
    def buckets(self):
        """
        Time buckets in this metrics store.
        :return: List of present time buckets in ascending order
        """
        # We lazy sort because we don't want to slow down write times. This will probably disappear in the long run
        # TODO: Revisit this after first stable version, potentially when a timeseries DB is implemented

        ordered_buckets = sorted(self._bucket_times)
        return ordered_buckets

    def ascending_iteration(self):
        """

        :return: Mapping of meter IDs to Meter's by bucket time in ascending order
        """
        for bucket_time in self.buckets:
            for meter in self.store[bucket_time].values():
                yield meter

    def store_meter_reading(self, mrid, name, psr_id, timestamp, value, kind, phase, unit):
        bucket_time = self._get_bucket(timestamp)
        bucket = self.store.get(bucket_time, {})
        self._bucket_times.add(bucket_time)
        meter = bucket.get(mrid, Meter(mrid, name, psr_id))
        meter.add_reading(timestamp, value, kind, phase, unit)
        bucket[mrid] = meter
        self.store[bucket_time] = bucket
