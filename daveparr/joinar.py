import narwhals as nw
from narwhals.typing import FrameT

@nw.narwhalify
def coerce_id_to_int(df: FrameT) -> FrameT:
    id_col = df.get_column("character_id")
    print(id_col.cast(nw.Int64))
    return df.with_columns((nw.col("character_id").cast(nw.Int64)))


@nw.narwhalify
def join_script_by_character(script_lines: FrameT, characters:FrameT) -> FrameT:
    print(coerce_id_to_int(script_lines))
    return coerce_id_to_int(script_lines).join(characters, left_on = "character_id", right_on = "id")



