from typing import Any, Callable


def mage_counter() -> Callable[[], int]:
    """Create a counting closure that tracks call count."""
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count
    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    """Create a power accumulator starting from initial_power."""
    total = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total
    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    """Create enchantment functions with a fixed enchantment type."""
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"
    return enchant


def memory_vault() -> dict[str, Callable[..., Any]]:
    """Create a memory management system using closures."""
    memories = {}

    def store(key: str, value) -> None:
        memories[key] = value

    def recall(key: str):
        return memories.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


if __name__ == "__main__":
    # Test mage counter
    print("Testing mage counter...")
    counter = mage_counter()
    print(f"Call 1: {counter()}")
    print(f"Call 2: {counter()}")
    print(f"Call 3: {counter()}")

    # Test spell accumulator
    print("\nTesting spell accumulator...")
    acc = spell_accumulator(100)
    print(f"Add 20: {acc(20)}")
    print(f"Add 30: {acc(30)}")
    print(f"Add 50: {acc(50)}")

    # Test enchantment factory
    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    # Test memory vault
    print("\nTesting memory vault...")
    vault = memory_vault()
    vault['store']("spell_1", "Fireball")
    vault['store']("spell_2", "Ice Storm")
    print(vault['recall']("spell_1"))
    print(vault['recall']("spell_2"))
    print(vault['recall']("spell_3"))
