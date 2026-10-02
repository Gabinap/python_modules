from typing import Any, Callable


def spell_combiner(
                    spell1: Callable[..., Any], spell2: Callable[..., Any]
                    ) -> Callable[..., tuple[Any, Any]]:
    """Combine two spells into one that returns a tuple of both results."""
    def combined(*args, **kwargs):
        return (spell1(*args, **kwargs), spell2(*args, **kwargs))
    return combined


def power_amplifier(
                    base_spell: Callable[..., Any], multiplier: int
                    ) -> Callable[..., Any]:
    """Amplify a spell's numerical result by a multiplier."""
    def amplified(*args, **kwargs):
        return base_spell(*args, **kwargs) * multiplier
    return amplified


def conditional_caster(
                        condition: Callable[..., bool],
                        spell: Callable[..., Any]
                        ) -> Callable[..., Any]:
    """Cast spell only if condition returns True."""
    def caster(*args, **kwargs):
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"
    return caster


def spell_sequence(
                    spells: list[Callable[..., Any]]
                    ) -> Callable[..., list[Any]]:
    """Create a function that casts all spells in order."""
    def sequence(*args, **kwargs):
        return [spell(*args, **kwargs) for spell in spells]
    return sequence


if __name__ == "__main__":
    # Test spell combiner
    print("Testing spell combiner...")

    def fireball(target):
        return f"Fireball hits {target}"

    def heal(target):
        return f"Heals {target}"

    combined = spell_combiner(fireball, heal)
    result = combined("Dragon")
    print(f"Combined spell result: {result[0]}, {result[1]}")

    # Test power amplifier
    print("\nTesting power amplifier...")

    def base_damage(power):
        return power

    mega_spell = power_amplifier(base_damage, 3)
    print(f"Original: {base_damage(10)}, Amplified: {mega_spell(10)}")

    # Test conditional caster
    print("\nTesting conditional caster...")

    def has_mana(power):
        return power > 5

    def attack(power):
        return f"Attack with {power} power"

    safe_attack = conditional_caster(has_mana, attack)
    print(safe_attack(10))
    print(safe_attack(3))

    # Test spell sequence
    print("\nTesting spell sequence...")

    def shield(target):
        return f"Shield on {target}"

    sequence = spell_sequence([fireball, heal, shield])
    print(sequence("Ally"))
