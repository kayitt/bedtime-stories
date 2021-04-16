from datetime import datetime
from typing import List
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from zoneinfo import ZoneInfo

import pandas as pd
from etl.src.transformer import (
    Builder,
    CurrentTemperatureTransformer,
    CompositeTransformer,
    Transformer,
    Director,
    TeaBoilsTransformer,
    WakeUpTimeTransformer,
    OutsideTemperatureTransformer,
)
from etl.src.data_classes import Model


def _series_to_ts(series: pd.Series):
    min_ts = series.index.min()
    return min_ts


def to_milliseconds(ts: datetime) -> int:
    return int(ts.timestamp() * 1000)


def _outside_temperature(s):
    min_temp = s.min()
    min_ts = s[s == min_temp].index[0]
    max_temp = s.max()
    max_ts = s[s == max_temp].index[0]
    return {
        "min": {
            "ts": min_ts,
            "value": float(min_temp),
        },
        "max": {
            "value": float(max_temp),
            "ts": max_ts,
        },
    }


class StubTransformer(Transformer):
    def transform(self, builder: Builder):
        builder.current_temperature = 21
        builder.num_tea_boils = 4
        builder.wake_up_time = 10
        builder.outside_temperature = 0


class TestCurrentTemperatureTransformer(TestCase):
    def setUp(self):
        self.current_temperature_query = """SELECT LAST("value") FROM "autogen"."°C" WHERE ("entity_id" = 'weather_station_temperature') AND time >= now() - 24h"""

        self.extractor = Mock()
        index = pd.to_datetime([17, 15], unit="ms")
        self.extractor.extract.return_value = pd.Series([23, 21], index=index)

    def test_transformed_builder_has_current_temperature(self):
        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.assertIsNotNone(builder.current_temperature)

    def test_accepts_extractor(self):
        CurrentTemperatureTransformer(self.extractor)

    def test_extract_called_with_current_temperature_query(self):
        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.extractor.extract.assert_called_with(query=self.current_temperature_query)

    def test_builder_none_temperature_before_transformation(self):
        builder = Builder()

        self.assertIsNone(builder.current_temperature)

    def test_current_temperature_is_latest_value(self):
        index = pd.to_datetime([17, 15], unit="ms")
        self.extractor.extract.return_value = pd.Series([23, 21], index=index)

        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.assertEqual(23, builder.current_temperature)

    def test_current_temperature_is_latest_value_another(self):
        index = pd.to_datetime([4, 9], unit="ms")
        self.extractor.extract.return_value = pd.Series([23, 21], index=index)

        builder = Builder()
        CurrentTemperatureTransformer(self.extractor).transform(builder)

        self.assertEqual(21, builder.current_temperature)


class TestOutsideTemperatureTransformer(TestCase):
    def setUp(self):
        self.outside_temperature_query = """SELECT "value" FROM "autogen"."°C" WHERE ("entity_id" = 'outdoor_module_temperature') AND time >= now() - 24h"""

        self.extractor = MagicMock()

    def test_transformed_builder_has_outside_temperature(self):
        builder = Builder()
        OutsideTemperatureTransformer(self.extractor).transform(builder)

        self.assertIsNotNone(builder.outside_temperature)

    def test_accepts_extractor(self):
        OutsideTemperatureTransformer(self.extractor)

    def test_extract_called_with_current_temperature_query(self):
        builder = Builder()
        OutsideTemperatureTransformer(self.extractor).transform(builder)

        self.extractor.extract.assert_called_with(query=self.outside_temperature_query)

    def test_builder_none_temperature_before_transformation(self):
        builder = Builder()

        self.assertIsNone(builder.outside_temperature)

    def test_current_temperature_is_min_max_values(self):
        index = pd.to_datetime([17, 15, 20], unit="ms")
        series = pd.Series([10, 21, 23], index=index)
        self.extractor.extract.return_value = series

        builder = Builder()
        OutsideTemperatureTransformer(self.extractor).transform(builder)

        self.assertEqual(_outside_temperature(series), builder.outside_temperature)

    def test_current_temperature_is_latest_value_another(self):
        index = pd.to_datetime([10, 11, 12], unit="ms")
        series = pd.Series([22, 18, 17], index=index)
        self.extractor.extract.return_value = series

        builder = Builder()
        OutsideTemperatureTransformer(self.extractor).transform(builder)

        self.assertEqual(_outside_temperature(series), builder.outside_temperature)


