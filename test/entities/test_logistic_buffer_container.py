# test_logistic_buffer_container.py

from draftsman.entity import LogisticBufferContainer, logistic_buffer_containers
from draftsman.errors import InvalidEntityID

from schema import SchemaError

from unittest import TestCase

class LogisticBufferContainerTesting(TestCase):
    def test_default_constructor(self):
        buffer_chest = LogisticBufferContainer()
        hw = buffer_chest.tile_width / 2.0
        hh = buffer_chest.tile_height / 2.0
        self.assertEqual(
            buffer_chest.to_dict(),
            {
                "name": logistic_buffer_containers[0],
                "position": {"x": hw, "y": hh}
            }
        )

    def test_constructor_init(self):
        buffer_chest = LogisticBufferContainer("logistic-chest-buffer", 
            position = [15, 3], bar = 5, 
            connections = {
                "1": {
                    "red": [
                        {"entity_id": "another_entity"},
                        {"entity_id": 2, "circuit_id": 1}
                    ]
                }
            })
        self.assertEqual(
            buffer_chest.to_dict(),
            {
                "name": "logistic-chest-buffer",
                "position": {"x": 15.5, "y": 3.5},
                "bar": 5,
                "connections": {
                    "1": {
                        "red": [
                            {"entity_id": "another_entity"},
                            {"entity_id": 2, "circuit_id": 1}
                        ]
                    }
                }
            }
        )
        buffer_chest = LogisticBufferContainer("logistic-chest-buffer", 
            position = {"x": 15.5, "y": 1.5}, bar = 5,
            tags = {
                "A": "B"
            }
        )
        self.assertEqual(
            buffer_chest.to_dict(),
            {
                "name": "logistic-chest-buffer",
                "position": {"x": 15.5, "y": 1.5},
                "bar": 5,
                "tags": {
                    "A": "B"
                }
            }
        )

        buffer_chest = LogisticBufferContainer(
            request_filters = [
                ("iron-ore", 100)
            ]
        )
        self.assertEqual(
            buffer_chest.to_dict(),
            {
                "name": "logistic-chest-buffer",
                "position": {"x": 0.5, "y": 0.5},
                "request_filters": [
                    {"index": 1, "name": "iron-ore", "count": 100}
                ]
            }
        )
        # TODO
        # storage_chest = LogisticStorageContainer(
        #     request_filters = [
        #         {"index": 1, "name": "iron-ore", "count": 100}
        #     ]
        # )

        # Warnings
        with self.assertWarns(UserWarning):
            LogisticBufferContainer("logistic-chest-buffer", 
                position = [0, 0], invalid_keyword = "100"
            )
        
        # Errors
        # Raises InvalidEntityID when not in containers
        with self.assertRaises(InvalidEntityID):
            LogisticBufferContainer("this is not a logistics storage chest")
        
        # Raises schema errors when any of the associated data is incorrect
        with self.assertRaises(SchemaError):
            LogisticBufferContainer("logistic-chest-buffer", id = 25)

        with self.assertRaises(SchemaError):
            LogisticBufferContainer("logistic-chest-buffer", position = "invalid")

        with self.assertRaises(SchemaError):
            LogisticBufferContainer("logistic-chest-buffer", bar = "not even trying")

        with self.assertRaises(SchemaError):
            LogisticBufferContainer("logistic-chest-buffer", 
                connections = {
                    "this is": ["very", "wrong"]
                }
            )

        with self.assertRaises(SchemaError):
            LogisticBufferContainer("logistic-chest-buffer", 
                request_filters = {
                    "this is": ["very", "wrong"]
                }
            )

    def test_power_and_circuit_flags(self):
        for name in logistic_buffer_containers:
            container = LogisticBufferContainer(name)
            self.assertEqual(container.power_connectable, False)
            self.assertEqual(container.dual_power_connectable, False)
            self.assertEqual(container.circuit_connectable, True)
            self.assertEqual(container.dual_circuit_connectable, False)

    def test_dimensions(self):
        for name in logistic_buffer_containers:
            container = LogisticBufferContainer(name)
            self.assertEqual(container.tile_width, 1)
            self.assertEqual(container.tile_height, 1)