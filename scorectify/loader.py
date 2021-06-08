from os import PathLike
from pathlib import Path
from typing import Union, List

import numpy as np
from PIL import Image
from pdf2image import convert_from_path


def load(path: Union[Path, PathLike, str], **kwargs) -> List[Image.Image]:
    """
    Load a visual music score form a file.

    PDFs, JPGs and PNGs are supported.
    :param path: The path to the music score
    :type path: Union[PathLike, str]
    :param kwargs: The args to give to the pdf loader
    :type kwargs: dict
    :return: A list of numpy arrays of the music score
    :rtype: List[np.ndarray]
    """
    if isinstance(path, str):
        path = Path(path)
    if path.suffix == '.pdf':
        return convert_from_path(path, **kwargs)
    elif path.suffix in ('.jpg', '.jpeg', '.png'):
        return [Image.open(path)]
    raise Exception(f"File does not have one of the expected suffixes (pdf, jpg, jpeg, png): {str(path)}")
