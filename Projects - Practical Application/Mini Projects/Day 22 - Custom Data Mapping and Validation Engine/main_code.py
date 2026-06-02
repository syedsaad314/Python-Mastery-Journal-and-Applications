"""
System: Custom Data Mapping and Validation Engine
Description: A production-grade object relational data mapper that uses property descriptors 
             to enforce strict runtime data validation and schema mapping.
Lead Engineer: Syed Saad Bin Irfan
"""

import re
from typing import Dict, Any, List

class DataTypeFieldDescriptor:
    """Base descriptor class that handles state mappings and type tracking."""
    def __init__(self, required_type: type, fallback_default: Any = None) -> None:
        self.expected_type: type = required_type
        self.default: Any = fallback_default
        self.inner_key: str = ""

    def __set_name__(self, owner_class: type, name_string: str) -> None:
        self.inner_key = f"_field_property_{name_string}"

    def __get__(self, instance: object, owner_class: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.inner_key, self.default)

    def __set__(self, instance: object, value: Any) -> None:
        if value is None and self.default is not None:
            value = self.default
            
        if value is not None and not isinstance(value, self.expected_type):
            raise TypeError(f"Schema mapping error: Field validation failed. Expected {self.expected_type}, received {type(value)}")
        setattr(instance, self.inner_key, value)


class RegexValidatedStringField(DataTypeFieldDescriptor):
    """Extended descriptor that enforces custom regular expression pattern checks on string attributes."""
    def __init__(self, regex_pattern_string: str, fallback_default: str = "") -> None:
        super().__init__(required_type=str, fallback_default=fallback_default)
        self.compiled_regex = re.compile(regex_pattern_string)

    def __set__(self, instance: object, value: Any) -> None:
        # First verify the basic data type rules match successfully
        super().__set__(instance, value)
        if value is not None:
            if not self.compiled_regex.match(value):
                raise ValueError(f"Schema mapping error: Content payload '{value}' violates regex constraint pattern.")


class ModelValidationSchemaMeta(type):
    """Metaclass that extracts field definition configurations to generate model schemas."""
    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        registered_model_fields: List[str] = []
        
        # Identify all declared descriptor fields inside the class namespace
        for key, attribute in namespace.items():
            if isinstance(attribute, DataTypeFieldDescriptor):
                registered_model_fields.append(key)
                
        # Inject the parsed fields registry directly back into the class metadata map
        namespace["_schema_fields_registry"] = registered_model_fields
        return super().__new__(mcs, name, bases, namespace)


class EntityDataModel(metaclass=ModelValidationSchemaMeta):
    """Base model class providing automated dictionary exports and structured data initialization."""
    _schema_fields_registry: List[str] = []

    def __init__(self, **kwargs: Any) -> None:
        # Populate incoming properties using the model's schema registry fields
        for field_key in self._schema_fields_registry:
            passed_value = kwargs.get(field_key, None)
            setattr(self, field_key, passed_value)

    def export_to_dict(self) -> Dict[str, Any]:
        """Serializes the class attributes into a clean, flat dictionary payload."""
        return {field: getattr(self, field) for field in self._schema_fields_registry}


# --- Target Data Model Implementations ---
class UserAccountProfileModel(EntityDataModel):
    """An enterprise account data model that validates field constraints at runtime."""
    account_id = DataTypeFieldDescriptor(required_type=int)
    email_address = RegexValidatedStringField(regex_pattern_string=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    system_tier_rank = DataTypeFieldDescriptor(required_type=str, fallback_default="STANDARD_CLIENT")

if __name__ == "__main__":
    print("\n=== STARTING CUSTOM DATA MAPPING AND VALIDATION ENGINE ===\n")

    # Build an instance using clean, verified configuration parameters
    valid_user = UserAccountProfileModel(
        account_id=202611, 
        email_address="saad.irfan@ubit.edu.pk",
        system_tier_rank="STAFF_DIRECTOR"
    )
    print(f"[MODEL REGISTRY] Successfully mapped record data payload: {valid_user.export_to_dict()}")

    print("\n--- INJECTING INVALID DATATYPE TO TRIGGER DEFENSES ---")
    try:
        # Pass an invalid data type to verify model field security rules
        invalid_user = UserAccountProfileModel(account_id="NOT_AN_INTEGER", email_address="test@domain.com")
    except TypeError as type_failure:
        print(f"[SECURITY GUARD ACTIVE] Blocked typing violation: {type_failure}")

    print("\n--- INJECTING INVALID REGEX STRING TO TRIGGER DEFENSES ---")
    try:
        # Pass an invalid email address format to verify regex pattern defenses
        faulty_email_user = UserAccountProfileModel(account_id=505, email_address="malformed_email_identity_string")
    except ValueError as validation_failure:
        print(f"[SECURITY GUARD ACTIVE] Blocked malformed string content: {validation_failure}")