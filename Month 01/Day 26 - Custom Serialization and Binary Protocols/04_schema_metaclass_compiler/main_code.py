"""
Core Topic: Declarative Binary Schema Meta-Compilers
Description: Compiles serialization rules from declarative models at type instantiation time.
Lead Engineer: Syed Saad Bin Irfan
"""

import struct
from typing import Dict, Any, List

class FieldBlueprint:
    """Base descriptor representing data attributes inside compiled models."""
    def __init__(self, struct_format_character: str) -> None:
        self.format_char: str = struct_format_character
        self.key_name: str = ""

    def __set_name__(self, owner_class: type, name_string: str) -> None:
        self.key_name = f"_schema_prop_{name_string}"

    def __get__(self, instance: object, owner_class: type) -> Any:
        if instance is None: return self
        return getattr(instance, self.key_name, None)

    def __set__(self, instance: object, value: Any) -> None:
        setattr(instance, self.key_name, value)


class CompiledBinarySchemaMeta(type):
    """Metaclass that extracts field formats to compile structural layout schemas at load time."""
    def __new__(mcs, class_name: str, bases_tuple: tuple, namespace_dict: dict) -> type:
        attribute_fields_ordered: List[tuple] = []
        
        # Identify all declared field attributes inside the namespace dictionary container
        for key, value in list(namespace_dict.items()):
            if isinstance(value, FieldBlueprint):
                attribute_fields_ordered.append((key, value.format_char))
                
        # Generate an optimized, compiled structural format layout signature string
        # '!Big-Endian' prefix alignment applied uniformly
        format_signature_string = "!" + "".join([item[1] for item in attribute_fields_ordered])
        
        # Inject compiled serialization rules back into the target class metadata map
        namespace_dict["_compiled_format_signature"] = format_signature_string
        namespace_dict["_ordered_field_keys"] = [item[0] for item in attribute_fields_ordered]
        namespace_dict["_fixed_byte_span_size"] = struct.calcsize(format_signature_string)

        return super().__new__(mcs, class_name, bases_tuple, namespace_dict)


class CompiledModelTemplate(metaclass=CompiledBinarySchemaMeta):
    """Provides automated binary serialization workflows using compiled class definitions."""
    _compiled_format_signature: str = ""
    _ordered_field_keys: List[str] = []
    _fixed_byte_span_size: int = 0

    def __init__(self, **kwargs: Any) -> None:
        for field in self._ordered_field_keys:
            setattr(self, field, kwargs.get(field, 0))

    def serialize_to_binary(self) -> bytes:
        """Packs internal object properties into compiled binary sequences instantly."""
        field_values = [getattr(self, field) for field in self._ordered_field_keys]
        return struct.pack(self._compiled_format_signature, *field_values)

    @classmethod
    def deserialize_from_binary(cls, source_buffer: bytes) -> "CompiledModelTemplate":
        """Unpacks raw bytes straight into object instances using the class's compiled schema layout."""
        unpacked_values = struct.unpack(cls._compiled_format_signature, source_buffer)
        kwargs = dict(zip(cls._ordered_field_keys, unpacked_values))
        return cls(**kwargs)


# --- Application Schema Implementation Testing Node ---
class ServerMetricsSnapshot(CompiledModelTemplate):
    """A data tracking layout compiled into optimized structural schemas at load time."""
    node_id = FieldBlueprint("I")      # Unsigned 32-bit Integer
    active_threads = FieldBlueprint("H") # Unsigned 16-bit Integer
    cpu_utilization = FieldBlueprint("d") # 64-bit Floating Point Double

if __name__ == "__main__":
    print("\n=== SYSTEM START: DECLARATIVE SCHEMA METACLASS COMPILER ===")
    
    snapshot = ServerMetricsSnapshot(node_id=202611, active_threads=45, cpu_utilization=0.6821)
    binary_data = snapshot.serialize_to_binary()
    print(f"[METACLASS] Compiled Schema Signature layout generated: {ServerMetricsSnapshot._compiled_format_signature}")
    print(f"[METACLASS] Total serialization length: {len(binary_data)} bytes (Fixed size span: {ServerMetricsSnapshot._fixed_byte_span_size})")

    restored_instance = ServerMetricsSnapshot.deserialize_from_binary(binary_data)
    print(f"[METACLASS] Deserialization verification. Core metric count: {restored_instance.node_id} | CPU: {restored_instance.cpu_utilization}")