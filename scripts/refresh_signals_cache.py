#!/usr/bin/env python3
"""Refresh arXiv signal cache for data-pipeline-lab-site.

Pragmatic v1:
- Fetch newest batch from arXiv API
- Merge incrementally with local cache by paper_id
- Keep rolling 30-day window in cache
- Recompute 7d vs prior 7d metrics
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List

import requests

ROOT = Path(__file__).resolve().parents[2]
CACHE_PATH = ROOT / "data-pipeline-lab-site" / "public" / "signals-cache.json"

KEYWORDS = [
    ("agent", "agentic_systems"),
    ("multi-agent", "agentic_systems"),
    ("rag", "retrieval_knowledge"),
    ("retrieval", "retrieval_knowledge"),
    ("multimodal", "multimodal"),
    ("vision-language", "multimodal"),
    ("transformer", "foundation_models"),
    ("attention", "foundation_models"),
    ("lora", "efficiency_infra"),
    ("quantization", "efficiency_infra"),
    ("alignment", "safety_governance"),
    ("hallucination", "safety_governance"),
]


@dataclass
class Paper:
    paper_id: str
    published: datetime
    text: str


def parse_entries(xml: str) -> List[Paper]:
    entries = re.findall(r"<entry>[\s\S]*?</entry>", xml)
    out: List[Paper] = []
    for entry in entries:
        pid = re.search(r"<id>http://arxiv.org/abs/(.*?)</id>", entry)
        pub = re.search(r"<published>(.*?)</published>", entry)
        title = re.search(r"<title>([\s\S]*?)</title>", entry)
        summary = re.search(r"<summary>([\s\S]*?)</summary>", entry)
        if not (pid and pub):
            continue
        try:
            published = datetime.fromisoformat(pub.group(1).replace("Z", "+00:00"))
        except ValueError:
            continue
        txt = f"{title.group(1) if title else ''} {summary.group(1) if summary else ''}"
        txt = re.sub(r"\s+", " ", txt).lower().strip()
        out.append(Paper(pid.group(1).strip(), published, txt))
    return out


def fetch_recent(max_results: int = 2000) -> List[Paper]:
    query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:stat.ML"
    url = (
        f"https://export.arxiv.org/api/query?search_query={query}"
        f"&sortBy=submittedDate&sortOrder=descending&start=0&max_results={max_results}"
    )
    resp = requests.get(url, timeout=40)
    resp.raise_for_status()
    uniq: Dict[str, Paper] = {}
    for p in parse_entries(resp.text):
        uniq[p.paper_id] = p
    return list(uniq.values())


def compute_items(papers: List[Paper]) -> dict:
    now = datetime.now(timezone.utc)
    start_7 = now - timedelta(days=7)
    start_14 = now - timedelta(days=14)

    p7 = [p for p in papers if p.published >= start_7]
    pprev = [p for p in papers if start_14 <= p.published < start_7]

    items = []
    for keyword, theme in KEYWORDS:
        c7 = sum(1 for p in p7 if keyword in p.text)
        cp = sum(1 for p in pprev if keyword in p.text)
        s7 = c7 / len(p7) if p7 else 0
        sp = cp / len(pprev) if pprev else 0
        growth = (c7 - cp) / max(cp, 1)
        score = 0.6 * growth + 0.4 * (s7 - sp)
        if c7 >= 3 or cp >= 3:
            items.append(
                {
                    "keyword": keyword,
                    "theme": theme,
                    "count7d": c7,
                    "countPrev7d": cp,
                    "share7d": s7,
                    "sharePrev7d": sp,
                    "score": score,
                }
            )

    items.sort(key=lambda r: r["score"], reverse=True)
    return {
        "mode": "cached-arxiv-incremental",
        "updatedAt": now.isoformat(),
        "windows": {
            "current": "last_7d",
            "previous": "prior_7d",
            "papers7d": len(p7),
            "papersPrev7d": len(pprev),
        },
        "items": items[:25],
    }


def main() -> None:
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30)

    existing: Dict[str, Paper] = {}
    if CACHE_PATH.exists():
        cache = json.loads(CACHE_PATH.read_text())
        for p in cache.get("papers", []):
            try:
                existing[p["paper_id"]] = Paper(
                    paper_id=p["paper_id"],
                    published=datetime.fromisoformat(p["published"]),
                    text=p["text"],
                )
            except Exception:
                continue

    recent = fetch_recent(max_results=2000)
    for p in recent:
        existing[p.paper_id] = p

    kept = [p for p in existing.values() if p.published >= cutoff]
    kept.sort(key=lambda p: p.published)

    computed = compute_items(kept)

    payload = {
        **computed,
        "watermark": now.isoformat(),
        "papers": [
            {"paper_id": p.paper_id, "published": p.published.isoformat(), "text": p.text}
            for p in kept
        ],
    }

    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(payload))
    print(f"Updated cache: {CACHE_PATH} | papers_kept={len(kept)} | items={len(payload['items'])}")


if __name__ == "__main__":
    main()
