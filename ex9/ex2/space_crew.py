"""Exercise 2: Space Crew Management - Nested models and complex validation."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    """Enum defining crew member ranks."""

    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    """Pydantic model for an individual crew member.

    This model will be nested inside SpaceMission. Pydantic
    validates nested models recursively: if a CrewMember field
    is invalid, the parent SpaceMission validation also fails,
    with a clear error path pointing to the exact nested field.
    """

    member_id: str = Field(
        ...,
        min_length=3,
        max_length=10,
        description="Unique member identifier",
    )
    name: str = Field(
        ..., min_length=2, max_length=50, description="Full name"
    )
    rank: Rank = Field(..., description="Crew rank")
    age: int = Field(..., ge=18, le=80, description="Age in years")
    specialization: str = Field(
        ..., min_length=3, max_length=30, description="Area of expertise"
    )
    years_experience: int = Field(
        ..., ge=0, le=50, description="Years of experience"
    )
    is_active: bool = Field(
        default=True, description="Whether the member is active"
    )


class SpaceMission(BaseModel):
    """Pydantic model for a space mission with nested crew list.

    Demonstrates how to use List[CrewMember] for nested model
    validation and cross-field rules involving the nested list.
    """

    mission_id: str = Field(
        ...,
        min_length=5,
        max_length=15,
        description="Unique mission identifier",
    )
    mission_name: str = Field(
        ..., min_length=3, max_length=100, description="Mission name"
    )
    destination: str = Field(
        ..., min_length=3, max_length=50, description="Mission destination"
    )
    launch_date: datetime = Field(..., description="Planned launch date")
    duration_days: int = Field(
        ...,
        ge=1,
        le=3650,
        description="Mission duration in days (max 10 years)",
    )
    crew: list[CrewMember] = Field(
        ...,
        min_length=1,
        max_length=12,
        description="List of crew members (1-12)",
    )
    mission_status: str = Field(
        default="planned", description="Current mission status"
    )
    budget_millions: float = Field(
        ..., ge=1.0, le=10000.0, description="Budget in millions of dollars"
    )

    @model_validator(mode="after")
    def validate_mission_rules(self) -> SpaceMission:
        """Validate mission-level business rules."""
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        leadership_ranks = {Rank.COMMANDER, Rank.CAPTAIN}
        has_leader = any(
            member.rank in leadership_ranks for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            experienced = sum(
                1 for member in self.crew if member.years_experience >= 5
            )
            ratio = experienced / len(self.crew)
            if ratio < 0.5:
                raise ValueError(
                    "Long missions (> 365 days) require at "
                    "least 50% experienced crew (5+ years)"
                )
        inactive = [
            member.name for member in self.crew if not member.is_active
        ]
        if inactive:
            raise ValueError(
                f"All crew must be active. Inactive: {', '.join(inactive)}"
            )

        return self


def main() -> None:
    """Demonstrate SpaceMission model creation and validation."""
    print("Space Mission Crew Validation")
    print("=" * 40)
    crew = [
        CrewMember(
            member_id="SC001",
            name="Sarah Connor",
            rank="commander",
            age=45,
            specialization="Mission Command",
            years_experience=20,
        ),
        CrewMember(
            member_id="SC002",
            name="John Smith",
            rank="lieutenant",
            age=35,
            specialization="Navigation",
            years_experience=10,
        ),
        CrewMember(
            member_id="SC003",
            name="Alice Johnson",
            rank="officer",
            age=28,
            specialization="Engineering",
            years_experience=6,
        ),
    ]

    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date="2025-06-15T08:00:00",
        duration_days=900,
        crew=crew,
        budget_millions=2500.0,
    )

    print("Valid mission created:")
    print(f"  Mission: {mission.mission_name}")
    print(f"  ID: {mission.mission_id}")
    print(f"  Destination: {mission.destination}")
    print(f"  Duration: {mission.duration_days} days")
    print(f"  Budget: ${mission.budget_millions}M")
    print(f"  Crew size: {len(mission.crew)}")
    print("  Crew members:")
    for member in mission.crew:
        print(
            f"  - {member.name} ({member.rank.value}) - "
            f"{member.specialization}"
        )

    print()
    print("=" * 40)
    print("Expected validation error:")
    try:
        SpaceMission(
            mission_id="M2024_MOON",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date="2025-01-01T12:00:00",
            duration_days=30,
            crew=[
                CrewMember(
                    member_id="CM001",
                    name="Bob Ross",
                    rank="cadet",
                    age=22,
                    specialization="Geology",
                    years_experience=1,
                )
            ],
            budget_millions=100.0,
        )
    except ValidationError as e:
        for error in e.errors():
            print(f"  {error['msg']}")


if __name__ == "__main__":
    main()
