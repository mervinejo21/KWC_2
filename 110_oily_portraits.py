import pandas as pd
import time
from typing import List, Dict, Set, Tuple


def read_input(file_path: str) -> Tuple[int, pd.DataFrame]:
    """
    Reads and parses the input file into a pandas DataFrame.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_paintings = int(lines[0].strip())
    data = [line.strip().split(maxsplit=2) for line in lines[1:]]
    df = pd.DataFrame(data, columns=["Type", "Tag_Count", "Tags"])
    df["Tag_Count"] = df["Tag_Count"].astype(int)
    df["Tags"] = df["Tags"].apply(lambda x: set(x.split()))
    return num_paintings, df


def calculate_score(frames: List[List[int]], tags_cache: Dict[int, Set[str]]) -> int:
    """
    Calculates the global satisfaction score for a sequence of frames.
    """
    score = 0
    for i in range(len(frames) - 1):
        tags1 = set.union(*[tags_cache[idx] for idx in frames[i]])
        tags2 = set.union(*[tags_cache[idx] for idx in frames[i + 1]])
        common = len(tags1 & tags2)
        unique_tags1 = len(tags1 - tags2)
        unique_tags2 = len(tags2 - tags1)
        score += min(common, unique_tags1, unique_tags2)
    return score


def fast_pair_portraits(paintings: Dict[int, Set[str]]) -> List[List[int]]:
    """
    Quickly pairs portraits based on precomputed tag scores.
    """
    pairs = []
    used = set()
    items = list(paintings.items())
    items.sort(key=lambda x: len(x[1]), reverse=True)  # Sort by tag count descending

    while items:
        idx1, tags1 = items.pop(0)  # Take the painting with the most tags
        if idx1 in used:
            continue

        best_pair = None
        best_score = float('-inf')
        best_index = -1

        # Limit comparisons to the top remaining items
        for i, (idx2, tags2) in enumerate(items[:50]):  # Adjust candidate pool size
            if idx2 in used:
                continue

            # Calculate diversity score
            union_size = len(tags1 | tags2)
            intersection_size = len(tags1 & tags2)
            score = union_size - intersection_size

            if score > best_score:
                best_score = score
                best_pair = idx2
                best_index = i

        if best_pair is not None:
            pairs.append([idx1, best_pair])
            used.add(idx1)
            used.add(best_pair)
            items.pop(best_index)  # Remove the paired item
        else:
            pairs.append([idx1])  # Single painting

    return pairs


def greedy_arrangement(glassframes: List[List[int]], tags_cache: Dict[int, Set[str]]) -> List[List[int]]:
    """
    Greedily arranges glassframes to optimize satisfaction score.
    """
    arranged_frames = [glassframes.pop(0)]  # Start with the first frame

    while glassframes:
        current_frame = arranged_frames[-1]
        current_tags = set.union(*[tags_cache[idx] for idx in current_frame])

        best_pair = None
        best_score = float('-inf')
        best_index = -1

        # Limit comparisons to the top candidates
        for i, candidate_frame in enumerate(glassframes[:100]):  # Adjust candidate pool size
            candidate_tags = set.union(*[tags_cache[idx] for idx in candidate_frame])
            common = len(current_tags & candidate_tags)
            unique_tags1 = len(current_tags - candidate_tags)
            unique_tags2 = len(candidate_tags - current_tags)
            score = min(common, unique_tags1, unique_tags2)  # Use satisfaction metric

            if score > best_score:
                best_score = score
                best_pair = candidate_frame
                best_index = i

        # Append the best candidate to the arrangement
        if best_pair is not None:
            arranged_frames.append(best_pair)
            glassframes.pop(best_index)
        else:
            # If no suitable pair is found, append the next frame
            arranged_frames.append(glassframes.pop(0))

    return arranged_frames


def process_file_with_fast_optimization(file_path: str, output_path: str) -> None:
    """
    Processes the input file and generates an optimized sequence of frames
    using faster pairing and greedy arrangement strategies.
    """
    start_time = time.time()

    # Step 1: Read input
    num_paintings, df = read_input(file_path)

    # Step 2: Precompute tags cache
    tags_cache = {idx: row["Tags"] for idx, row in df.iterrows()}

    # Step 3: Fast pair portraits
    paired_frames = fast_pair_portraits({idx: tags_cache[idx] for idx in df.index})

    # Step 4: Greedy arrangement
    arranged_frames = greedy_arrangement(paired_frames, tags_cache)

    # Step 5: Calculate final score
    score = calculate_score(arranged_frames, tags_cache)

    # Step 6: Write output
    with open(output_path, 'w') as file:
        file.write(f"{len(arranged_frames)}\n")
        for frame in arranged_frames:
            file.write(" ".join(map(str, frame)) + "\n")

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Processed {file_path}:")
    print(f"Score = {score}")
    print(f"Execution Time = {execution_time:.2f} seconds")


# File paths
input_file = r"D:\KWC_2\input\110_oily_portraits.txt"
output_file = r"D:\KWC_2\output\optimized_oily_paintings_fast.txt"

# Process the file
process_file_with_fast_optimization(input_file, output_file)
