import os
import random
import time

def calculate_local_robotic_satisfaction(frame1, frame2):
    """
    Calculate Local Robotic Satisfaction for two subsequent frameglasses.
    Args:
        frame1 (str): Tags of the first frameglass.
        frame2 (str): Tags of the second frameglass.
    Returns:
        int: Local Robotic Satisfaction for the two frameglasses.
    """
    tags1 = set(frame1.split()[2:])  # Tags of Fi (skipping "L" and count)
    tags2 = set(frame2.split()[2:])  # Tags of Fi+1 (skipping "L" and count)

    common_tags = len(tags1 & tags2)  # Tags common to both frames
    tags_in_f1_not_in_f2 = len(tags1 - tags2)  # Tags in Fi but not in Fi+1
    tags_in_f2_not_in_f1 = len(tags2 - tags1)  # Tags in Fi+1 but not in Fi

    return min(common_tags, tags_in_f1_not_in_f2, tags_in_f2_not_in_f1)


def score_function(data):
    """
    Calculate the total score for a dataset based on Local Robotic Satisfaction.
    Args:
        data (list): The list of processed data lines.
    Returns:
        int: Total score for the dataset.
    """
    total_score = 0
    for i in range(len(data) - 1):  # Iterate over pairs of subsequent frames
        total_score += calculate_local_robotic_satisfaction(data[i], data[i + 1])
    return total_score


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
        scores['same_order'] = score_function(parsed_data)

        # 2. Using reverse order
        t2_start = time.time()
        reversed_data = list(reversed(parsed_data))
        with open(output_files['reverse_order'], "w") as f:
            f.write("\n".join(reversed_data))
        t2_end = time.time()
        times['reverse_order'] = t2_end - t2_start
        scores['reverse_order'] = score_function(reversed_data)

        # 3. Using random order
        t3_start = time.time()
        random_order = parsed_data[:]
        random.shuffle(random_order)
        with open(output_files['random_order'], "w") as f:
            f.write("\n".join(random_order))
        t3_end = time.time()
        times['random_order'] = t3_end - t3_start
        scores['random_order'] = score_function(random_order)

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
        scores['tag_order'] = score_function(ordered_by_tags)

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
