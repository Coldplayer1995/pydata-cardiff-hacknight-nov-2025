import daveparr.joinar as joinar
import polars as pl
from polars.testing import assert_frame_equal
import pytest


def test_coerce_id_to_int():
    result = joinar._coerce_id_to_int(
        pl.DataFrame({"test_id": [1.0, 2.0, 3.0]}), "test_id"
    )
    assert_frame_equal(result, pl.DataFrame({"test_id": [1, 2, 3]}))


# IDEA(DRGP): Can these tests be fixturised with params for better ergonomics?
# IDEA(DRGP): Can these tests be extended to check that not all results on the joined data are null?
def test_join_script_by_character():
    script_data = pl.read_csv("data/raw/simpsons_script_lines.csv")
    result = joinar.join_script_by_character(
        script_data, pl.read_csv("data/raw/simpsons_characters.csv")
    )
    assert isinstance(result, pl.DataFrame)
    assert len(result) == len(script_data)
    assert len(result.unique()) == len(script_data.unique())


def test_join_script_by_location():
    script_data = pl.read_csv("data/raw/simpsons_script_lines.csv")
    result = joinar.join_script_by_location(
        script_data, pl.read_csv("data/raw/simpsons_locations.csv")
    )
    assert isinstance(result, pl.DataFrame)
    assert len(result) == len(script_data)
    assert len(result.unique()) == len(script_data.unique())


def test_join_script_by_episodes():
    script_data = pl.read_csv("data/raw/simpsons_script_lines.csv")
    result = joinar.join_script_by_episode(
        script_data, pl.read_csv("data/raw/simpsons_episodes.csv")
    )
    assert isinstance(result, pl.DataFrame)
    assert len(result) == len(script_data)
    assert len(result.unique()) == len(script_data.unique())