# noinspection DuplicatedCode
class TestTeaBoilsTransformer(TestCase):
    def setUp(self):
        self.num_tea_boils_query = """SELECT MAX("value") FROM "W" WHERE ("entity_id" = 'plug_current_consumption_3') AND time >= now() - 24h GROUP BY time(5m) fill(0)"""
        self.extractor = Mock()
        tz = ZoneInfo("Europe/Berlin")
        ts_1 = datetime(2021, 4, 11, hour=5, tzinfo=tz)
        ts_2 = datetime(2021, 4, 11, hour=10, tzinfo=tz)
        ts_3 = datetime(2021, 4, 11, hour=22, tzinfo=tz)
        ts_4 = datetime(2021, 4, 11, hour=23, tzinfo=tz)
        self.ts_1 = ts_1 #to_milliseconds(ts_1)
        self.ts_2 = ts_2 #to_milliseconds(ts_2)
        self.ts_3 = ts_3 #to_milliseconds(ts_3)
        self.ts_4 = ts_4 # to_milliseconds(ts_4)

    def from_times_to_timeseries(self, val1, val2, val3, val4):
        tz = ZoneInfo("Europe/Berlin")
        index = [to_milliseconds(datetime(2021, 4, 11, hour=5, tzinfo=tz)),
                 to_milliseconds(datetime(2021, 4, 11, hour=10, tzinfo=tz)),
                 to_milliseconds(datetime(2021, 4, 11, hour=22, tzinfo=tz)),
                 to_milliseconds(datetime(2021, 4, 11, hour=23, tzinfo=tz))]
        ts_index = pd.to_datetime([x for x in index], unit="ms").tz_localize(tz="UTC")
        return pd.Series([val1, val2, val3, val4], index=ts_index)

    def test_transformed_builder_has_num_tea_boils(self):
        builder = Builder()
        self.extractor.extract.return_value = self.from_times_to_timeseries(1,2,3,4)
        TeaBoilsTransformer(self.extractor).transform(builder)

        self.assertIsNotNone(builder.num_tea_boils)

    def test_accepts_extractor(self):
        TeaBoilsTransformer(self.extractor)

    def test_extract_called_with_tea_boils_query(self):
        builder = Builder()
        index = [self.ts_1, self.ts_2]
        self.extractor.extract.return_value = self.from_times_to_timeseries(1,2,3,4)
        TeaBoilsTransformer(self.extractor).transform(builder)

        self.extractor.extract.assert_called_with(query=self.num_tea_boils_query)

    def test_builder_none_tea_boils_before_transformation(self):
        builder = Builder()

        self.assertIsNone(builder.num_tea_boils)

    def test_num_tea_boils_counts_non_consequent_positive_values(self):
        index = [self.ts_1, self.ts_2, self.ts_3, self.ts_4]
        self.extractor.extract.return_value = self.from_times_to_timeseries(0,23,21,0)

        builder = Builder()
        TeaBoilsTransformer(self.extractor).transform(builder)

        self.assertEqual(1, builder.num_tea_boils)

    def test_num_tea_boils_works_if_first_value_positive(self):
        index = [self.ts_1, self.ts_2, self.ts_3, self.ts_4]
        self.extractor.extract.return_value = self.from_times_to_timeseries(1,0,1,0)

        builder = Builder()
        TeaBoilsTransformer(self.extractor).transform(builder)

        self.assertEqual(2, builder.num_tea_boils)




class TestWakeUpTime(TestCase):
    def setUp(self):
        self.wake_up_query = """SELECT movement FROM (SELECT count("value") AS movement FROM "state" WHERE ("entity_id" = 'hue_motion_sensor_entrance_motion') AND time >= now() - 24h GROUP BY time(1m) ) WHERE movement > 0"""
        self.extractor = MagicMock()

    def test_transformed_builder_has_wake_up_time(self):
        builder = Builder()
        WakeUpTimeTransformer(self.extractor).transform(builder)

        self.assertIsNotNone(builder.wake_up_time)

    def test_accepts_extractor(self):
        CurrentTemperatureTransformer(self.extractor)

    def test_extract_called_with_wake_up_time_query(self):
        builder = Builder()
        WakeUpTimeTransformer(self.extractor).transform(builder)

        self.extractor.extract.assert_called_with(query=self.wake_up_query)

    def test_builder_none_wake_up_time_before_transformation(self):
        builder = Builder()

        self.assertIsNone(builder.wake_up_time)

    def test_wake_up_time_is_argmin(self):
        index = pd.to_datetime([4, 5], unit="ms")
        series = pd.Series([34, 21], index=index)
        self.extractor.extract.return_value = series
        builder = Builder()
        expected_ts = _series_to_ts(series)

        WakeUpTimeTransformer(self.extractor).transform(builder)

        self.assertEqual(expected_ts, builder.wake_up_time)

    def test_wake_up_time_is_argmin_another(self):
        index = pd.to_datetime([4, 9], unit="ms")
        series = pd.Series([23, 21], index=index)
        self.extractor.extract.return_value = series
        builder = Builder()
        expected_ts = _series_to_ts(pd.Series([23, 21], index=index))

        WakeUpTimeTransformer(self.extractor).transform(builder)

        self.assertEqual(expected_ts, builder.wake_up_time)


class TestCompositeTransformer(TestCase):
    def setUp(self):
        self.current_temp_mock = Mock()
        self.transformer = CompositeTransformer(transformers=[self.current_temp_mock])

    def test_can_create_report(self):
        self.transformer.transform(Builder())

    def test_create_report_runs_current_temperature_transform(self):
        self.transformer.transform(Builder())

        self.current_temp_mock.transform.assert_called()


class TestDirector(TestCase):
    def test_has_create_report_accepts_transformer(self):
        mock_transformer = Mock()
        Director(mock_transformer).create_report()

        mock_transformer.transform.assert_called_with(Builder())

    def test_create_report_creates_model(self):
        expected_model = Model(
            current_temperature=21,
            num_tea_boils=4,
            wake_up_time=10,
            outside_temperature=0,
        )

        model = Director(StubTransformer()).create_report()

        self.assertEqual(expected_model, model)
