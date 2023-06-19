# importing all necessary libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os
# Setting seaborn style

sns.set_style("white")

# Loading dataset h5 using Pandas. Please add your file to read_hdf('path',key='dataframe')
base_path = r"Z:\project_pfc_n_depression_behavior\SIT2022\1C-SIT"
df = pd.read_hdf(os.path.join(
    base_path, 'df_individual_analyzed_merged.h5'), key='dataframe')
print("File loaded")

# Define colors for different target types
colors = {'roi_target': '#003f5c', 'event_roi_target': '#7a5195',
          'roi_control': '#ef5675', 'event_roi_control': '#ffa600'}

# Generating PDFPages for all mice within a target
with PdfPages(os.path.join(base_path, 'plots_by_target.pdf')) as pdf_pages:
    # Loop over each unique mouse and within_factor combination
    for (mouse, within_factor), data in df.groupby(['mouse', 'within_factor']):

        # Create a figure object with 2 subplots
        fig, axs = plt.subplots(ncols=2, figsize=(7, 4))

        # Select the data for each target type
        target_data = data.loc[data.index.get_level_values('target').isin(
                                ['roi_target', 'roi_control']
                            )].groupby('target').mean()
        event_data = data.loc[data.index.get_level_values('target').isin(
                            ['event_roi_target', 'event_roi_control']
                        )].groupby('target').sum()

        # Create bar plots for each target type in the appropriate subplot
        for i, (plot_data, target_type) in enumerate([(target_data, 'roi'), (event_data, 'event_roi')]):
            if target_type == 'roi':
                ylabel = 'Mean Value'
            else:
                ylabel = 'Sum Value'
            ax = sns.barplot(x=plot_data.index,
                                y=plot_data.values.ravel(),
                                palette=[colors[f'{target_type}_target'], colors[f'{target_type}_control']],
                                ax=axs[i])
            axs[i].set(xlabel='Target', ylabel=ylabel,
                       title=f'{target_type.title()} Targets')
            axs[i].set_ylim([0, 1])
            # Adding colors for legend
            handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in [
                colors[f'{target_type}_target'], colors[f'{target_type}_control']]]
            labels = [f'{target_type}_target', f'{target_type}_control']
            axs[i].legend(handles, labels)

            # Add value numbers to the bars
            for patch in ax.patches:
                height = patch.get_height()
                ax.text(patch.get_x()+patch.get_width()/2.,
                        height+0.02, f'{height:.2f}', ha="center")

         # Set the title of the figure
        fig.suptitle(f'Mouse {mouse} - {within_factor}')

        # Adjust the layout and spacing of subplots
        fig.tight_layout()

        # Add the plot to the PDF object
        pdf_pages.savefig(fig)

        # Close the figure object to free memory
        plt.close(fig)


# Generating new data structure in order to plot results by each condition

df = df.reset_index()

# Get unique values in the column cond
groups = df['cond'].unique()

# Create figure with multiple axes
fig, axes = plt.subplots(len(groups), 2, figsize=(4, 80), sharey=True)


# Loop through each group and plot on corresponding axes
for i, group in enumerate(groups):
    # Filter data by target column and group
    filtered = df[(df['target'].isin(['roi_control', 'roi_target']))
                  & (df['cond'] == group)]

    # Plot for category wICR
    sns.barplot(x='mouse', y='val', hue='target',
                data=filtered[filtered['within_factor'] == 'wICR'], errorbar=None, ax=axes[i, 0])
    axes[i, 0].set_title(
        f'wICR - {group}', loc='left', fontdict={'fontsize': 11})
    # axes[i, 0].set_xlabel('Mouse')
    axes[i, 0].set_ylabel('Values')
    axes[i, 0].set_ylim([0, 1])
    axes[i, 0].set_xticklabels(axes[i, 0].get_xticklabels(), rotation=90)

    # Plot for category woICR
    sns.barplot(x='mouse', y='val', hue='target',
                data=filtered[filtered['within_factor'] == 'woICR'], errorbar=None, ax=axes[i, 1])
    axes[i, 1].set_title(f'woICR - {group}',
                         loc='left', fontdict={'fontsize': 11})
    # axes[i, 1].set_xlabel('Mouse')
    axes[i, 1].set_ylim([0, 1])
    axes[i, 1].set_ylabel('Values')
    axes[i, 1].set_xticklabels(axes[i, 1].get_xticklabels(), rotation=90)

    # Adjust subplot margins
fig.subplots_adjust(hspace=0.7, right=1.8)

# Save plots to PDF
with PdfPages(os.path.join(base_path, 'plots_per_group.pdf')) as pdf:
    pdf.savefig(fig, bbox_inches='tight',
                pad_inches=0.5, orientation='portrait')

# Show plot
# plt.show()