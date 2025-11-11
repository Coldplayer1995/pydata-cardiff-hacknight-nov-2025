import narwhals as nw
from narwhals.typing import FrameT

@nw.narwhalify
def _coerce_id_to_int(df: FrameT, col: str) -> FrameT:
    """
    Coerces a specific column to an integer for joining to the script
    
    :param df: A data frame
    :type df: FrameT
    :param col: The column to coerce
    :type col: str
    :return: The data frame `df` with the column `col` as an `Int64` type
    :rtype: Any
    """
    return df.with_columns((nw.col(col).cast(nw.Int64)))


@nw.narwhalify
def join_script_by_character(script_lines: FrameT, characters:FrameT) -> FrameT:
    """
    Joins the script data to the characters data
    
    :param script_lines: The script daa
    :type script_lines: FrameT
    :param characters: The characters data
    :type characters: FrameT
    :return: The Script and characters data joined
    :rtype: Any
    """
    coerced_df = _coerce_id_to_int(script_lines, "character_id")
    # TODO (DRGP): Work out why I need to flip to native to flip back again?
    return coerced_df.join(nw.to_native(characters), left_on = "character_id", right_on = "id")



