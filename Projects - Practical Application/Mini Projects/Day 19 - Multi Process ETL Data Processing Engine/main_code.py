"""
System: Multi-Process ETL Data Processing Engine
Description: A production-grade parallel Extract-Transform-Load engine that partitions dense unstructured 
             data blocks, cleans records concurrently, and aggregates telemetry metrics via process-safe pipes.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
import logging
import multiprocessing
import os
import time
from typing import Dict, List, Tuple, Any, Optional

# Configure clean, informative production-grade tracking formats
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] (PID-%(process)d) %(message)s')

class ParallelETLEngine:
    def __init__(self, raw_source_path: str, output_destination_path: str, chunk_capacity: int = 1000) -> None:
        self.source_path: str = raw_source_path
        self.dest_path: str = output_destination_path
        self.chunk_size: int = chunk_capacity
        self.cpu_core_limit: int = max(1, multiprocessing.cpu_count() - 1)

    @staticmethod
    def _transform_and_clean_record(raw_record_string: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """Runs validation routines to filter and scrub unstructured log entries."""
        if not raw_record_string.strip():
            return False, None
        try:
            record = json.loads(raw_record_string)
            
            # Data cleansing checks
            if "transaction_id" not in record or "amount" not in record:
                return False, None
                
            # Perform downstream data enrichment transformations
            record["amount"] = float(record["amount"])
            record["etl_timestamp"] = time.time()
            record["status_cleansed"] = True
            record["client_region"] = record.get("client_region", "UNKNOWN").upper()
            
            return True, record
        except (json.JSONDecodeError, ValueError, TypeError):
            return False, None

    def _worker_pipeline_entrypoint(self, chunk_data_payload: List[str], communication_pipe: multiprocessing.connection.Connection) -> None:
        """Executes extraction and transformation rules over an isolated data chunk."""
        cleaned_records_batch: List[Dict[str, Any]] = []
        dropped_records_counter: int = 0
        local_financial_sum: float = 0.0

        for raw_line in chunk_data_payload:
            success, clean_obj = self._transform_and_clean_record(raw_line)
            if success and clean_obj:
                cleaned_records_batch.append(clean_obj)
                local_financial_sum += clean_obj["amount"]
            else:
                dropped_records_counter += 1

        # Package data and send metrics summary back down the IPC pipeline channel
        summary_payload = {
            "processed_records": cleaned_records_batch,
            "dropped_count": dropped_records_counter,
            "financial_sum": local_financial_sum
        }
        
        try:
            communication_pipe.send(summary_payload)
        finally:
            communication_pipe.close()

    def execute_etl_orchestration(self) -> Dict[str, Any]:
        """Orchestrates the ingestion, process scaling, and data aggregation workflow."""
        logging.info(f"Initializing ETL processing pipeline. Optimized core assignment count: {self.cpu_core_limit}")
        
        if not os.path.exists(self.source_path):
            logging.error(f"Execution halted: Source file target '{self.source_path}' does not exist.")
            return {"status": "FAILED", "reason": "MISSING_SOURCE"}

        start_time = time.perf_counter()

        # Step 1: Extract data chunks from source logs
        all_chunks: List[List[str]] = []
        current_chunk: List[str] = []
        
        with open(self.source_path, 'r', encoding='utf-8') as src_file:
            for line in src_file:
                current_chunk.append(line)
                if len(current_chunk) >= self.chunk_size:
                    all_chunks.append(current_chunk)
                    current_chunk = []
            if current_chunk: # Append remaining data lines
                all_chunks.append(current_chunk)

        logging.info(f"Extraction step complete. Total data chunks generated: {len(all_chunks)}")

        # Step 2: Scale workloads concurrently across multiple processes
        active_processes: List[multiprocessing.Process] = []
        pipe_connections_registry: List[multiprocessing.connection.Connection] = []
        
        # Process chunks using a round-robin task allocation loop
        for idx, chunk in enumerate(all_chunks):
            parent_conn, child_conn = multiprocessing.Pipe(duplex=False)
            pipe_connections_registry.append(parent_conn)
            
            p = multiprocessing.Process(
                target=self._worker_pipeline_entrypoint,
                args=(chunk, child_conn),
                name=f"ETLWorkerNode-{idx}"
            )
            active_processes.append(p)
            p.start()
            # Ensure child handle is closed inside parent context to prevent resource leaks
            child_conn.close() 

        logging.info("All parallel ETL processes spawned and processing data chunks...")

        # Step 3: Aggregate metrics and compile results from IPC channels
        compiled_master_dataset: List[Dict[str, Any]] = []
        total_malformed_records_dropped: int = 0
        aggregated_financial_revenue: float = 0.0

        for parent_connection in pipe_connections_registry:
            try:
                # Retrieve individual worker summaries via IPC
                worker_summary = parent_connection.recv()
                compiled_master_dataset.extend(worker_summary["processed_records"])
                total_malformed_records_dropped += worker_summary["dropped_count"]
                aggregated_financial_revenue += worker_summary["financial_sum"]
            except EOFError:
                logging.error("IPC pipe failure: Worker process terminated unexpectedly.")
            finally:
                parent_connection.close()

        # Ensure all child workers are joined and cleaned up cleanly
        for p in active_processes:
            p.join()

        # Step 4: Write transformed datasets to target output files
        with open(self.dest_path, 'w', encoding='utf-8') as target_dest:
            for structured_record in compiled_master_dataset:
                target_dest.write(json.dumps(structured_record) + "\n")

        execution_duration = time.perf_counter() - start_time
        logging.info(f"ETL pipeline executed successfully in {execution_duration:.4f} seconds.")

        return {
            "status": "METRICS_COMPILED",
            "total_records_saved": len(compiled_master_dataset),
            "malformed_records_purged": total_malformed_records_dropped,
            "aggregated_financial_revenue": round(aggregated_financial_revenue, 2),
            "duration_sec": round(execution_duration, 4)
        }

if __name__ == "__main__":
    print("\n=== SYSTEM START: PARALLEL MULTI-PROCESS ETL LOG ENGINE ===\n")
    mock_input = "raw_source_transactions.log"
    mock_output = "scrubbed_clean_production_output.json"

    # Seed unstructured raw source datasets
    with open(mock_input, "w") as f:
        f.write('{"transaction_id": "TX_1001", "amount": "150.75", "client_region": "pk"}\n')
        f.write('MALFORMED_LINE_DATA_STRUCTURE_DISRUPTED_ENTRY\n') # Intentional dirty row
        f.write('{"transaction_id": "TX_1002", "amount": "2300.50", "client_region": "ae"}\n')
        f.write('{"transaction_id": "TX_1003", "amount": "45.00"}\n') # Missing element row
        f.write('{"transaction_id": "TX_1004", "amount": "890.25", "client_region": "us"}\n')

    # Initialize and execute the parallel ETL engine
    etl_pipeline = ParallelETLEngine(raw_source_path=mock_input, output_destination_path=mock_output, chunk_capacity=2)
    metrics_summary = etl_pipeline.execute_etl_orchestration()

    print(f"\n=== ETL AGGREGATION METRICS METADATA ===\n{json.dumps(metrics_summary, indent=4)}")

    # Clean up file structures post-execution
    for path in [mock_input, mock_output]:
        if os.path.exists(path):
            os.remove(path)