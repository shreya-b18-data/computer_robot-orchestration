"""Dual-channel communication layer (in-memory simulation).

Two independent channels:
  - robot-to-robot  (peer messages, e.g. handshakes, intent sharing)
  - robot-to-PC     (reports to / commands from the central controller)
Each channel can drop messages with a given probability to model unreliable links.
"""
import random
from collections import deque
from dataclasses import dataclass, field


@dataclass
class Message:
    sender: str
    receiver: str
    kind: str
    payload: dict = field(default_factory=dict)


class Channel:
    def __init__(self, name, drop_prob=0.0, seed=0):
        self.name = name
        self.drop_prob = drop_prob
        self.rng = random.Random(seed)
        self.inboxes = {}
        self.sent = 0
        self.dropped = 0

    def register(self, node_id):
        self.inboxes.setdefault(node_id, deque())

    def send(self, msg):
        """Deliver a message. Returns True if delivered, False if dropped."""
        if msg.receiver not in self.inboxes:
            raise KeyError(f"{msg.receiver!r} is not registered on channel {self.name!r}")
        self.sent += 1
        if self.rng.random() < self.drop_prob:
            self.dropped += 1
            return False
        self.inboxes[msg.receiver].append(msg)
        return True

    def receive_all(self, node_id):
        """Return and clear all pending messages for a node."""
        box = self.inboxes[node_id]
        messages = list(box)
        box.clear()
        return messages


class CommsHub:
    """Holds both channels so robots and the PC register once and use either."""

    def __init__(self, robot_ids, pc_id="pc", drop_robot=0.0, drop_pc=0.0, seed=0):
        self.robot_to_robot = Channel("robot-robot", drop_robot, seed)
        self.robot_to_pc = Channel("robot-pc", drop_pc, seed + 1)
        for rid in robot_ids:
            self.robot_to_robot.register(rid)
            self.robot_to_pc.register(rid)
        self.robot_to_pc.register(pc_id)
        self.pc_id = pc_id
