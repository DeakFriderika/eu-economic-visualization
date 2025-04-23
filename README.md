# EU Economic Indicators Visualization

This project analyzes and visualizes key economic indicators for EU member states from 2013 to 2023.

## Data Sources
- GDP per capita
- Government debt (% of GDP)
- Budget deficit (% of GDP)

## Visualizations
1. **GDP and Budget Deficit Scatter Plot** (`gdp_deficit_simple_scatter.png`)
   - Shows relationship between GDP per capita and budget deficit for 2023
   - Includes reference lines for balanced budget and average GDP

2. **Government Debt Heatmap** (`debt_heatmap.png`)
   - Displays debt levels across all EU countries from 2013-2023
   - Color-coded with EU's 60% debt threshold as reference
   - Includes actual values in each cell

3. **Economic Radar Chart** (`economic_radar_chart.png`)
   - Compares three countries based on GDP levels:
     - Luxembourg (highest GDP)
     - Malta (average GDP)
     - Bulgaria (lowest GDP)
   - Shows normalized values for GDP, debt, and deficit

## Requirements
- Python 3.x
- pandas
- matplotlib
- seaborn
- numpy

## Setup
```bash
pip install pandas matplotlib seaborn numpy
```

## Usage
Run the analysis script:
```bash
python merge_data.py
``` 