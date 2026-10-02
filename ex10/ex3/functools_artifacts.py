import functools
import operator
from typing import Any, Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    """Reduce spell powers using the specified operation."""
    operations = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": lambda a, b: a if a > b else b,
        "min": lambda a, b: a if a < b else b,
    }
    return functools.reduce(operations[operation], spells)


def partial_enchanter(
                        base_enchantment: Callable[..., Any]
                        ) -> dict[str, Callable[..., Any]]:
    """Create partial applications for different element enchantments."""
    return {
        'fire_enchant': functools.partial(
            base_enchantment, 50, "Fire"
        ),
        'ice_enchant': functools.partial(
            base_enchantment, 50, "Ice"
        ),
        'lightning_enchant': functools.partial(
            base_enchantment, 50, "Lightning"
        ),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Calculate the nth fibonacci number with memoization."""
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[..., str]:
    """Create a single dispatch spell system."""
    @functools.singledispatch
    def cast(spell):
        return f"Unknown spell type: {type(spell).__name__}"

    @cast.register(int)
    def _(spell):
        return f"Damage spell: {spell} damage dealt"

    @cast.register(str)
    def _(spell):
        return f"Enchantment: {spell} applied"

    @cast.register(list)
    def _(spell):
        return f"Multi-cast: {len(spell)} spells launched"

    return cast


if __name__ == "__main__":
    # Test spell reducer
    powers = [10, 20, 30, 40]
    print("Testing spell reducer...")
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")
    print(f"Min: {spell_reducer(powers, 'min')}")

    # Test partial enchanter
    print("\nTesting partial enchanter...")

    def base_enchant(power: int, element: str, target: str) -> str:
        return f"{element} enchantment ({power} power) on {target}"

    enchants = partial_enchanter(base_enchant)
    print(enchants['fire_enchant']("Sword"))
    print(enchants['ice_enchant']("Shield"))
    print(enchants['lightning_enchant']("Staff"))

    # Test memoized fibonacci
    print("\nTesting memoized fibonacci...")
    print(f"Fib(10): {memoized_fibonacci(10)}")
    print(f"Fib(15): {memoized_fibonacci(15)}")
    print(f"Cache info: {memoized_fibonacci.cache_info()}")

    # Test spell dispatcher
    print("\nTesting spell dispatcher...")
    cast = spell_dispatcher()
    print(cast(42))
    print(cast("Blessing"))
    print(cast(["fire", "ice", "lightning"]))
