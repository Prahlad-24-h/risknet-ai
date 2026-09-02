# 🛡️ RISKNET AI

## AI-Powered Fraud Ring & Customer Risk Intelligence Platform

RISKNET AI is an intelligent fraud detection and risk management platform designed to identify suspicious customers and detect connected fraud rings using a combination of:

- Rule-Based Risk Analysis
- Machine Learning
- Graph-Based Fraud Detection
- Fraud Ring Classification
- Network Analysis

The system combines customer behavior, transaction patterns, identity information, and graph relationships to generate an explainable final risk score.

---

# 🚀 Problem Statement

Financial platforms face complex fraud attacks where fraudulent customers are often connected through shared:

- Devices
- Payment instruments
- Identities
- Behavioral patterns
- Transaction activity

Traditional fraud detection systems often analyze customers individually.

However, modern fraud frequently occurs in coordinated fraud rings.

RISKNET AI addresses this problem by combining Machine Learning and Graph Intelligence to detect both individual customer risk and connected fraud networks.

---

# 💡 Solution

RISKNET AI analyzes customer data through multiple intelligence layers:

```text
Customer Data
      │
      ▼
Feature Engineering
      │
      ├───────────────┐
      ▼               ▼
Rule-Based Engine   Machine Learning
      │               │
      └───────┬───────┘
              ▼
       Graph Intelligence
              │
              ▼
       Fraud Ring Detection
              │
              ▼
       Final Risk Engine
              │
              ▼

      Risk Intelligence Dashboard
```text

🧠 Key Features
1. Customer Risk Scoring

Each customer receives:

Final Risk Score
Final Risk Level
ML Risk Level
Graph Risk Level
Risk Reason

Risk levels include:

🟢 LOW
🟡 MEDIUM
🔴 HIGH
2. Machine Learning Risk Detection

The Machine Learning model analyzes customer behavior and transaction patterns.

Example features include:

Credit Score
Monthly Income
Account Age
Transaction Count
Total Transaction Amount
Average Transaction Amount
Declined Transactions
Chargebacks
Promo Usage

The trained model generates customer risk predictions.

3. Graph-Based Fraud Detection

RISKNET AI creates a fraud network using relationships between customers and shared entities.

Examples:

Customer A ─── Device X
Customer B ─── Device X

Customer A ─── Payment Card Y
Customer C ─── Payment Card Y

These connections help identify coordinated fraud activity.

🔗 Fraud Ring Detection

The system detects groups of connected customers using graph analysis.

Fraud indicators include:

Shared devices
Shared payment instruments
Connected identities
Suspicious transaction behavior

Each detected network receives:

Ring ID
Ring Customer Count
Ring Node Count
Graph Risk Score
Graph Risk Level
🚨 Fraud Ring Types

RISKNET AI supports detection and classification of three major fraud ring patterns.

🎟️ Coupon / Referral Abuse Ring

Fraudsters create multiple accounts to exploit:

New user offers
Coupon codes
Referral bonuses
Promotional campaigns

Detection signals:

Shared devices
High promo usage
Multiple accounts
Connected payment instruments

💳 Card Testing Fraud Ring

Fraudsters test stolen payment cards using multiple transactions.

Detection signals:

High transaction attempts
High decline rates
Shared payment instruments
Suspicious transaction patterns

💰 Chargeback Fraud Ring

Fraudsters perform transactions and later dispute them.

Detection signals:

High chargeback count
High transaction value
Connected accounts
Shared devices or payment instruments

🏗️ Project Architecture
                    ┌─────────────────────┐
                    │   Raw Dataset       │
                    │ Excel / CSV         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Data Processing   │
                    │ Feature Engineering │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌──────────────┐  ┌──────────────┐ ┌──────────────┐
      │ Rule Engine  │  │ ML Model     │ │ Graph Engine │
      └──────┬───────┘  └──────┬───────┘ └──────┬───────┘
             │                 │                │
             └─────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │ Fraud Ring Engine   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Final Risk Engine   │
                    └──────────┬──────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
            ┌──────────────┐      ┌──────────────┐
            │ FastAPI API  │      │ Streamlit UI │
            └──────────────┘      └──────────────┘
