from pathlib import Path
import tempfile
import json
from infravce.advisories.ingest import ingest


def test_ingest_loads_list():
    data = [{"advisory_id": "CVE-TEST", "product": "foo", "versions": ["1.0.0"]}]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "adv.json"
        p.write_text(json.dumps(data))
        res = ingest(p)
        assert len(res.records) == 1


def test_ingest_loads_cases():
    data = {"cases": [{"cve_id": "CVE-X", "product": "bar", "version": "2.0.0"}]}
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "cases.json"
        p.write_text(json.dumps(data))
        res = ingest(p)
        assert len(res.records) == 1
