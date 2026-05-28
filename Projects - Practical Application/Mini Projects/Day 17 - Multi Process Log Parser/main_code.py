"""
Mini-Project: Concurrent File Analytics Tool
Description: Multiprocessed file parsing engine splitting log analysis across independent worker processes.
Lead Engineer: Syed Saad Bin Irfan
"""

import json
import multiprocessing
import os
from typing import Dict, List, Generator

class LogParserEngine:
    def __init__(self, log_path: str, core_count: int = 2) -> None:
        self.log_path: str = log_path
        self.workers: int = core_count
        self.result_queue: multiprocessing.Queue = multiprocessing.Queue()

    def _stream_bytes(self, offset: int, length: int) -> Generator[str, None, None]:
        """Reads a specific section of a file line-by-line using byte offsets."""
        with open(self.log_path, 'r', encoding='utf-8', errors='ignore') as src:
            src.seek(offset)
            read_bytes = 0
            while read_bytes < length:
                line = src.readline()
                if not line:
                    break
                read_bytes += len(line.encode('utf-8'))
                yield line.strip()

    def _worker_scan(self, offset: int, length: int, alert_key: str) -> None:
        matches = []
        for line in self._stream_bytes(offset, length):
            if alert_key in line and line.startswith("{"):
                try:
                    matches.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        self.result_queue.put(matches)

    def process_logs(self, target_level: str) -> List[Dict[str, str]]:
        file_bytes = os.path.getsize(self.log_path)
        segment_bytes = file_bytes // self.workers
        pool: List[multiprocessing.Process] = []

        for i in range(self.workers):
            start = i * segment_bytes
            size = segment_bytes if i < self.workers - 1 else (file_bytes - start)
            proc = multiprocessing.Process(target=self._worker_scan, args=(start, size, target_level))
            pool.append(proc)
            proc.start()

        all_matches = []
        for _ in range(self.workers):
            all_matches.extend(self.result_queue.get())

        for proc in pool:
            proc.join()

        return all_matches

if __name__ == "__main__":
    # Local verification loop
    test_file = "app_runtime.json.log"
    with open(test_file, "w") as f:
        f.write('{"level": "ERROR", "ctx": "AUTH", "msg": "Expired token"}\n')
        f.write('{"level": "INFO", "ctx": "DB", "msg": "Connection OK"}\n')
        f.write('{"level": "ERROR", "ctx": "PAY", "msg": "Gateway timeout"}\n')

    parser = LogParserEngine(test_file)
    errors = parser.process_logs("ERROR")
    print(f"[PORTFOLIO SHOWCASE] Extracted Error JSON Records:\n{json.dumps(errors, indent=2)}")
    
    if os.path.exists(test_file):
        os.remove(test_file)