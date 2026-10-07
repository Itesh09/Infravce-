"""Advisories: ingest + match with source precedence."""

from __future__ import annotations

from .ingest import AdvisoryRecord, IngestResult, ingest
from .match import ApplicabilityVote, match_observations

__all__ = ["AdvisoryRecord", "ApplicabilityVote", "IngestResult", "ingest", "match_observations"]
