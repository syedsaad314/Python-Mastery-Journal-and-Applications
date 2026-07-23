# Lead Engineer: Syed Saad Bin Irfan
from schemas import SimulatedMetricMessage

class HighPerformanceEncoder:
    @staticmethod
    def _encode_varint(value: int) -> bytes:
        if value == 0:
            return b'\x00'
        res = bytearray()
        while value > 0:
            byte = value & 0x7F
            value >>= 7
            if value > 0:
                byte |= 0x80
            res.append(byte)
        return bytes(res)

    @staticmethod
    def serialize_message(msg: SimulatedMetricMessage) -> bytes:
        payload = bytearray()
        
        # Packing Field 1 (device_id): Tag = (1 << 3) | 0 = 8
        payload.append(8)
        payload.extend(HighPerformanceEncoder._encode_varint(msg.device_id))
        
        # Packing Field 2 (system_load): Tag = (2 << 3) | 0 = 16
        payload.append(16)
        payload.extend(HighPerformanceEncoder._encode_varint(msg.system_load))
        
        # Packing Field 3 (service_tag): Tag = (3 << 3) | 2 = 26
        payload.append(26)
        string_bytes = msg.service_tag.encode('utf-8')
        payload.extend(HighPerformanceEncoder._encode_varint(len(string_bytes)))
        payload.extend(string_bytes)
        
        return bytes(payload)