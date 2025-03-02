# 📊 Data Analysis Agent

![Data Analysis Agent Banner](https://raw.githubusercontent.com/username/data-analysis-agent/main/banner.png)

> An AI-powered tool that transforms your data into insights through natural language processing.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b.svg)](https://streamlit.io/)
[![Gemini API](https://img.shields.io/badge/powered%20by-Gemini-brightgreen.svg)](https://ai.google.dev/)

## ✨ Features

- **Natural Language Analysis** - Ask questions about your data in plain English
- **Smart Visualizations** - Generate beautiful charts with a simple request
- **AI Recommendations** - Get intelligent suggestions for deeper insights
- **Export & Share** - Save your findings for presentations and reports

## 🚀 Demo

![Demo GIF](https://raw.githubusercontent.com/username/data-analysis-agent/main/demo.gif)

## 🛠️ Installation

Clone this repository and install the required packages:

```bash
git clone https://github.com/username/data-analysis-agent.git
cd data-analysis-agent
pip install -r requirements.txt
```

Create a `.env` file in the project directory with your Google API key:

```
GOOGLE_API_KEY=your_gemini_api_key_here
```

## 📋 Requirements

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- Plotly
- Google Generative AI
- Pillow
- python-dotenv

## 🏃‍♂️ Usage

Run the application with:

```bash
streamlit run enhanced-data-analysis-agent_v3.py
```

Then open your browser and navigate to http://localhost:8501

### Step 1: Upload Your Data
Upload a CSV or Excel file using the sidebar, or try our sample dataset.

### Step 2: Ask Questions
Ask questions about your data in natural language like:
- "What is the average sale amount by product category?"
- "Is there a correlation between customer age and total sales?"
- "Which store location has the highest average customer rating?"

### Step 3: Generate Visualizations
Create charts by describing what you want to see:
- "Plot total sales by product category"
- "Create a scatter plot of customer age vs. total sale"
- "Show the distribution of payment methods"

### Step 4: Get AI Recommendations
Let our AI suggest interesting insights and visualizations based on your data.

## 🖼️ Screenshots

<div align="center">
  <img src="https://raw.githubusercontent.com/username/data-analysis-agent/main/screenshot1.png" width="45%" alt="Dashboard Overview"/>
  <img src="https://raw.githubusercontent.com/username/data-analysis-agent/main/screenshot2.png" width="45%" alt="Visualization Example"/>
</div>

## 🏗️ Architecture

```
                                   ┌───────────────┐
                                   │   User Input  │
                                   └───────┬───────┘
                                           │
                                           ▼
┌───────────────┐                 ┌───────────────┐                 ┌───────────────┐
│     Data      │────────────────▶│   Streamlit   │◀───────────────▶│   Gemini AI   │
│   Processing  │                 │   Interface   │                 │     Model     │
└───────────────┘                 └───────┬───────┘                 └───────────────┘
                                           │
                                           ▼
                                   ┌───────────────┐
                                   │ Visualization │
                                   │    Engine     │
                                   └───────────────┘
```

## 🔧 Customization

You can customize the application by modifying:

- The custom CSS in the `st.markdown()` section to match your brand colors
- The sample data to better fit your use case
- The model parameters in the `analyze_with_gemini()` function

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/username/data-analysis-agent/issues).

## 📝 License

This project is [MIT](https://opensource.org/licenses/MIT) licensed.

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/) for the amazing web app framework
- [Google Gemini AI](https://ai.google.dev/) for the powerful language model
- [Plotly](https://plotly.com/) and [Matplotlib](https://matplotlib.org/) for visualization libraries

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/username">Your Name</a>
</p>
