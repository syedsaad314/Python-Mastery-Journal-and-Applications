"""
Core Topic: Class-Creation Lifecycle Metaclasses
Description: Enforces strict naming conventions and architecture requirements across classes at boot runtime.
Lead Engineer: Syed Saad Bin Irfan
"""

class OperationalContractMeta(type):
    """Metaclass that validates class definitions before compiling them into active types."""
    def __new__(mcs, name_string: str, bases_tuple: tuple, namespace_dict: dict) -> type:
        print(mcs)
        print(f"[METACLASS] Intercepted construction layout for class entity: '{name_string}'")
        
        # Enforce that all production class names use standard camel-case formatting
        if not name_string.istitle():
            raise NameError(f"Architecture violation: Class name '{name_string}' must follow strict PascalCase formatting rules.")

        # Verify that classes implementing this metaclass explicitly define a documentation string
        if "__doc__" not in namespace_dict or not namespace_dict["__doc__"].strip():
            raise NotImplementedError(f"Architecture violation: Class '{name_string}' is missing required documentation strings.")

        # Compile and return the validated type into runtime memory
        return super().__new__(mcs, name_string, bases_tuple, namespace_dict)


class BaseMicroservice(metaclass=OperationalContractMeta):
    """Core template class for downstream microservice implementations."""
    pass

if __name__ == "__main__":
    print("[SYSTEM Core] Metaclass verification phase initialized...")
    try:
        # Dynamically trigger class creation to test runtime metaclass validation
        type("invalid_lowercase_service", (BaseMicroservice,), {"__doc__": "Valid text strings."})
    except NameError as failure:
        print(f"[TRAPPED ARCHITECTURE FAULT] System rejected invalid structure: {failure}")