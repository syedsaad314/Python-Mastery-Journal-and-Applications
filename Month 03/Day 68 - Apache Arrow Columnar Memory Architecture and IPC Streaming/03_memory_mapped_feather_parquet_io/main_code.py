# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Memory-Mapped Feather File I/O
Description: Opens Feather (Arrow IPC File format) via OS memory-mapping
             to access datasets without loading file contents into RAM.
"""
from pathlib import Path
import tempfile
import pyarrow as pa  # type: ignore
import pyarrow.feather as feather  # type: ignore


class MemoryMappedFeatherEngine:
    @staticmethod
    def write_and_mmap(file_path: Path, table: pa.Table) -> pa.Table:
        # Save table to Feather format (IPC file layout)
        feather.write_feather(table, file_path)
        
        # Open file via OS memory map
        mmap_source = pa.memory_map(str(file_path), mode="r")
        return feather.read_table(mmap_source)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as tmpdir:
        feather_path = Path(tmpdir) / "data.feather"
        
        orig_table = pa.Table.from_pydict({
            "id": pa.array([1, 2, 3, 4], type=pa.int64()),
            "value": pa.array([10.5, 20.5, 30.5, 40.5], type=pa.float64())
        })
        
        mmapped_table = MemoryMappedFeatherEngine.write_and_mmap(feather_path, orig_table)
        
        assert len(mmapped_table) == 4
        assert mmapped_table.column("value").to_pylist() == [10.5, 20.5, 30.5, 40.5]
        
        print("[TASK 03 PASSED] Feather dataset opened via memory-mapped IPC reader.")