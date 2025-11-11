import narwhals as nw
from narwhals.typing import FrameT

@nw.narwhalify
def coerce_id_to_int(df: FrameT, col: str) -> FrameT:
    return df.with_columns((nw.col(col).cast(nw.Int64)))


@nw.narwhalify
def join_script_by_character(script_lines: FrameT, characters:FrameT) -> FrameT:
    coerced_df = coerce_id_to_int(script_lines, "character_id")
    return coerced_df.join(nw.to_native(characters), left_on = "character_id", right_on = "id")



