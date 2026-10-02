import functools
import time
from typing import Any, Callable


def spell_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator that measures function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper


def power_validator(
        min_power: int
        ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator factory that validates power levels."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'power' in kwargs:
                power = kwargs['power']
            else:
                int_args = [
                    a for a in args if isinstance(a, (int, float))
                ]
                power = int_args[-1] if int_args else 0
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(
        max_attempts: int
        ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator that retries failed spells."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying... "
                        f"(attempt {attempt}/{max_attempts})"
                    )
            return (
                f"Spell casting failed after {max_attempts} attempts"
            )
        return wrapper
    return decorator


class MageGuild:
    """A guild of mages demonstrating staticmethod and decorators."""

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Check if a mage name is valid."""
        return len(name) >= 3 and all(
            c.isalpha() or c == ' ' for c in name
        )

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        """Cast a spell with the given name and power."""
        return f"Successfully cast {spell_name} with {power} power"


if __name__ == "__main__":
    # Test spell timer
    print("Testing spell timer...")

    @spell_timer
    def fireball():
        time.sleep(0.1)
        return "Fireball cast!"

    result = fireball()
    print(f"Result: {result}")

    # Test power validator
    print("\nTesting power validator...")

    @power_validator(min_power=20)
    def mega_spell(power: int) -> str:
        return f"Mega spell with {power} power!"

    print(mega_spell(25))
    print(mega_spell(5))

    # Test retry spell
    print("\nTesting retry spell...")
    state = {'count': 0}

    @retry_spell(max_attempts=3)
    def unstable_spell():
        state['count'] += 1
        if state['count'] < 3:
            raise ValueError("Spell unstable!")
        return "Spell succeeded!"

    print(unstable_spell())

    # Test MageGuild
    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Gandalf"))
    print(MageGuild.validate_mage_name("A1"))

    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Thunder", 5))
