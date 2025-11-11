import daveparr.joinar as joinar
import polars as pl
from polars.testing import assert_frame_equal

def test_coerce_id_to_int():
    result = joinar.coerce_id_to_int(pl.DataFrame({"test_id": [1.0, 2.0, 3.0]}), "test_id")
    assert_frame_equal(result, pl.DataFrame({"test_id": [1, 2, 3]}))

def test_join_script_by_character():
    result = joinar.join_script_by_character(
        pl.read_csv("data/raw/simpsons_script_lines.csv"), 
        pl.read_csv("data/raw/simpsons_characters.csv"))
    print(result)
    