"""
Core Topic: Advanced Attribute Access via Descriptors
Description: Controls class state assignments using low-level memory binding hooks.
Lead Engineer: Syed Saad Bin Irfan
"""

class BoundedIntegerField:
    """A descriptor class that handles attribute storage and validation at the object level."""
    def __init__(self, minimum_value: int, maximum_value: int) -> None:
        self.min: int = minimum_value
        self.max: int = maximum_value
        # Store a private key name string post-binding
        self.storage_key: str = ""

    def __set_name__(self, owner_class: type, name_string: str) -> None:
        # Dynamically determine the variable name assigned inside the parent object
        self.storage_key = f"__private_{name_string}"

    def __get__(self, instance_object: object, owner_class: type) -> any:
        # If accessed from the class level, return the descriptor instance itself
        if instance_object is None:
            return self
        return getattr(instance_object, self.storage_key, 0)

    def __set__(self, instance_object: object, incoming_value: int) -> None:
        if not isinstance(incoming_value, int):
            raise TypeError(f"Field expects integer inputs. Received: {type(incoming_value)}")
        if not (self.min <= incoming_value <= self.max):
            raise ValueError(f"Value {incoming_value} breaches range boundary thresholds [{self.min}-{self.max}].")
        # Commit the validated data straight into the object's instance dictionary
        setattr(instance_object, self.storage_key, incoming_value)


class ServerConfiguration:
    # Bind custom descriptor instances to class variables
    allocated_cores = BoundedIntegerField(minimum_value=1, maximum_value=64)
    network_port = BoundedIntegerField(minimum_value=1024, maximum_value=65535)

if __name__ == "__main__":
    config = ServerConfiguration()
    config.allocated_cores = 16
    config.network_port = 8080
    print(f"[DESCRIPTOR] Active Cotes Loaded: {config.allocated_cores} | Port: {config.network_port}")

    try:
        config.network_port = 99  # Should trip validation thresholds
    except ValueError as err:
        print(f"[TRAPPED EXPECTED ERROR] Defenses active: {err}")