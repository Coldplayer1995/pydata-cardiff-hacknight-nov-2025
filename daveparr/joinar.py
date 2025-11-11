"""Utility functions to join the Simpsons data set

**Should** be backend agnostic because [narwhals](https://narwhals-dev.github.io/narwhals/)

Running this module as 'main' produces polars style summary statistics
"""
import narwhals as nw
from narwhals.typing import FrameT

# IDEA(DRGP): Can these internal functions be piped not nested?
@nw.narwhalify
def _coerce_id_to_int(df: FrameT, col: str) -> FrameT:
    """
    Coerces a specific column to an integer for joining to the script

    :param df: A data frame
    :type df: FrameT
    :param col: The column to coerce
    :type col: str
    :return: The data frame `df` with the column `col` as an `Int64` type
    :rtype: FrameT
    """
    return df.with_columns((nw.col(col).cast(nw.Int64)))

@nw.narwhalify
def _join_script_to_df(script_lines: FrameT, df: FrameT, script_on: str):
    """
    Generically join the script data to other data sets

    :param script_lines: The script data
    :type script_lines: FrameT
    :param df: The other data
    :type df: FrameT
    :param script_on: The column to join on
    :type script_on: str
    """
    return script_lines.join(df, left_on=script_on, right_on="id", how="left")

# IDEA(DRGP): Can these top level functions be piped to join the 'whole' data set?
# IDEA(DRGP): Can these top level functions have some suitably flexible run time guarantees by using Pandera or Pydantic?
@nw.narwhalify
def join_script_by_character(
    script_lines: FrameT, characters: FrameT, id: str = "character_id"
) -> FrameT:
    """
    Joins the script data to the characters data

    :param script_lines: The script daa
    :type script_lines: FrameT
    :param characters: The characters data
    :type characters: FrameT
    :param id: The id column to join on, defaults to `"character_id"`
    :type id: str
    :return: The script and characters data joined
    :rtype: FrameT
    """
    return _join_script_to_df(_coerce_id_to_int(script_lines, id), characters, id)


@nw.narwhalify
def join_script_by_location(
    script_lines: FrameT, locations: FrameT, id: str = "location_id"
) -> FrameT:
    """
    Joins the script data to the location data

    :param script_lines: The script data
    :type script_lines: FrameT
    :param locations: The locations data
    :type locations: FrameT
    :param id: The id column to join on, defaults to `"location_id"`
    :type id: str
    :return: Description
    :rtype: Any
    """
    return _join_script_to_df(_coerce_id_to_int(script_lines, id), locations, id)


@nw.narwhalify
def join_script_by_episode(
    script_lines: FrameT, episodes: FrameT, id: str = "episode_id"
) -> FrameT:
    """
    Joins the script data to the episodes data

    :param script_lines: The script data
    :type script_lines: FrameT
    :param episodes: The episodes data
    :type episodes: FrameT
    :param id: The id column to join on, defaults to `"locations_id"`
    :type id: str
    :return: Description
    :rtype: Any
    """
    return _join_script_to_df(_coerce_id_to_int(script_lines, id), episodes, id)


if __name__ == "__main__":
    import polars as pl

    script_data = pl.read_csv("data/raw/simpsons_script_lines.csv")

    # IDEA(DRGP): Can this process be refactored to reduce repetition? Iterate over data + function pairs maybe?
    print(
        join_script_by_episode(
            script_data, pl.read_csv("data/raw/simpsons_episodes.csv")
        ).describe()
    )

    print(
        join_script_by_character(
            script_data, pl.read_csv("data/raw/simpsons_characters.csv")
        ).describe()
    )

    print(
        join_script_by_location(
            script_data, pl.read_csv("data/raw/simpsons_locations.csv")
        ).describe()
    )
