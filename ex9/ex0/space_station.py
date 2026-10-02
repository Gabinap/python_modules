"""Exercise 0: Space Station Data.

Basic Pydantic model with Field validation.
"""

from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    """Pydantic model representing a space station with validated fields.

    BaseModel is the foundation class of Pydantic. Every field declared
    with a type annotation is automatically validated when you create
    an instance. Field() lets you add extra constraints like min/max
    length or value ranges.
    """

    station_id: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Unique station identifier",
    )
    name: str = Field(
        ..., min_length=1, max_length=50, description="Station name"
    )
    crew_size: int = Field(
        ..., ge=1, le=20, description="Number of crew members (1-20)"
    )
    power_level: float = Field(
        ..., ge=0.0, le=100.0, description="Power level in percent"
    )
    oxygen_level: float = Field(
        ..., ge=0.0, le=100.0, description="Oxygen level in percent"
    )
    last_maintenance: datetime = Field(
        ..., description="Date of last maintenance"
    )
    is_operational: bool = Field(
        default=True, description="Whether the station is operational"
    )
    notes: str | None = Field(
        default=None,
        max_length=200,
        description="Optional notes about the station",
    )


def main() -> None:
    """Demonstrate SpaceStation model creation and validation."""
    print("Space Station Data Validation")
    print("=" * 40)
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance="2024-01-15T10:30:00",
        is_operational=True,
        notes="All systems nominal",
    )

    print("Valid station created:")
    print(f"  ID: {station.station_id}")
    print(f"  Name: {station.name}")
    print(f"  Crew: {station.crew_size} people")
    print(f"  Power: {station.power_level}%")
    print(f"  Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Offline"
    print(f"  Status: {status}")

    print()
    print("=" * 40)
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="BAD01",
            name="Overcrowded Station",
            crew_size=25,
            power_level=50.0,
            oxygen_level=40.0,
            last_maintenance="2024-06-01T00:00:00",
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"  {error['msg']}")


if __name__ == "__main__":
    main()
