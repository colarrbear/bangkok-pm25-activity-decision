import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# test gitignore

# Load the CSV file into a pandas DataFrame
df = pd.read_csv("../response_clean.csv")

grouped_data = df.groupby('go_outside')['current_AQI'].mean().reset_index()

# Create subplots
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 12))

# Plot the bar chart for mean AQI based on going outside
axes[0, 0].bar(grouped_data['go_outside'], grouped_data['current_AQI'], color=['red', 'green'])
axes[0, 0].set_xlabel('Go Outside')
axes[0, 0].set_ylabel('Mean AQI')
axes[0, 0].set_title('Mean AQI Based on Going Outside')

# Plot the line plot for concern_level and change_behavior
sns.lineplot(data=df, x='concern_level', y='change_behavior', ax=axes[0, 1])
axes[0, 1].set_title('Line Plot for Concern Level and Change Behavior level')
axes[0, 1].set_xlabel('Concern Level')
axes[0, 1].set_ylabel('Change Behavior level')

# Generate word cloud for factors
factors_data = df['factors_influence'].str.lower().str.replace(',', '').str.split()
all_factors = [factor for sublist in factors_data for factor in sublist]

wordcloud_text = ' '.join(all_factors)
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(wordcloud_text)

# Plot the word cloud
axes[1, 0].imshow(wordcloud, interpolation='bilinear')
axes[1, 0].set_title('Word Cloud for Factors')
axes[1, 0].axis('off')

reconsider_percentages = {}
pm_levels = ['Below 50 (Good)', '50-100 (Moderate)', '101-150 (Unhealthy for Sensitive Groups)',
             '151-200 (Unhealthy)', 'Above 200 (Very Unhealthy)']

for pm_level in pm_levels:
    total_count = len(df[df['reconsidering_PM_level'] == pm_level])
    reconsider_count = len(df[(df['reconsidering_PM_level'] == pm_level) & (df['go_outside'] == 'No')])
    reconsider_percent = (reconsider_count / total_count) * 100 if total_count != 0 else 0
    reconsider_percentages[pm_level] = reconsider_percent

# Plot the bar chart for percentage of reconsider and PM2.5 level
reconsider_percent_df = pd.DataFrame(reconsider_percentages.items(), columns=['PM2.5 Level', 'Reconsider Percentage'])
sns.barplot(data=reconsider_percent_df, x='PM2.5 Level', y='Reconsider Percentage', ax=axes[1, 1])
axes[1, 1].set_title('Percentage of Reconsider by PM2.5 Level')
axes[1, 1].set_xlabel('PM2.5 Level')
axes[1, 1].set_ylabel('Reconsider Percentage')
axes[1, 1].set_xticklabels(axes[1, 1].get_xticklabels(), rotation=45)


plt.tight_layout()
plt.savefig('static/usingplot.png')
