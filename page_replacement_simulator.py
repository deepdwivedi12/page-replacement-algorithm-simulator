from typing import List, Dict, Any
import pandas as pd

def parse_reference_string(raw: str) -> List[int]:
    """Parse comma- or whitespace-separated non-negative integer pages."""
    parts = raw.replace(",", " ").split()
    if not parts:
        raise ValueError("Please enter at least one page number.")
    try:
        pages = [int(part) for part in parts]
    except ValueError:
        raise ValueError("Invalid reference string: use numeric page values separated by commas or spaces.")
    if any(page < 0 for page in pages):
        raise ValueError("Page numbers must be non-negative integers.")
    return pages

def validate_num_frames(raw: str) -> int:
    try:
        frames = int(raw)
    except ValueError:
        raise ValueError("Number of frames must be a whole number.")
    if frames < 1:
        raise ValueError("Number of frames must be at least 1.")
    return frames

def make_trace_row(step, page, frames, result, replaced):
    return {
        "Step": step,
        "Page": page,
        "Frames": frames.copy(),
        "Result": result,
        "Page Replaced": "-" if replaced is None else replaced
    }

def fifo(reference: List[int], num_frames: int):
    """Return (page_faults, page_hits, trace) for FIFO."""
    frames = []
    next_to_replace = 0
    faults = hits = 0
    trace = []

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

def lru(reference: List[int], num_frames: int):
    """Return (page_faults, page_hits, trace) for LRU."""
    frames = []
    last_used = {}
    faults = hits = 0
    trace = []

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
                least_recent_page = min(frames, key=lambda p: last_used[p])
                replaced = least_recent_page
                frames[frames.index(least_recent_page)] = page
        last_used[page] = step
        trace.append(make_trace_row(step, page, frames, result, replaced))

    return faults, hits, trace

def optimal(reference: List[int], num_frames: int):
    """Return (page_faults, page_hits, trace) for Optimal page replacement."""
    frames = []
    faults = hits = 0
    trace = []

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
                # If multiple pages are never used again, choose the one
                # appearing first in the current frame list (assignment rule).
                next_use = {}
                for frame_page in frames:
                    try:
                        next_use[frame_page] = future.index(frame_page)
                    except ValueError:
                        next_use[frame_page] = float("inf")
                victim = max(frames, key=lambda p: next_use[p])
                replaced = victim
                frames[frames.index(victim)] = page
        trace.append(make_trace_row(index + 1, page, frames, result, replaced))

    return faults, hits, trace

def show_trace(name: str, faults: int, hits: int, trace: List[Dict[str, Any]]):
    total = faults + hits
    display_rows = []
    for row in trace:
        display_rows.append({
            "Step": row["Step"],
            "Page Referenced": row["Page"],
            "Frame Contents": " | ".join(map(str, row["Frames"])),
            "Hit/Fault": row["Result"],
            "Page Replaced": row["Page Replaced"]
        })
    print(f"\\n{name} — Step-by-step trace")
    display(pd.DataFrame(display_rows).set_index("Step"))
    print(f"Page faults : {faults}")
    print(f"Page hits   : {hits}")
    print(f"Hit ratio   : {hits / total:.2%}")
    print(f"Fault ratio : {faults / total:.2%}")

def compare_algorithms(reference: List[int], num_frames: int):
    algorithms = {
        "FIFO": fifo,
        "LRU": lru,
        "Optimal": optimal
    }
    results = {}
    rows = []
    for name, algorithm in algorithms.items():
        faults, hits, trace = algorithm(reference, num_frames)
        results[name] = (faults, hits, trace)
        show_trace(name, faults, hits, trace)
        total = len(reference)
        rows.append({
            "Algorithm": name,
            "Frames": num_frames,
            "Page Faults": faults,
            "Page Hits": hits,
            "Hit Ratio": f"{hits / total:.2%}",
            "Fault Ratio": f"{faults / total:.2%}"
        })

    print("\\nFinal comparison")
    display(pd.DataFrame(rows).set_index("Algorithm"))
    return results

try:
    raw_reference = input("Enter page reference string (comma or space separated): ")
    raw_frames = input("Enter number of frames: ")

    reference_string = parse_reference_string(raw_reference)
    number_of_frames = validate_num_frames(raw_frames)

    print("\\nReference string:", reference_string)
    print("Number of frames:", number_of_frames)
    results = compare_algorithms(reference_string, number_of_frames)
except ValueError as error:
    print("Input error:", error)

part_b_reference = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
part_b_frames = 3
part_b_results = compare_algorithms(part_b_reference, part_b_frames)

belady_reference = [1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5]

belady_rows = []
for frame_count in (3, 4):
    for name, algorithm in (("FIFO", fifo), ("LRU", lru), ("Optimal", optimal)):
        faults, hits, _ = algorithm(belady_reference, frame_count)
        belady_rows.append({
            "Algorithm": name,
            "Frames": frame_count,
            "Page Faults": faults,
            "Page Hits": hits
        })

belady_table = pd.DataFrame(belady_rows)
display(belady_table.pivot(index="Algorithm", columns="Frames", values="Page Faults")
        .rename(columns={3: "Faults (3 frames)", 4: "Faults (4 frames)"}))

fifo_3 = belady_table.query("Algorithm == 'FIFO' and Frames == 3")["Page Faults"].iloc[0]
fifo_4 = belady_table.query("Algorithm == 'FIFO' and Frames == 4")["Page Faults"].iloc[0]
print("Belady's anomaly observed for FIFO:", fifo_4 > fifo_3)

experiment_cases = {
    "LRU better": [1, 2, 3, 1, 2, 4, 1, 2, 3, 1, 2, 4, 1, 2, 3],
    "FIFO better/equal": [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3]
}
experiment_frames = 3
experiment_rows = []

for case_name, pages in experiment_cases.items():
    fifo_faults, _, _ = fifo(pages, experiment_frames)
    lru_faults, _, _ = lru(pages, experiment_frames)
    experiment_rows.append({
        "Case": case_name,
        "Reference string": " ".join(map(str, pages)),
        "Frames": experiment_frames,
        "FIFO faults": fifo_faults,
        "LRU faults": lru_faults
    })

display(pd.DataFrame(experiment_rows))

