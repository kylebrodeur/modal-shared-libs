"""Contract tests for the shared hooks seam: THE family integration contract.

Covers: closed tag set (unknown refuses, decorator + manual share one
registry), ordered multi-registration, contained + reported errors, scoped
registration helper, clear() semantics.
"""

from __future__ import annotations

import pytest

from libs.hooks import Hooks, registered

TAGS = ("a.pre", "a.post", "b.post")


@pytest.fixture
def hooks() -> Hooks:
    return Hooks(TAGS, name="test")


class TestRegistry:
    def test_unknown_tag_refuses(self, hooks: Hooks) -> None:
        with pytest.raises(ValueError, match="unknown hook tag"):
            hooks.register("not.a.tag", lambda: None)
        with pytest.raises(ValueError, match="unknown hook tag"):
            hooks.on("not.a.tag")
        with pytest.raises(ValueError, match="unknown hook tag"):
            hooks.fire("not.a.tag")

    def test_decorator_and_manual_share_registry(self, hooks: Hooks) -> None:
        calls: list[str] = []

        @hooks.on("a.pre")
        def lane_fn(value: str) -> None:
            calls.append(value)

        assert hooks.registrations("a.pre") == [lane_fn]
        hooks.register("a.pre", lambda v: calls.append(v + "-2"))
        hooks.fire("a.pre", "x")
        assert calls == ["x", "x-2"]

    def test_fire_order_is_registration_order_and_errors_returned(self, hooks: Hooks) -> None:
        calls: list[str] = []

        def first(v: str) -> None:
            calls.append("first:" + v)

        def broken(v: str) -> None:
            raise RuntimeError("lane exploded")

        def third(v: str) -> None:
            calls.append("third:" + v)

        hooks.register("a.post", first)
        hooks.register("a.post", broken)
        hooks.register("a.post", third)
        errors = hooks.fire("a.post", "v")
        # all handlers ran; the broken one is contained
        assert calls == ["first:v", "third:v"]
        assert len(errors) == 1
        assert "first: " not in errors[0] and "broken" in errors[0] and "RuntimeError" in errors[0]
        assert hooks.last_errors("a.post") == errors

    def test_last_errors_empty_on_clean_fire(self, hooks: Hooks) -> None:
        hooks.register("b.post", lambda: None)
        hooks.fire("b.post")
        assert hooks.last_errors("b.post") == []

    def test_registrations_is_a_copy(self, hooks: Hooks) -> None:
        hooks.register("a.pre", lambda: None)
        grabbed = hooks.registrations("a.pre")
        grabbed.clear()
        assert hooks.registrations("a.pre") != []

    def test_clear_one_tag_or_all(self, hooks: Hooks) -> None:
        hooks.register("a.pre", lambda: None)
        hooks.register("a.post", lambda: None)
        hooks.clear("a.pre")
        assert hooks.registrations("a.pre") == [] and hooks.registrations("a.post") != []
        hooks.clear()
        assert hooks.registrations("a.post") == []


class TestScopedRegistration:
    def test_registered_context_manages_membership(self, hooks: Hooks) -> None:
        fn = lambda: None  # noqa: E731
        with registered(hooks, "b.post", fn):
            assert hooks.registrations("b.post") == [fn]
        assert hooks.registrations("b.post") == []

    def test_registered_survives_handler_error(self, hooks: Hooks) -> None:
        fn = lambda: None  # noqa: E731
        with pytest.raises(RuntimeError), registered(hooks, "b.post", fn):
            assert hooks.registrations("b.post") == [fn]
            raise RuntimeError("scope unwinds")
        assert hooks.registrations("b.post") == []


class TestConsumerIsolation:
    def test_two_instances_are_independent(self, hooks: Hooks) -> None:
        other = Hooks(TAGS, name="other")
        hooks.register("a.pre", lambda: None)
        assert other.registrations("a.pre") == []
        other.fire("a.pre")
        assert other.last_errors("a.pre") == []
        assert hooks.last_errors("a.pre") == []  # separate error memory too
