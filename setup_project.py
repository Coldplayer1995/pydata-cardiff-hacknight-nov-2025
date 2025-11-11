import pandas
import polars
import narwhals
import pathlib
import urllib.request


def download_data() -> None:
    csv_paths = [
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-02-04/simpsons_characters.csv",
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-02-04/simpsons_episodes.csv",
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-02-04/simpsons_locations.csv",
            "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-02-04/simpsons_script_lines.csv",
        ]

    for file in csv_paths:
        path_value = pathlib.Path(file)
        data = polars.read_csv(file, ignore_errors=True)
        print(data.describe())
        data.write_csv("data/"+path_value.name)

def download_docs() -> None:
    docs_paths = [
        "https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-02-04/readme.md",
        "https://github.com/rfordatascience/tidytuesday/blob/main/data/2025/2025-02-04/meta.yaml"
    ]

    for file in docs_paths:
        path_value = pathlib.Path(file)
        urllib.request.urlretrieve(file, "docs/" +path_value.name)

def main():
    download_data()
    download_docs()


if __name__ == "__main__":
    main()
