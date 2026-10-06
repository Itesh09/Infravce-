"""Queryable persistence for observations, applicability votes, and coverage."""

from __future__ import annotations

from infravce.store.observations import SCHEMA_VERSION, ObservationStore

__all__ = ["SCHEMA_VERSION", "ObservationStore"]
