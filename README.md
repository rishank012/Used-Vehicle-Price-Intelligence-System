<div align="center">
  <h1>🚗 Used Vehicle Price Intelligence System</h1>
  <p><i>An intelligent, data-driven decision-support system designed to bring transparency to the used car market.</i></p>

  [![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io)
  [![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
</div>

---

## 📖 Overview
This project leverages Machine Learning and Data Mining techniques to estimate the fair market value of used vehicles and detect potential pricing manipulation by sellers. Whether you are a buyer looking for a fair deal or an analyst studying market trends, this system provides actionable insights backed by data.

## 🌟 Key Features
* **💰 Fair Price Estimation:** Uses **K-Nearest Neighbors (KNN)** to predict the accurate market value of a car based on its attributes (KM driven, fuel type, transmission, etc.).
* **🛡️ Manipulation Detection:** Employs a **Decision Tree Classifier** to flag listings with extreme price deviations (e.g., ±30%) as potential fraud or manipulation.
* **📊 Market Segmentation:** Utilizes **K-Means Clustering** to group cars into *Underpriced*, *Normal*, and *Overpriced* tiers.
* **🔍 Feature Insights:** Uses **Association Rule Mining (Apriori)** to discover hidden market patterns (e.g., how automatic transmissions affect resale value for first owners).
* **💻 Interactive Dashboard:** A clean, user-friendly web interface built with **Streamlit** for real-time price checking and risk assessment.

## 🛠️ Tech Stack
| Category | Technologies |
|---|---|
| **Language** | Python |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (KNN, Decision Trees, K-Means), Mlxtend (Apriori) |
| **Frontend/UI** | Streamlit |
| **Visualization** | Matplotlib, Seaborn |

## 📊 Dataset
The model is trained on the **Delhi Used Car Listings** dataset sourced from [Kaggle](https://www.kaggle.com/), containing over 1,000 unique vehicle listings with features spanning make, model, ownership history, and distance traveled.

## 🚀 How to Run the Project Locally

Follow these steps to set up and run the application on your local machine:

**1. Clone the repository:**
```bash
git clone [https://github.com/rishank012/Used-Vehicle-Price-Intelligence-System.git](https://github.com/rishank012/Used-Vehicle-Price-Intelligence-System.git)
cd Used-Vehicle-Price-Intelligence-System
```

**2. Create and activate a virtual environment (Recommended):**
```bash
# On macOS/Linux
python -m venv venv
source venv/bin/activate  

# On Windows
python -m venv venv
venv\Scripts\activate
```

**3. Install the required dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the Streamlit Dashboard:**
```bash
streamlit run main.py
```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page or submit a Pull Request.

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
