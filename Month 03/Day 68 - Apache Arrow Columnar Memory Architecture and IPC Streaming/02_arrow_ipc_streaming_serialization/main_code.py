# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: Arrow Inter-Process Communication (IPC) Binary Streams
Description: Serializes PyArrow RecordBatches into binary IPC stream formats
             and reconstructs schema/data without format conversion overhead.
"""
import pyarrow as pa  # type: ignore
import pyarrow.ipc as ipc  # type: ignore


class ArrowIPCStreamEngine:
    @staticmethod
    def serialize_and_deserialize(batch: pa.RecordBatch) -> pa.RecordBatch:
        # Write RecordBatch to in-memory binary IPC stream
        sink = pa.BufferOutputStream()
        with ipc.new_stream(sink, batch.schema) as writer:
            writer.write_batch(batch)
            
        buf = sink.getvalue()
        
        # Read RecordBatch from binary IPC stream
        reader = ipc.open_stream(buf)
        reconstructed_batch = reader.read_next_batch()
        return reconstructed_batch


if __name__ == "__main__":
    schema = pa.schema([
        ("sensor_id", pa.int32()),
        ("reading", pa.float64())
    ])
    
    raw_batch = pa.RecordBatch.from_arrays([
        pa.array([101, 102, 103], type=pa.int32()),
        pa.array([36.5, 37.1, 36.8], type=pa.float64())
    ], schema=schema)
    
    result_batch = ArrowIPCStreamEngine.serialize_and_deserialize(raw_batch)
    
    assert result_batch.num_rows == 3
    assert result_batch.column(0).to_pylist() == [101, 102, 103]
    
    print(f"[TASK 02 PASSED] Arrow IPC stream serialized/deserialized {result_batch.num_rows} rows zero-overhead.")