import pandas as pd
import matplotlib.pyplot as plt
import argparse
from tqdm import tqdm
import matplotlib.pyplot as plt

def analyze_downtime(file_path):
    """
    Analyzes downtime data from a CSV file to calculate total count, max duration, 
    and average duration for each URL, and displays the results in a bar chart.

    Parameters:
        file_path (str): Path to the CSV file containing downtime data.
    """
    # Load the CSV data into a DataFrame
    data = pd.read_csv(file_path)
    
    # Check that required columns are present
    if not {'URL', 'Total Downtime (s)'}.issubset(data.columns):
        raise ValueError("CSV file must contain 'URL' and 'Total Downtime (s)' columns.")
    
    # Progress bar setup
    print("Processing data...")
    grouped_data = []
    for url, group in tqdm(data.groupby('URL'), desc="Calculating metrics"):
        total_count = group.shape[0]
        max_duration = group['Total Downtime (s)'].max()
        avg_duration = group['Total Downtime (s)'].mean()
        grouped_data.append([url, total_count, max_duration, avg_duration])
    
    # Convert the result to a DataFrame
    summary = pd.DataFrame(grouped_data, columns=['URL', 'Total_count', 'Max_duration', 'Average_duration'])
    
    # Display results as a chart
    plot_downtime_summary(summary)

import matplotlib.pyplot as plt

def plot_downtime_summary(summary_df, save_path="downtime_summary.png"):
    """
    Plots downtime summary metrics for each URL using a bar chart and saves the plot as a PNG file.

    Parameters:
        summary_df (DataFrame): DataFrame containing downtime metrics (URL, counts, max, avg).
        save_path (str): Path to save the plot as a PNG file.
    """
    # Set up the figure and axes
    fig, ax1 = plt.subplots(figsize=(14, 10))  

    # Create secondary y-axis
    ax2 = ax1.twinx()
    
    # Plot total count and max duration
    summary_df.plot(x='URL', y='Total_count', kind='bar', ax=ax1, width=0.4, position=1, legend=False)
    ax1.set_ylabel('Total Count (Downtimes)')
    ax1.set_xlabel('URL')
    
    summary_df.plot(x='URL', y='Max_duration', kind='line', ax=ax2, marker='o', color='orange', linewidth=2, legend=False)
    ax2.set_ylabel('Max Duration (seconds)')
    
    # Rotate x-axis labels for readability
    ax1.set_xticklabels(summary_df['URL'], rotation=45, ha="right")
    
    # Set title with adjusted padding
    fig.suptitle('Downtime Analysis: Total Count and Max Duration by URL', fontsize=16)
    
    # Adjust layout with minimal padding and reserved space for the title
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    # Save the plot as a PNG with additional padding around the figure
    plt.savefig(save_path, bbox_inches="tight", pad_inches=0.3)
    
    # Display the plot
    plt.show()

    print(f"Plot saved as '{save_path}'")


def main():
    # Set up argument parser for command-line options
    parser = argparse.ArgumentParser(description="Analyze downtime from a CSV file.")
    parser.add_argument('--csv', required=True, help="Path to the CSV file containing downtime data.")
    args = parser.parse_args()
    
    # Run the analysis with the provided CSV file path
    analyze_downtime(args.csv)

if __name__ == '__main__':
    main()
