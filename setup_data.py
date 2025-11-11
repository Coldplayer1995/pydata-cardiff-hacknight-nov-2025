import pathlib
import urllib.request
import pydytuesday
from daveparr import joinar

def download_docs() -> None:
    docs_paths = [
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-02-04/readme.md",
        "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2025/2025-02-04/meta.yaml"
    ]

    for file in docs_paths:
        path_value = pathlib.Path(file)
        urllib.request.urlretrieve(file, "docs/" + path_value.name)

def main():
    download_docs()
    data = pydytuesday.tt_download('2025-02-04', save_to_disk = False)

    for k,v in data.items():
        print(k)
        v.info()
        v.to_csv("data/raw/" + k + ".csv", index = False)


if __name__ == "__main__":
    main()
