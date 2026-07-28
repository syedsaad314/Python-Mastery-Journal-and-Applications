# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Custom Pandas Extension Arrays
Description: Builds a custom domain-specific ExtensionArray interface to register 
             first-class custom data types with native Pandas Series support.
"""
import numpy as np # type: ignore
import pandas as pd # type: ignore
from pandas.api.extensions import ExtensionArray, ExtensionDtype, register_extension_dtype # type: ignore


@register_extension_dtype
class PointDtype(ExtensionDtype):
    name = "2d_point"
    type = tuple
    kind = "O"

    @classmethod
    def construct_array_from_sequence(cls, scalars, dtype=None, copy=False):
        return PointArray(np.asarray(scalars, dtype=object))


class PointArray(ExtensionArray):
    def __init__(self, values: np.ndarray):
        self._data = values
        self._dtype = PointDtype()

    @property
    def dtype(self):
        return self._dtype

    def __len__(self):
        return len(self._data)

    def __getitem__(self, item):
        return self._data[item]

    def isna(self):
        return np.array([x is None for x in self._data], dtype=bool)

    def take(self, indices, allow_fill=False, fill_value=None):
        indices = np.asarray(indices, dtype=int)
        if allow_fill:
            fill = fill_value if fill_value is not None else None
            data = [self._data[i] if i >= 0 else fill for i in indices]
        else:
            data = self._data[indices]
        return PointArray(np.asarray(data, dtype=object))

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        return PointArray(np.asarray(scalars, dtype=object))


if __name__ == "__main__":
    points = [(10, 20), (30, 40), (50, 60)]
    s_points = pd.Series(PointArray._from_sequence(points))
    
    assert s_points.dtype.name == "2d_point"
    assert s_points[0] == (10, 20)
    assert len(s_points) == 3
    
    print(f"[TASK 05 PASSED] Custom ExtensionDtype '{s_points.dtype.name}' successfully integrated into Pandas Series.")