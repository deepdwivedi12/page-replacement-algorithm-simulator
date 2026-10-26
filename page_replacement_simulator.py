"""
Page Replacement Algorithm Simulator
Operating Systems Lab Assignment
Algorithms: FIFO, LRU, Optimal
Run with: python3 page_replacement_simulator.py
"""
from typing import List, Dict, Any, Tuple


def parse_reference_string(raw: str) -> List[int]:
    parts = raw.replace(",", " ").split()
    if not parts:
        raise ValueError("Please enter at least one page number.")
    try:
        pages = [int(part) for part in parts]
    except ValueError as exc:
        raise ValueError("Enter numeric page values separated by commas or spaces.") from exc
    if any(page < 0 for page in pages):
        raise ValueError("Page numbers must be non-negative integers.")
    return pages


def validate_num_frames(raw: str) -> int:
    try:
        frames = int(raw)
    except ValueError as exc:
        raise ValueError("Number of frames must be a whole number.") from exc
    if frames < 1:
        raise ValueError("Number of frames must be at least 1.")
    return frames


def make_trace_row(step, page, frames, result, replaced):
    return {"Step": step, "Page": page, "Frames": frames.copy(),
            "Result": result, "Page Replaced": "-" if replaced is None else replaced}


def fifo(reference: List[int], num_frames: int) -> Tuple[int, int, list]:
    frames, next_to_replace, faults, hits, trace = [], 0, 0, 0, []
    for step, page in enumerate(reference, start=1):
        replaced = None
        if page in frames:
            hits += 1
            result = "Hit"
        else:
            faults += 1
            result = "Fault"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                replaced = frames[next_to_replace]
                frames[next_to_replace] = page
                next_to_replace = (next_to_replace + 1) % num_frames
        trace.append(make_trace_row(step, page, frames, result, replaced))
    return faults, hits, trace


def lru(reference: List[int], num_frames: int) -> Tuple[int, int, list]:
    frames, last_used, faults, hits, trace = [], {}, 0, 0, []
    for step, page in enumerate(reference, start=1):
        replaced = None
        if page in frames:
            hits += 1
            result = "Hit"
        else:
            faults += 1
            result = "Fault"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                victim = min(frames, key=lambda p: last_used[p])
                replaced = victim
                frames[frames.index(victim)] = page
        last_used[page] = step
        trace.append(make_trace_row(step, page, frames, result, replaced))
    return faults, hits, trace


def optimal(reference: List[int], num_frames: int) -> Tuple[int, int, list]:
    frames, faults, hits, trace = [], 0, 0, []
    for index, page in enumerate(reference):
        replaced = None
        if page in frames:
            hits += 1
            result = "Hit"
        else:
            faults += 1
            result = "Fault"
            if len(frames) < num_frames:
                frames.append(page)
            else:
                future = reference[index + 1:]
                next_use = {}
                for frame_page in frames:
                    try:
                        next_use[frame_page] = future.index(frame_page)
                    except ValueError:
                        next_use[frame_page] = float("inf")
                # max() keeps the first frame in a tie, as required by the assignment.
                victim = max(frames, key=lambda p: next_use[p])
                replaced = victim
                frames[frames.index(victim)] = page
        trace.append(make_trace_row(index + 1, page, frames, result, replaced))
    return faults, hits, trace


def show_trace(name: str, faults: int, hits: int, trace: list) -> None:
    print(f"\n{name} — Step-by-step trace")
    headers = ["Step", "Page Referenced", "Frame Contents", "Hit/Fault", "Page Replaced"]
    rows = [[str(row["Step"]), str(row["Page"]), " | ".join(map(str, row["Frames"])),
             row["Result"], str(row["Page Replaced"])] for row in trace]
    widths = [max(len(headers[i]), *(len(row[i]) for row in rows)) for i in range(len(headers))]
    print(" | ".join(headers[i].ljust(widths[i]) for i in range(len(headers))))
    print("-+-".join("-" * width for width in widths))
    for row in rows:
        print(" | ".join(row[i].ljust(widths[i]) for i in range(len(headers))))
    total = faults + hits
    print(f"Page faults : {faults}")
    print(f"Page hits   : {hits}")
    print(f"Hit ratio   : {hits / total:.2%}")
    print(f"Fault ratio : {faults / total:.2%}")


def compare_algorithms(reference: List[int], num_frames: int):
    algorithms = {"FIFO": fifo, "LRU": lru, "Optimal": optimal}
    results = {}
    for name, algorithm in algorithms.items():
        faults, hits, trace = algorithm(reference, num_frames)
        results[name] = (faults, hits, trace)
        show_trace(name, faults, hits, trace)
    total = len(reference)
    print("\nFinal comparison")
    print(f"{'Algorithm':<12} {'Frames':>7} {'Faults':>8} {'Hits':>7} {'Hit Ratio':>11} {'Fault Ratio':>13}")
    print("-" * 62)
    for name, (faults, hits, _) in results.items():
        print(f"{name:<12} {num_frames:>7} {faults:>8} {hits:>7} {hits / total:>10.2%} {faults / total:>12.2%}")
    return results


def main() -> None:
    print("Page Replacement Algorithm Simulator")
    print("-----------------------------------")
    try:
        reference = parse_reference_string(input("Enter page reference string (comma or space separated): "))
        num_frames = validate_num_frames(input("Enter number of frames: "))
    except ValueError as error:
        print(f"Input error: {error}")
        return
    print("\nReference string:", reference)
    print("Number of frames:", num_frames)
    compare_algorithms(reference, num_frames)


if __name__ == "__main__":
    main()
