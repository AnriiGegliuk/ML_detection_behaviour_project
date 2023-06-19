# importing all necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os
import time

# Setting seaborn style
sns.set_style("white")

# Loading dataset h5 using Pandas. Please add your file to read_hdf('path',key='dataframe')
base_path = r"Z:\project_pfc_n_depression_behavior\SIT2022\1C-SIT"
df = pd.read_hdf(os.path.join(
    base_path, 'df_individual_analyzed_merged.h5'), key='dataframe')
df = df.reset_index()
print("File loaded")

################################# Generating data structure in order to plot results by each target and day #################################

# Define colors for different target types
colors = {'roi_target': '#003f5c', 'event_roi_target': '#7a5195',
          'roi_control': '#ef5675', 'event_roi_control': '#ffa600'}

# Generating PDFPages for all mice within a target
# Generating PDFPages for all mice within a target
with PdfPages(os.path.join(base_path, 'plots_by_target_and_day_1.pdf')) as pdf_pages:
    # Loop over each unique condition and day combination
    for (mouse, day), data in df.groupby(['mouse', 'day']):
        # Create a figure object with 4 subplots
        fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(10, 8))

        # Select the data for each target type
        target_data = data.loc[data['target'].isin(['roi_target', 'roi_control'])].groupby('target').mean()
        event_data = data.loc[data['target'].isin(['event_roi_target', 'event_roi_control'])].groupby('target').sum()

        # Loop over each subplot to create the bar plots
        for i, (plot_data, target_type) in enumerate([(target_data, 'roi'), (event_data, 'event_roi')]):
            if target_type == 'roi':
                ylabel = 'Mean Value'
            else:
                ylabel = 'Sum Value'

            # Calculate the subplot index
            row = i // 2
            col = i % 2

            ax = sns.barplot(x=plot_data.index,
                            y=plot_data['val'],
                            palette=[colors[f'{target_type}_target'], colors[f'{target_type}_control']],
                            ax=axs[row][col])
            axs[row][col].set(xlabel='Target', ylabel=ylabel,
                    title=f'{target_type.title()} Targets')
            axs[row][col].set_ylim([0, 1])
            # Adding colors for legend
            handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in [
                colors[f'{target_type}_target'], colors[f'{target_type}_control']]]
            labels = [f'{target_type}_target', f'{target_type}_control']
            axs[row][col].legend(handles, labels)

            # Add value numbers to the bars
            for patch in ax.patches:
                height = patch.get_height()
                ax.text(patch.get_x()+patch.get_width()/2.,
                        height+0.02, f'{height:.2f}', ha="center")

        # Set the title of the figure
        fig.suptitle(f'{mouse} - {day}')

        # Adjust the layout and spacing of subplots
        fig.tight_layout()

        # Add the plot to the PDF object
        pdf_pages.savefig(fig)

        # Close the figure object to free memory
        plt.close(fig)

print(f'Files are saved for target and day in {base_path}')
