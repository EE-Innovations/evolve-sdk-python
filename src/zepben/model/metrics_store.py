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


from zepben.model.metering import MeterReading


class MetricsStore(object):
    """
    We store buckets of time (5 minute intervals), which map to meters which map to Reading types (see metering.py)
    to ordered lists of readings of that type.
    If a meter doesn't report for a bucket, that meter did not report any metrics for that time period
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

    def __iter__(self):
        # TODO: this is a bit broken and doesn't make sense.... iter should return self, and next should do iteration
        for bucket_time in self.buckets:
            for meter, typ in self.store[bucket_time].items():
                for readings in typ.values():
                    mr = MeterReading(meter=meter, readings=readings)
                    yield mr

    def __next__(self):
        for r in self.ascending_iteration():
            yield r

        raise StopIteration()

    def get_readings(self, reading_type):
        """
        At the moment we simply iterate over each bucket, meter, and reading type, and return
        MeterReadings with a single type of reading
        """
        for bucket_time in self.buckets:
            for meter, typ in self.store[bucket_time].items():
                mr = MeterReading(meter=meter, readings=typ[reading_type])
                yield mr

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

    def store_meter_reading(self, meter_reading):
        """
        Stores a given meter reading. If the meter already has readings in the bucket it will append
        the readings to the existing meter, based on the type of the reading.

        Note that a MeterReadings mRID is not used as part of this function. For the purposes of storing readings,
        only the associated meter mRID is considered.
        :param meter_reading:
        :return:
        """
        # TODO: This should store Readings, not MeterReadings
        for reading in meter_reading.readings:
            bucket_time = self._get_bucket(reading.timestamp)
            bucket = self.store.get(bucket_time, {})
            self._bucket_times.add(bucket_time)
            reading_types = bucket.get(meter_reading.meter, {})
            readings = reading_types.get(type(reading), [])
            readings.append(reading)
            reading_types[type(reading)] = readings
            bucket[meter_reading.meter] = reading_types
            self.store[bucket_time] = bucket
