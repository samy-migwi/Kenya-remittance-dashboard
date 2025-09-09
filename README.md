
# Kenya Remittance Dashboard 🌍📊

![Kenya Remittance Dashboard](https://kenya-remittance-dashboard.onrender.com)
<img width="1814" height="924" alt="Screenshot From 2025-09-03 20-30-27" src="https://github.com/user-attachments/assets/88426e14-fa0b-4274-a5a0-fe454f1bcf76" />


## Overview

The **Kenya Remittance Dashboard** is an interactive web application that visualizes remittance inflows to Kenya. This project showcases my data science skills in data cleaning, analysis, and visualization.
The dashboard provides insights into remittance trends over time.

## Features

- **Data Cleaning and Analysis**: Utilizes Jupyter notebooks for data preprocessing and exploratory data analysis.
- **Interactive Visualizations**: Built with Plotly Dash to provide dynamic charts and graphs.
- **Deployment**: Hosted on Render for public access.

## Technology Stack

- **Data Analysis**: Python, Pandas, Jupyter Notebook
- **Visualization**: Plotly, Dash
- **Deployment**: Render

## Live Demo

Explore the live dashboard here: [Kenya Remittance Dashboard](https://kenya-remittance-dashboard.onrender.com)

## Installation

To run this project locally:

1. Clone this repository:
   ```bash
   git clone https://github.com/samy-migwi/Kenya-remittance-dashboard.git
   cd Kenya-remittance-dashboard
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For MacOS/Linux
   venv\Scripts\activate     # For Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
   python app.py
   ```
5. Visit the app at `http://127.0.0.1:8050/` in your browser.

## Data Source

The data used in this project is sourced from the Central Bank of Kenya's [Diaspora Remittances](https://www.centralbank.go.ke/diaspora-remittances/) reports. The dataset includes monthly remittance values from January 2004 to October 2024.

## Project Structure

```plaintext
Kenya-remittance-dashboard/
├── assets                  # Main application script
├── data                 # CSS and assets for styling
├── notebook                  # Data files
├── src/assets            # I cointain the icons 
├── src/app.py        # dashboard app engine
├── README.md        #  readme and know who we are .
├── render.yaml        # yaml file for the render server
├── requirements.txt       # Python requirements
└── sampletest.py              # The very first version of the dashbaord i keep it for later reference
```

## Key Insights

1. **Growth Over Time**: Remittance inflows have increased significantly, reaching an all-time high of USD 437 million in October 2024. 
2. **Regional Contributions**: North America remains a leading source of remittances to Kenya. 
3. **Economic Impact**: Remittances are a vital source of foreign exchange, equivalent to more than 3% of Kenya’s GDP. 

## Contributions

Contributions are welcome! If you'd like to add features or fix issues, please fork the repository and submit a pull request.

## Contact

**Author**: [Samy Migwi](https://github.com/samy-migwi)

For questions or feedback, feel free to reach out via email: [samy.migwi002@gmail.com](mailto:samy.migwi002@gmail.com).

## License

This project is licensed under the [MIT License](LICENSE).

---