📁 Project Structure
```text
risknet-ai/
│
├── api/
│   ├── __init__.py
│   └── main.py
│
├── dashboard/
│   ├── __init__.py
│   ├── app.py
│   └── api_client.py
│
├── data/
│   ├── raw/
│   │   └── AI_Risk_Manager_Synthetic_Dataset_v2.xlsx
│   │
│   └── processed/
│       ├── customer_risk_features.csv
│       ├── ml_predictions.csv
│       ├── graph_risk_results.csv
│       ├── network_metrics.csv
│       ├── final_risk_results.csv
│       └── fraud_ring_classification.csv
│
├── models/
│   └── risk_model.pkl
│
├── src/
│   ├── data_loader.py
│   ├── risk_engine.py
│   ├── final_risk_engine.py
│   │
│   ├── features/
│   │   ├── customer_features.py
│   │   ├── fraud_graph.py
│   │   ├── graph_risk.py
│   │   ├── ring_detector.py
│   │   ├── ring_classifier.py
│   │   ├── coupon_ring.py
│   │   ├── card_testing_ring.py
│   │   └── chargeback_ring.py
│   │
│   └── ml/
│       ├── train_model.py
│       ├── predict.py
│       └── evaluate_model.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```text
📊 Dataset Features

The processed dataset includes:

Feature	Description
customer_id	                                 Unique customer identifier
device_id	                                 Customer device identifier
primary_payment_instrument_id	                 Payment instrument
transaction_count	                         Number of transactions
total_transaction_amount	                 Total transaction value
declined_transactions	                         Failed transactions
chargeback_count	                         Number of chargebacks
promo_count	                                 Promotional usage
decline_rate	                                 Transaction decline ratio
chargeback_rate	                                 Chargeback ratio
promo_rate	                                 Promotion usage ratio
final_risk_score	                         Combined risk score
final_risk_level	                         Final risk classification
ring_id	                                         Detected fraud network
fraud_ring_type	                                 Classified fraud type

🤖 Technology Stack
Programming
Python
Data Processing
Pandas
NumPy
Machine Learning
Scikit-learn
Joblib
Graph Intelligence
NetworkX
Backend
FastAPI
Uvicorn
Dashboard
Streamlit
Deployment
Docker
Docker Compose
Version Control
Git
GitHub
⚙️ Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Move into the project:

cd risknet-ai

Create a virtual environment:

python -m venv .venv

Activate it:

Linux / WSL
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
▶️ Run the API
uvicorn api.main:app --reload

API will run on:

http://127.0.0.1:8000

Available endpoints:

/
/health
/customers
/customer/{customer_id}
📊 Run the Dashboard

Open another terminal and activate the virtual environment:

source .venv/bin/activate

Run:

streamlit run dashboard/app.py --server.port 8502

Open:

http://localhost:8502
🐳 Docker Deployment

Build the Docker image:

docker build -t risknet-ai-api .

Run the API container:

docker run --rm -p 8000:8000 risknet-ai-api

For Docker Compose:

docker compose up --build
📈 Project Outcome

RISKNET AI successfully demonstrates:

Customer-level fraud risk scoring
Machine Learning-based predictions
Graph-based relationship analysis
Fraud ring detection
Fraud ring classification
Explainable risk intelligence
REST API integration
Interactive dashboard visualization
Docker-based deployment
🔮 Future Enhancements

Future versions can include:

Real-time transaction streaming
Kafka integration
Neo4j graph database
Deep learning fraud detection
Graph Neural Networks
Real payment gateway integration
Automated fraud alerts
Cloud deployment on AWS
Kubernetes deployment
CI/CD pipeline
