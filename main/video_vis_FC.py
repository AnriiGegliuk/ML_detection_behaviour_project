# importing all necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os
import datetime

# Setting seaborn style
sns.set_style("white")

# Loading dataset h5 using Pandas. Please add your file to read_hdf('path',key='dataframe')
base_path = r"Z:\project_pfc_n_depression_behavior\SIT2022\1C-SIT-SDS"
df = pd.read_hdf(os.path.join(
    base_path, 'df_individual_analyzed_merged.h5'), key='dataframe')
df = df.reset_index()
print("File loaded")

# Get current date and time, so unique name for each file will be generated all the time when conde is running
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

# Create a file name with the timestamp
filename_targets_days = f"plots_by_target_and_day_{timestamp}.pdf"
filename_cond_days = f'plots_per_group_and_day{timestamp}.pdf'


################################# Generating data structure in order to plot results by each target and day #################################

# Define colors for different target types
colors = {'roi_target': '#003f5c', 'event_roi_target': '#7a5195',
          'roi_control': '#ef5675', 'event_roi_control': '#ffa600'}

# Generating PDFPages for all mice within a target
with PdfPages(os.path.join(base_path, filename_targets_days)) as pdf_pages:
    fig = None
    axs = None
    count=0
    dg = df.groupby(['mouse', 'day', 'within_factor'])
    # Loop over each unique condition and day combination
    for (mouse, day, within_factor), data in dg:
        rowindex = count % 4
        if rowindex == 0:
            # Create a figure object with 2 subplots
            fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(9, 17))
        
        # Select the data for each target type
        target_data = data.loc[data['target'].isin(['roi_target', 'roi_control'])].groupby('target').mean()
        event_data = data.loc[data['target'].isin(['event_roi_target', 'event_roi_control'])].groupby('target').sum()

        # Create bar plots for each target type in the appropriate subplot
        for i, (plot_data, target_type) in enumerate([(target_data, 'roi'), (event_data, 'event_roi')]):
            if target_type == 'roi':
                ylabel = 'Mean Value'
            else:
                ylabel = 'Sum Value'

            ax = sns.barplot(x=plot_data.index,
                            y=plot_data['val'],
                            palette=[colors[f'{target_type}_target'], colors[f'{target_type}_control']],
                            ax=axs[rowindex,i])
            
            axs[rowindex,i].set(xlabel='Target', ylabel=ylabel, title=f'{target_type.title()} Targets - {mouse} - {within_factor} - {day}')
            axs[rowindex,i].set_ylim([0, 1])

            # Adding colors for legend
            handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in [colors[f'{target_type}_target'], colors[f'{target_type}_control']]]
            
            labels = [f'{target_type}_target', f'{target_type}_control']
            axs[rowindex,i].legend(handles, labels)

            # Add value numbers to the bars
            for patch in ax.patches:
                height = patch.get_height()
                ax.text(patch.get_x()+patch.get_width()/2.,
                        height+0.02, f'{height:.2f}', ha="center")

        if rowindex == 3 or count == dg:
            # Adjust the layout and spacing of subplots
            fig.tight_layout()

            # Add the plot to the PDF object
            pdf_pages.savefig(fig)

            # Close the figure object to free memory
            plt.close(fig)

        count += 1
print(f'Files are saved for target and day in {base_path}')



################################ Generating data structure in order to plot results by each condition and Day #################################

# Get unique values in the column cond
groups = df['cond'].unique()

# Create PDF file to save plots
with PdfPages(os.path.join(base_path, filename_cond_days)) as pdf:
    # Loop through each group
    for group in groups:
        # Get unique values in the column day for the current group
        days = df.loc[df['cond'] == group, 'day'].unique()

        for i, day in enumerate(days):
            try:
                # Create two subplots for categories wICR and woICR
                fig, axes = plt.subplots(1, 2, figsize=(7, 7), sharey=True)
                # Filter data by target column, group, and day
                filtered = df[(df['target'].isin(['roi_control', 'roi_target'])) & (df['cond'] == group) & (df['day'] == day)]

                # Plot for category wICR
                sns.barplot(x='mouse', y='val', hue='target', data=filtered[filtered['within_factor'] == 'wICR'], errorbar=None, ax=axes[0])
                axes[0].set_title(f'(wICR) - {group} - {day}')
                axes[0].set_xlabel('Mouse')
                axes[0].set_ylabel('Values')
                axes[0].set_ylim([0, 1])
                axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)

                # Plot for category woICR
                sns.barplot(x='mouse', y='val', hue='target', data=filtered[filtered['within_factor'] == 'woICR'], errorbar=None, ax=axes[1])
                axes[1].set_title(f'(woICR) - {group} - {day}')
                axes[1].set_xlabel('Mouse')
                axes[1].set_ylim([0, 1])
                axes[1].set_ylabel('Values')
                axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)

                # Adjust subplot margins
                fig.subplots_adjust(hspace=0.3, right=1.8)

                # Save plot to PDF
                pdf.savefig(fig, bbox_inches='tight',
                            pad_inches=0.5, orientation='portrait')

                # Close the plot to free up memory
                plt.close(fig)

            except ValueError:
                print(f"No data available for group {group}, day {day}. Please check unique values in day column and ammend accordingly")

print(f'Files are saved for cond and day in {base_path}')
# Show plot
# plt.show()

