import os
import random
import time

def score_function(data, condition):
    """
    Calculate a score for the data based on the given condition.
    Args:
        data (list): The list of processed data lines.
        condition (str): The condition to evaluate ('same', 'reverse', 'random', 'tags').
    Returns:
        int: A calculated score for the condition.
    """
    if condition == 'same':
        return len(data)  # Score is the total number of lines
    elif condition == 'reverse':
        return sum(len(line.split()) for line in reversed(data))  # Total tags in reverse order
    elif condition == 'random':
        return len(set(data))  # Score is the count of unique lines (ensures randomness)
    elif condition == 'tags':
        return max(len(line.split()) for line in data)  # Max number of tags in any line
    else:
        return 0  # Default for unknown conditions


def parse_file(input_file, output_folder):
    try:
        start_time = time.time()  # Start the timer

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Read the input file and skip only the first line
        with open(input_file, "r") as file:
            lines = file.readlines()

        data_lines = lines[1:]  # Skip only the first line

        # Process lines into structured data
        parsed_data = [line.strip() for line in data_lines]

        # Output file paths
        output_files = {
            'same_order': os.path.join(output_folder, "output_same_order.txt"),
            'reverse_order': os.path.join(output_folder, "output_reverse_order.txt"),
            'random_order': os.path.join(output_folder, "output_random_order.txt"),
            'tag_order': os.path.join(output_folder, "output_tag_order.txt")
        }

        # Timed operations and scoring
        times = {}
        scores = {}

        # 1. Using the same order
        t1_start = time.time()
        with open(output_files['same_order'], "w") as f:
            f.write("\n".join(parsed_data))
        t1_end = time.time()
        times['same_order'] = t1_end - t1_start
        scores['same_order'] = score_function(parsed_data, 'same')

        # 2. Using reverse order
        t2_start = time.time()
        with open(output_files['reverse_order'], "w") as f:
            f.write("\n".join(reversed(parsed_data)))
        t2_end = time.time()
        times['reverse_order'] = t2_end - t2_start
        scores['reverse_order'] = score_function(parsed_data, 'reverse')

        # 3. Using random order
        t3_start = time.time()
        random_order = parsed_data[:]
        random.shuffle(random_order)
        with open(output_files['random_order'], "w") as f:
            f.write("\n".join(random_order))
        t3_end = time.time()
        times['random_order'] = t3_end - t3_start
        scores['random_order'] = score_function(random_order, 'random')

        # 4. Ordered according to the number of tags in the frameglasses
        t4_start = time.time()
        ordered_by_tags = sorted(
            parsed_data,
            key=lambda x: len(x.split()) - 2,  # -2 to exclude "L" and the count
            reverse=True  # Largest tag count first
        )
        with open(output_files['tag_order'], "w") as f:
            f.write("\n".join(ordered_by_tags))
        t4_end = time.time()
        times['tag_order'] = t4_end - t4_start
        scores['tag_order'] = score_function(ordered_by_tags, 'tags')

        total_time = time.time() - start_time

        # Print execution times and scores
        print(f"Output files saved in '{output_folder}' successfully!")
        print(f"Execution Times:")
        for key, value in times.items():
            print(f"  {key.replace('_', ' ').title()}: {value:.4f} seconds")
        print(f"Total Time: {total_time:.2f} seconds")

        print(f"\nScores:")
        for key, value in scores.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

    except Exception as e:
        print(f"Error: {e}")

# File paths
input_file = r"D:\KWC_2\input\0_example.txt"  # Replace with your file path
output_folder = "output"  # Specify the output folder name

# Run the parser
parse_file(input_file, output_folder)
