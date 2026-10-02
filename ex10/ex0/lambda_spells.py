def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort magical artifacts by power level in descending order."""
    return sorted(artifacts, key=lambda a: a['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    """Filter mages by minimum power level."""
    return list(filter(lambda m: m['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """Transform spell names with magical decorations."""
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Calculate statistics about mage power levels."""
    max_power = max(mages, key=lambda m: m['power'])['power']
    min_power = min(mages, key=lambda m: m['power'])['power']
    avg_power = round(
        sum(map(lambda m: m['power'], mages)) / len(mages), 2
    )
    return {
        'max_power': max_power,
        'min_power': min_power,
        'avg_power': avg_power
    }


if __name__ == "__main__":
    # Test artifact sorter
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'divination'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'offensive'},
        {'name': 'Healing Ring', 'power': 60, 'type': 'support'},
    ]
    print("Testing artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']} ({sorted_artifacts[0]['power']}"
        f" power) comes before {sorted_artifacts[1]['name']}"
        f" ({sorted_artifacts[1]['power']} power)"
    )

    # Test power filter
    mages = [
        {'name': 'Alex', 'power': 75, 'element': 'fire'},
        {'name': 'Jordan', 'power': 90, 'element': 'ice'},
        {'name': 'Riley', 'power': 60, 'element': 'earth'},
    ]
    print("\nTesting power filter...")
    strong_mages = power_filter(mages, 70)
    for mage in strong_mages:
        print(f"{mage['name']} (power: {mage['power']})")

    # Test spell transformer
    spells = ["fireball", "heal", "shield"]
    print("\nTesting spell transformer...")
    transformed = spell_transformer(spells)
    print(" ".join(transformed))

    # Test mage stats
    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Avg power: {stats['avg_power']}")
