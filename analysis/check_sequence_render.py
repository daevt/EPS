"""Audit final native sequence-render DOM without changing diagram sources.

Run after render_diagrams.cjs has rendered every current manifest entry.
Only Sequence_Render_Validation.json is written. Uses Python's stdlib only.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import html
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

HERE = Path(__file__).resolve().parent
INTERSECTION_TOLERANCE = 1.0
NEAR_LABEL_GAP = 8.0
MIN_ARROW_ROW_GAP = 60.0


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def clean_label(value):
    return re.sub(r"<[^>]*>", " ", html.unescape(str(value or ""))).strip()


def style_dict(value):
    return dict(part.split("=", 1) for part in str(value).split(";") if "=" in part)


def valid_box(box):
    return (isinstance(box, dict) and all(numeric(box.get(key)) for key in ("x", "y", "w", "h"))
            and box["w"] > 0 and box["h"] > 0)


def box_intersection(left, right):
    return (min(left["x"] + left["w"], right["x"] + right["w"]) - max(left["x"], right["x"]),
            min(left["y"] + left["h"], right["y"] + right["h"]) - max(left["y"], right["y"]))


def vertical_gap(left, right):
    if left["y"] + left["h"] <= right["y"]:
        return right["y"] - left["y"] - left["h"]
    if right["y"] + right["h"] <= left["y"]:
        return left["y"] - right["y"] - right["h"]
    return -min(left["y"] + left["h"], right["y"] + right["h"]) + max(left["y"], right["y"])


def point_list(edge):
    return [point for point in edge.get("points", [])
            if isinstance(point, dict) and numeric(point.get("x")) and numeric(point.get("y"))]


def arrow_y(edge):
    points = point_list(edge)
    return sum(point["y"] for point in points) / len(points) if points else None


def segment_hits_box(start, end, box, inset=INTERSECTION_TOLERANCE):
    """Liang–Barsky clipping against the open-ish interior of a label box."""
    xmin, xmax = box["x"] + inset, box["x"] + box["w"] - inset
    ymin, ymax = box["y"] + inset, box["y"] + box["h"] - inset
    if xmax <= xmin or ymax <= ymin:
        return False
    dx, dy = end["x"] - start["x"], end["y"] - start["y"]
    low, high = 0.0, 1.0
    for p, q in ((-dx, start["x"] - xmin), (dx, xmax - start["x"]),
                 (-dy, start["y"] - ymin), (dy, ymax - start["y"])):
        if abs(p) < 1e-9:
            if q < 0:
                return False
            continue
        ratio = q / p
        if p < 0:
            low = max(low, ratio)
        else:
            high = min(high, ratio)
        if low > high:
            return False
    return True


def audit(manifest_path, output_path, required_views):
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    base = manifest_path.parent
    entries = manifest.get("diagrams", [])
    issues = []
    views = []

    def issue(severity, code, view_id, detail, **extra):
        issues.append({"severity": severity, "code": code, "view_id": view_id, "detail": detail, **extra})

    if len(entries) != required_views or manifest.get("view_count") != required_views:
        issue("error", "VIEW_COUNT", None,
              f"Expected {required_views} final views; manifest has {len(entries)} entries and view_count={manifest.get('view_count')}.")
    ids = [entry.get("id") for entry in entries]
    if len(ids) != len(set(ids)):
        issue("error", "DUPLICATE_VIEW_ID", None, "Manifest view IDs are not unique.")
    known_ids = set(ids)
    totals = {"source_sha256_matches": 0, "dom_files_available": 0,
              "expected_edges": 0, "native_edges_with_paths": 0, "message_labels": 0,
              "intersecting_label_pairs": 0, "near_label_pairs": 0,
              "label_crossed_by_other_message": 0}

    for entry in entries:
        uid = entry["id"]
        source = base / entry["filename"]
        dom_path = base / ".render-cache" / "dom" / (source.stem + ".dom.json")
        result = {"id": uid, "logical_id": entry.get("logical_id"), "source": str(source),
                  "dom": str(dom_path), "sha256_match": False, "expected_edges": 0,
                  "native_edges_with_paths": 0, "message_labels": 0,
                  "min_label_width": None, "max_label_width": None, "max_label_height": None,
                  "min_message_arrow_gap": None, "issues": 0}
        before = len(issues)
        for target in entry.get("references", []):
            if target not in known_ids:
                issue("error", "UNRESOLVED_REFERENCE", uid, f"Native ref target {target!r} is absent from the final manifest.")
        if not source.is_file():
            issue("error", "SOURCE_MISSING", uid, "Current editable source is missing.")
            result["issues"] = len(issues) - before
            views.append(result)
            continue
        try:
            xml_root = ET.fromstring(source.read_bytes())
        except ET.ParseError as exc:
            issue("error", "SOURCE_XML", uid, str(exc))
            result["issues"] = len(issues) - before
            views.append(result)
            continue
        expected_edges = {cell.get("id"): cell for cell in xml_root.findall(".//mxCell") if cell.get("edge") == "1"}
        result["expected_edges"] = len(expected_edges)
        totals["expected_edges"] += len(expected_edges)
        if not dom_path.is_file():
            issue("error", "DOM_MISSING", uid, "Render this current source with render_diagrams.cjs before auditing.")
            result["issues"] = len(issues) - before
            views.append(result)
            continue
        try:
            dom = json.loads(dom_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            issue("error", "DOM_INVALID", uid, str(exc))
            result["issues"] = len(issues) - before
            views.append(result)
            continue
        totals["dom_files_available"] += 1
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        result["source_sha256"] = digest
        result["dom_source_sha256"] = dom.get("sourceSha256")
        result["sha256_match"] = dom.get("sourceSha256") == digest
        if result["sha256_match"]:
            totals["source_sha256_matches"] += 1
        else:
            issue("error", "STALE_RENDER", uid, "The native DOM SHA256 does not match the current editable source; all geometry findings for this view are stale.")
        actual_edges = {edge.get("id"): edge for edge in dom.get("edges", [])}
        if len(actual_edges) != len(expected_edges):
            issue("error", "EDGE_COUNT", uid, f"Source has {len(expected_edges)} edges, native DOM has {len(actual_edges)}.")
        for eid in expected_edges:
            edge = actual_edges.get(eid)
            if not edge:
                issue("error", "EDGE_MISSING", uid, f"No native DOM edge for {eid}.", edge_id=eid)
            elif not edge.get("paths") or not any(isinstance(path, str) and path.strip() for path in edge["paths"]):
                issue("error", "EDGE_NOT_NATIVE", uid, f"Edge {eid} has no actual native SVG path.", edge_id=eid)
            else:
                result["native_edges_with_paths"] += 1
        totals["native_edges_with_paths"] += result["native_edges_with_paths"]
        if dom.get("nativeEdgeCount") != result["native_edges_with_paths"]:
            issue("error", "NATIVE_EDGE_COUNT", uid, "Recorded nativeEdgeCount differs from the per-edge path evidence.")
        messages = []
        for eid, source_edge in expected_edges.items():
            if not re.fullmatch(r"m\d+", str(eid)) or not clean_label(source_edge.get("value")):
                continue
            edge = actual_edges.get(eid)
            if not edge:
                continue
            if not valid_box(edge.get("labelBox")):
                issue("error", "LABEL_BOX_MISSING", uid, f"Message {eid} has no finite positive actual labelBox.", edge_id=eid)
                continue
            styles = style_dict(source_edge.get("style", ""))
            try:
                width = float(styles.get("labelWidth", "nan"))
                font = float(styles.get("fontSize", "nan"))
            except ValueError:
                width = font = float("nan")
            if not math.isfinite(width) or not 190 <= width <= 230:
                issue("error", "LABEL_WIDTH_POLICY", uid, f"Message {eid} has no explicit 190–230px native labelWidth.", edge_id=eid)
            if not math.isfinite(font) or font < 14:
                issue("error", "MESSAGE_FONT", uid, f"Message {eid} font size is below the final 14pt source target.", edge_id=eid)
            box = edge["labelBox"]
            if box["h"] > 60:
                issue("warning", "TALL_MESSAGE_LABEL", uid, f"Message {eid} label is {box['h']:.1f}px high; inspect four-or-more-line wrapping.", edge_id=eid)
            own_y = arrow_y(edge)
            if own_y is None:
                issue("error", "MESSAGE_POINTS", uid, f"Message {eid} has no finite native arrow coordinates.", edge_id=eid)
            messages.append(edge)
        result["message_labels"] = len(messages)
        totals["message_labels"] += len(messages)
        if messages:
            result["min_label_width"] = min(edge["labelBox"]["w"] for edge in messages)
            result["max_label_width"] = max(edge["labelBox"]["w"] for edge in messages)
            result["max_label_height"] = max(edge["labelBox"]["h"] for edge in messages)
        for i, left in enumerate(messages):
            for right in messages[i + 1:]:
                dx, dy = box_intersection(left["labelBox"], right["labelBox"])
                if dx > INTERSECTION_TOLERANCE and dy > INTERSECTION_TOLERANCE:
                    totals["intersecting_label_pairs"] += 1
                    issue("error", "LABEL_INTERSECTION", uid, "Two actual native message label boxes intersect.",
                          edge_ids=[left["id"], right["id"]], overlap_px={"x": round(dx, 3), "y": round(dy, 3)})
                else:
                    gap = vertical_gap(left["labelBox"], right["labelBox"])
                    if dx > INTERSECTION_TOLERANCE and 0 <= gap < NEAR_LABEL_GAP:
                        totals["near_label_pairs"] += 1
                        issue("warning", "NEAR_ADJACENT_LABELS", uid,
                              f"Horizontally overlapping label boxes have only {gap:.2f}px vertical clearance.", edge_ids=[left["id"], right["id"]])
        ordered = sorted((arrow_y(edge), edge) for edge in messages if arrow_y(edge) is not None)
        gaps = [ordered[i + 1][0] - ordered[i][0] for i in range(len(ordered) - 1)]
        if gaps:
            result["min_message_arrow_gap"] = round(min(gaps), 3)
        for i, gap in enumerate(gaps):
            if gap < MIN_ARROW_ROW_GAP:
                issue("warning", "CLOSE_MESSAGE_ROWS", uid, f"Adjacent native arrow rows are only {gap:.2f}px apart.",
                      edge_ids=[ordered[i][1]["id"], ordered[i + 1][1]["id"]])
        for label in messages:
            for other in messages:
                if other["id"] == label["id"]:
                    continue
                points = point_list(other)
                if any(segment_hits_box(start, end, label["labelBox"]) for start, end in zip(points, points[1:])):
                    totals["label_crossed_by_other_message"] += 1
                    issue("error", "UNRELATED_ARROW_THROUGH_LABEL", uid,
                          "A native message segment crosses the interior of a different message's actual label box.",
                          label_edge_id=label["id"], crossing_edge_id=other["id"])
        result["issues"] = len(issues) - before
        views.append(result)

    error_count = sum(item["severity"] == "error" for item in issues)
    warning_count = sum(item["severity"] == "warning" for item in issues)
    report = {"schema_version": "1.0", "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "manifest": str(manifest_path), "status": "FAIL" if error_count else "WARN" if warning_count else "PASS",
        "summary": {"logical_sequences": manifest.get("count"), "required_views": required_views,
                    "manifest_views": len(entries), "errors": error_count, "warnings": warning_count, **totals},
        "thresholds": {"bbox_intersection_tolerance_px": INTERSECTION_TOLERANCE,
                       "near_label_vertical_gap_px": NEAR_LABEL_GAP, "minimum_arrow_row_gap_px": MIN_ARROW_ROW_GAP,
                       "explicit_label_width_range_px": [190, 230], "minimum_message_source_font": 14},
        "limits": [
            "Checks actual native mxGraph DOM geometry and source freshness; does not inspect every raster image visually or at final A4 printed size.",
            "Uses actual edge labelBox rectangles only; intentional lifeline, activation, fragment, guard, and container overlaps are not counted as label collisions.",
            "Arrow/label collision checks use native message point segments, excluding the message's own label, frame separators, and nonmessage geometry.",
            "A source SHA256 mismatch invalidates freshness; any geometry from that stale DOM is reported as stale rather than evidence about the current source.",
            "Does not claim usability, accessibility, implementation, provider, payment, security, performance, or regulatory test results."
        ], "views": views, "issues": issues}
    output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"status": report["status"], **report["summary"], "output": str(output_path)}, indent=2))
    return 1 if error_count else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=HERE / "sequence_models.json")
    parser.add_argument("--output", type=Path, default=HERE / "Sequence_Render_Validation.json")
    parser.add_argument("--require-views", type=int, default=58)
    args = parser.parse_args()
    return audit(args.manifest.resolve(), args.output.resolve(), args.require_views)


if __name__ == "__main__":
    sys.exit(main())
