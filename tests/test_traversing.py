import unittest
from dataclasses import dataclass, field
from typing import List

from pylasu.model import Node, pos


@dataclass
class Box(Node):
    name: str = None
    contents: List[Node] = field(default_factory=list)


@dataclass
class Item(Node):
    name: str = None


test_case = Box(
    name="root",
    contents=[
        Box(name="first", contents=[Item(name="1", specified_position=pos(3, 6, 3, 12))],
            specified_position=pos(2, 3, 4, 3)),
        Item(name="2", specified_position=pos(5, 3, 5, 9)),
        Box(
            name="big",
            contents=[
                Box(
                    name="small",
                    contents=[
                        Item(name="3", specified_position=pos(8, 7, 8, 13)),
                        Item(name="4", specified_position=pos(9, 7, 9, 13)),
                        Item(name="5", specified_position=pos(10, 7, 10, 13))
                    ],
                    specified_position=pos(7, 5, 11, 5)
                )
            ],
            specified_position=pos(6, 3, 12, 3)
        ),
        Item(name="6", specified_position=pos(13, 3, 13, 9))
    ],
    specified_position=pos(1, 1, 14, 1)
)


class TraversingTest(unittest.TestCase):
    def test_walk_depth_first(self):
        self.assertEqual(["root", "first", "1", "2", "big", "small", "3", "4", "5", "6"],
                         [n.name for n in test_case.walk()])

    def test_walk_leaves_first(self):
        self.assertEqual(["1", "first", "2", "3", "4", "5", "small", "big", "6", "root"],
                         [n.name for n in test_case.walk_leaves_first()])
