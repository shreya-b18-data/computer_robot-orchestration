import pytest

from src.comms import Channel, CommsHub, Message


def test_message_delivered():
    ch = Channel("test")
    ch.register("a")
    ch.register("b")
    assert ch.send(Message("a", "b", "hello", {"x": 1}))
    msgs = ch.receive_all("b")
    assert len(msgs) == 1 and msgs[0].payload == {"x": 1}
    assert ch.receive_all("b") == []  # inbox cleared after reading


def test_unregistered_receiver_raises():
    ch = Channel("test")
    ch.register("a")
    with pytest.raises(KeyError):
        ch.send(Message("a", "ghost", "hi"))


def test_full_drop_loses_everything():
    ch = Channel("lossy", drop_prob=1.0)
    ch.register("a")
    ch.register("b")
    assert not ch.send(Message("a", "b", "hi"))
    assert ch.dropped == 1 and ch.receive_all("b") == []


def test_channels_are_independent():
    hub = CommsHub(["r1", "r2"], drop_robot=1.0, drop_pc=0.0)
    hub.robot_to_robot.send(Message("r1", "r2", "handshake"))
    hub.robot_to_pc.send(Message("r1", "pc", "status"))
    assert hub.robot_to_robot.receive_all("r2") == []  # robot link is down
    assert len(hub.robot_to_pc.receive_all("pc")) == 1  # PC link still works