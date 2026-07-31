# Lead Engineer: Syed Saad Bin Irfan
"""
Core Topic: High-Throughput Arrow Flight RPC Protocol Pipeline
Description: Simulates an Arrow Flight RPC server stream generator, transmitting
             RecordBatches over binary network memory buffers without serialization.
"""
import pyarrow as pa  # type: ignore


class SimulatedFlightStreamProducer:
    def __init__(self, total_batches: int, batch_size: int):
        self.total_batches = total_batches
        self.batch_size = batch_size
        self.schema = pa.schema([("stream_id", pa.int64()), ("metric", pa.float64())])

    def generate_flight_stream(self):
        # Generator yielding serialized Arrow Flight RecordBatches
        for i in range(self.total_batches):
            yield pa.RecordBatch.from_arrays([
                pa.array([i] * self.batch_size, type=pa.int64()),
                pa.array([99.9] * self.batch_size, type=pa.float64())
            ], schema=self.schema)


if __name__ == "__main__":
    producer = SimulatedFlightStreamProducer(total_batches=5, batch_size=100)
    
    total_received_rows = 0
    for flight_batch in producer.generate_flight_stream():
        assert isinstance(flight_batch, pa.RecordBatch)
        total_received_rows += flight_batch.num_rows
        
    assert total_received_rows == 500
    
    print(f"[TASK 06 PASSED] Simulated Flight RPC Stream received {total_received_rows} records over binary memory buffers.")