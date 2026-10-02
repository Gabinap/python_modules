"""Exercise 1: Alien Contact Logs - Custom validation with model_validator."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    """Enum defining the types of alien contact.

    Inheriting from both str and Enum makes the enum JSON-serializable
    and allows direct string comparison. Pydantic recognizes this
    pattern and validates that only these values are accepted.
    """

    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    """Pydantic model for alien contact reports with custom validation.

    The @model_validator decorator lets you define validation logic
    that involves multiple fields at once (cross-field validation).
    This is impossible with simple Field() constraints alone.
    """

    contact_id: str = Field(
        ...,
        min_length=5,
        max_length=15,
        description="Unique contact identifier",
    )
    timestamp: datetime = Field(..., description="Date and time of contact")
    location: str = Field(
        ..., min_length=3, max_length=100, description="Location of contact"
    )
    contact_type: ContactType = Field(..., description="Type of contact")
    signal_strength: float = Field(
        ..., ge=0.0, le=10.0, description="Signal strength (0-10 scale)"
    )
    duration_minutes: int = Field(
        ..., ge=1, le=1440, description="Duration in minutes (max 24 hours)"
    )
    witness_count: int = Field(
        ..., ge=1, le=100, description="Number of witnesses"
    )
    message_received: str | None = Field(
        default=None, max_length=500, description="Optional received message"
    )
    is_verified: bool = Field(
        default=False, description="Whether the contact is verified"
    )

    @model_validator(mode="after")
    def validate_contact_rules(self) -> "AlienContact":
        """Apply business rules that depend on multiple fields.

        mode='after' means this runs after all individual field
        validations pass. We have access to the fully typed model.
        """
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include a message")

        return self


def main() -> None:
    """Demonstrate AlienContact model creation and validation."""
    print("Alien Contact Log Validation")
    print("=" * 40)
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp="2024-03-15T22:30:00",
        location="Area 51, Nevada",
        contact_type="radio",
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
        is_verified=True,
    )

    print("Valid contact report:")
    print(f"  ID: {contact.contact_id}")
    print(f"  Type: {contact.contact_type.value}")
    print(f"  Location: {contact.location}")
    print(f"  Signal: {contact.signal_strength}/10")
    print(f"  Duration: {contact.duration_minutes} minutes")
    print(f"  Witnesses: {contact.witness_count}")
    print(f"  Message: '{contact.message_received}'")

    print()
    print("=" * 40)
    print("Expected validation error:")
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp="2024-04-01T03:00:00",
            location="Roswell, New Mexico",
            contact_type="telepathic",
            signal_strength=3.0,
            duration_minutes=10,
            witness_count=1,
            is_verified=False,
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"  {error['msg']}")


if __name__ == "__main__":
    main()
