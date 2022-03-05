# test_arithmetic_combinator.py

from draftsman.constants import Direction
from draftsman.entity import DeciderCombinator, decider_combinators
from draftsman.errors import InvalidEntityID, InvalidSignalID, InvalidConditionOperation

from schema import SchemaError

from unittest import TestCase

class DeciderCombinatorTesting(TestCase):
    def test_default_constructor(self):
        combinator = DeciderCombinator()
        self.assertEqual(
            combinator.to_dict(),
            {
                "name": "decider-combinator",
                "position": {"x": 0.5, "y": 1.0}
            }
        )

    def test_constructor_init(self):
        combinator = DeciderCombinator(
            "decider-combinator",
            position = [3, 3],
            direction = Direction.EAST,
            control_behavior = {
                "decider_conditions": {
                    "first_constant": 10,
                    "second_constant": 10
                }
            }
        )
        self.assertEqual(
            combinator.to_dict(),
            {
                "name": "decider-combinator",
                "position": {"x": 4.0, "y": 3.5},
                "direction": 2,
                "control_behavior": {
                    "decider_conditions": {
                        "first_constant": 10,
                        "second_constant": 10
                    }
                }
            }
        )

        combinator = DeciderCombinator(
            "decider-combinator",
            position = [3, 3],
            direction = Direction.EAST,
            control_behavior = {
                "decider_conditions": {
                    "first_signal": "signal-A",
                    "comparator": ">=",
                    "second_signal": "signal-B"
                }
            }
        )
        self.assertEqual(
            combinator.to_dict(),
            {
                "name": "decider-combinator",
                "position": {"x": 4.0, "y": 3.5},
                "direction": 2,
                "control_behavior": {
                    "decider_conditions": {
                        "first_signal": {
                            "name": "signal-A",
                            "type": "virtual"
                        },
                        "comparator": "≥",
                        "second_signal": {
                            "name": "signal-B",
                            "type": "virtual"
                        }
                    }
                }
            }
        )

        combinator = DeciderCombinator(
            "decider-combinator",
            position = [3, 3],
            direction = Direction.EAST,
            control_behavior = {
                "decider_conditions": {
                    "first_signal": {
                        "name": "signal-A",
                        "type": "virtual"
                    },
                    "comparator": "<=",
                    "second_signal": {
                        "name": "signal-B",
                        "type": "virtual"
                    }
                }
            }
        )
        self.maxDiff = None
        self.assertEqual(
            combinator.to_dict(),
            {
                "name": "decider-combinator",
                "position": {"x": 4.0, "y": 3.5},
                "direction": 2,
                "control_behavior": {
                    "decider_conditions": {
                        "first_signal": {
                            "name": "signal-A",
                            "type": "virtual"
                        },
                        "comparator": "≤",
                        "second_signal": {
                            "name": "signal-B",
                            "type": "virtual"
                        }
                    }
                }
            }
        )

        # Warnings
        with self.assertWarns(UserWarning):
            DeciderCombinator(unused_keyword = "whatever")

        # Errors
        with self.assertRaises(InvalidEntityID):
            DeciderCombinator("this is not an arithmetic combinator")

    def test_flags(self):
        for name in decider_combinators:
            combinator = DeciderCombinator(name)
            self.assertEqual(combinator.power_connectable, False)
            self.assertEqual(combinator.dual_power_connectable, False)
            self.assertEqual(combinator.circuit_connectable, True)
            self.assertEqual(combinator.dual_circuit_connectable, True)

    def test_dimensions(self):
        combinator = DeciderCombinator()
        self.assertEqual(combinator.tile_width, 1)
        self.assertEqual(combinator.tile_height, 2)

    def test_set_decider_conditions(self):
        combinator = DeciderCombinator()
        combinator.set_decider_conditions("signal-A", ">", "iron-ore")
        self.maxDiff = None
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "first_signal": {
                        "name": "signal-A",
                        "type": "virtual"
                    },
                    "comparator": ">",
                    "second_signal": {
                        "name": "iron-ore",
                        "type": "item"
                    }
                }
            }
        )
        combinator.set_decider_conditions("signal-A", "=", "copper-ore", "signal-B")
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "first_signal": {
                        "name": "signal-A",
                        "type": "virtual"
                    },
                    "comparator": "=",
                    "second_signal": {
                        "name": "copper-ore",
                        "type": "item"
                    },
                    "output_signal": {
                        "name": "signal-B",
                        "type": "virtual"
                    }
                }
            }
        )
        combinator.set_decider_conditions(10, "<=", 100, "signal-C")
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "first_constant": 10,
                    "comparator": "≤",
                    "second_constant": 100,
                    "output_signal": {
                        "name": "signal-C",
                        "type": "virtual"
                    }
                }
            }
        )

        combinator.set_decider_conditions(None, None, None, None)
        self.assertEqual(
            combinator.control_behavior, 
            {
                "decider_conditions": {}
            }
        )

        combinator.set_decider_conditions(None)
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "comparator": "<",
                    "second_constant": 0
                }
            }
        )

        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions(TypeError)
        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions("incorrect")
        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions("signal-A", "incorrect", "signal-D")
        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions("signal-A", "<", TypeError)
        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions("signal-A", "<", "incorrect")
        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions("signal-A", "<", "signal-D", TypeError)
        with self.assertRaises(SchemaError):
            combinator.set_decider_conditions("signal-A", "<", "signal-D", "incorrect")

        # TODO:
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "comparator": "<",
                    "second_constant": 0
                }
            }
        )

        # Test Remove conditions
        combinator.remove_decider_conditions()
        self.assertEqual(combinator.control_behavior, {})

        # Test set_copy_count
        combinator.set_copy_count_from_input(True)
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "copy_count_from_input": True
                }
            }
        )
        combinator.set_copy_count_from_input(False)
        self.assertEqual(
            combinator.control_behavior,
            {
                "decider_conditions": {
                    "copy_count_from_input": False
                }
            }
        )
        combinator.set_copy_count_from_input(None)
        self.assertEqual( # maybe should be == {}?
            combinator.control_behavior,
            {
                "decider_conditions": {}
            }
        )