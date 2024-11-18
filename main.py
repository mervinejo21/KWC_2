import os
import random
import time
import pandas as pd


def calculate_local_robotic_satisfaction(frame1, frame2):
    """
    Calculate Local Robotic Satisfaction for two subsequent frameglasses.
    Args:
        frame1 (list): Tags of the first frameglass.
        frame2 (list): Tags of the second frameglass.
    Returns:
        int: Local Robotic Satisfaction for the two frameglasses.
    """
    tags1 = set(frame1)  # Tags of Fi
    tags2 = set(frame2)  # Tags of Fi+1

    common_tags = len(tags1 & tags2)  # Tags common to both frames
    tags_in_f1_not_in_f2 = len(tags1 - tags2)  # Tags in Fi but not in Fi+1
    tags_in_f2_not_in_f1 = len(tags2 - tags1)  # Tags in Fi+1 but not in Fi

    return min(common_tags, tags_in_f1_not_in_f2, tags_in_f2_not_in_f1)


def score_function(data):
    """
    Calculate the total score for a dataset based on Local Robotic Satisfaction.
    Args:
        data (pd.DataFrame): DataFrame containing the tags for each frameglass.
    Returns:
        int: Total score for the dataset.
    """
    total_score = 0
    for i in range(len(data) - 1):  # Iterate over pairs of subsequent frames
        total_score += calculate_local_robotic_satisfaction(data.iloc[i, 2:], data.iloc[i + 1, 2:])
    return total_score


def parse_file(input_file, output_folder):
    try:
        start_time = time.time()  # Start the timer

        # Ensure the output folder exists
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Read the input file and skip the first line
        with open(input_file, "r") as file:
            lines = file.readlines()
        data = pd.DataFrame([line.strip().split() for line in lines[1:]])  # Create DataFrame dynamically

        # Dynamically set column names based on actual number of columns
        num_columns = data.shape[1]
        data.columns = ["type", "count"] + [f"tag_{i}" for i in range(2, num_columns)]

        data["count"] = data["count"].astype(int)  # Convert count to integer

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
        data.to_csv(output_files['same_order'], index=False, header=False, sep=" ")
        t1_end = time.time()
        times['same_order'] = t1_end - t1_start
        scores['same_order'] = score_function(data)

        # 2. Using reverse order
        t2_start = time.time()
        reversed_data = data.iloc[::-1].reset_index(drop=True)
        reversed_data.to_csv(output_files['reverse_order'], index=False, header=False, sep=" ")
        t2_end = time.time()
        times['reverse_order'] = t2_end - t2_start
        scores['reverse_order'] = score_function(reversed_data)

        # 3. Using random order
        t3_start = time.time()
        random_data = data.sample(frac=1).reset_index(drop=True)
        random_data.to_csv(output_files['random_order'], index=False, header=False, sep=" ")
        t3_end = time.time()
        times['random_order'] = t3_end - t3_start
        scores['random_order'] = score_function(random_data)

        # 4. Ordered by the number of tags
        t4_start = time.time()
        data["tag_count"] = data.iloc[:, 2:].notnull().sum(axis=1)  # Count non-null tags
        ordered_by_tags = data.sort_values(by="tag_count", ascending=False).drop(columns=["tag_count"]).reset_index(drop=True)
        ordered_by_tags.to_csv(output_files['tag_order'], index=False, header=False, sep=" ")
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
input_file = r"D:\KWC_2\input\1_binary_landscapes.txt"  # Replace with your file path
output_folder = "output"  # Specify the output folder name

# Run the parser
parse_file(input_file, output_folder)
