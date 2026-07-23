# Lead Engineer: Syed Saad Bin Irfan
from schemas import SimulatedMetricMessage

class HighPerformanceDecoder:
    @staticmethod
    def _parse_varint(buffer: bytes, index: int) -> tuple[int, int]:
        result = 0
        shift = 0
        while True:
            byte = buffer[index]
            index += 1
            result |= (byte & 0x7F) << shift
            if not (byte & 0x80):
                break
            shift += 7
        return result, index

    @staticmethod
    def deserialize_message(buffer: bytes) -> SimulatedMetricMessage:
        index = 0
        buffer_len = len(buffer)
        
        device_id = 0
        system_load = 0
        service_tag = ""
        
        while index < buffer_len:
            tag, index = HighPerformanceDecoder._parse_varint(buffer, index)
            field_number = tag >> 3
            
            if field_number == 1:
                device_id, index = HighPerformanceDecoder._parse_varint(buffer, index)
            elif field_number == 2:
                system_load, index = HighPerformanceDecoder._parse_varint(buffer, index)
            elif field_number == 3:
                str_len, index = HighPerformanceDecoder._parse_varint(buffer, index)
                service_tag = buffer[index:index+str_len].decode('utf-8')
                index += str_len
            else:
                raise ValueError(f"Unknown architectural layout tag detected: {tag}")
                
        return SimulatedMetricMessage(device_id, system_load, service_tag)