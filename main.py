import os
import time
from typing import List, Tuple


def read_file(file_path):
    """
    Reads and parses the input file.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract the number of paintings
    num_paintings = int(lines[0].strip())

    # Extract painting details
    paintings = [line.strip().split(maxsplit=2) for line in lines[1:]]
    for p in paintings:
        if len(p) < 3:  # Handle missing tags gracefully
            p.append("")  # Add empty tags
    return num_paintings, paintings


def calculate_tags(frameglass: List[int], paintings: List[List[str]]):
    """
    Calculates the union of tags for a given frameglass.
    """
    tags = set()
    for idx in frameglass:
        tags.update(paintings[idx - 1][2].split())  # Convert 1-based index to 0-based
    return tags


def generate_greedy_order(paintings: List[List[str]]):
    """
    Generates frameglasses using a greedy heuristic to maximize satisfaction score.
    """
    frameglasses = []

    # Split paintings into landscapes and portraits
    landscapes = [i + 1 for i, p in enumerate(paintings) if p[0] == "L"]
    portraits = [i + 1 for i, p in enumerate(paintings) if p[0] == "P"]

    # Create initial frameglasses
    all_frameglasses = [[pid] for pid in landscapes]  # Single landscapes
    all_frameglasses += [portraits[i:i+2] for i in range(0, len(portraits), 2)]  # Pairs of portraits

    if not all_frameglasses:
        return []

    # Initialize with the first frameglass
    current = all_frameglasses.pop(0)
    frameglasses.append(current)

    while all_frameglasses:
        best_score = -1
        best_frame = None

        # Find the best next frameglass
        for candidate in all_frameglasses:
            tags_current = calculate_tags(current, paintings)
            tags_candidate = calculate_tags(candidate, paintings)

            common = len(tags_current & tags_candidate)
            only_in_current = len(tags_current - tags_candidate)
            only_in_candidate = len(tags_candidate - tags_current)

            local_score = min(common, only_in_current, only_in_candidate)
            if local_score > best_score:
                best_score = local_score
                best_frame = candidate

        # Update the sequence
        current = best_frame
        frameglasses.append(current)
        all_frameglasses.remove(current)

    return frameglasses


def write_output_file(folder_path, file_name, frameglasses):
    """
    Writes the frameglasses to an output file in the specified format.
    """
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'w') as file:
        file.write(f"{len(frameglasses)}\n")  # Write number of frameglasses
        for frameglass in frameglasses:
            file.write(" ".join(map(str, frameglass)) + "\n")

    print(f"Output written to: {file_path}")


def scoring_function(frameglasses: List[List[int]], paintings: List[List[str]]):
    """
    Computes the global satisfaction score for a sequence of frameglasses.
    """
    global_score = 0

    for i in range(len(frameglasses) - 1):
        tags_fi = calculate_tags(frameglasses[i], paintings)
        tags_fi_plus_1 = calculate_tags(frameglasses[i + 1], paintings)

        common_tags = len(tags_fi & tags_fi_plus_1)
        fi_not_in_fi_plus_1 = len(tags_fi - tags_fi_plus_1)
        fi_plus_1_not_in_fi = len(tags_fi_plus_1 - tags_fi)

        local_score = min(common_tags, fi_not_in_fi_plus_1, fi_plus_1_not_in_fi)
        global_score += local_score

    return global_score


def evaluate_execution_time(paintings: List[List[str]]):
    """
    Measures execution time of the greedy heuristic.
    """
    start_time = time.time()
    generate_greedy_order(paintings)
    end_time = time.time()
    return end_time - start_time


def process_data(input_file, output_folder):
    """
    Processes the input file and generates the optimized output.
    """
    num_paintings, paintings = read_file(input_file)

    # Generate frameglasses using a greedy heuristic
    frameglasses = generate_greedy_order(paintings)

    # Write the optimized output
    write_output_file(output_folder, "optimized_output.txt", frameglasses)

    # Evaluate execution time
    execution_time = evaluate_execution_time(paintings)
    print(f"\nExecution time: {execution_time:.6f} seconds")

    # Calculate the global satisfaction score
    score = scoring_function(frameglasses, paintings)
    print(f"\nGlobal Satisfaction Score: {score}")


# Execute the script
if __name__ == "__main__":
    input_file_path = r"D:\KWC_2\input\1_binary_landscapes.txt"  # Update with the correct input file path
    output_folder = "output"  # Output folder
    process_data(input_file_path, output_folder)
