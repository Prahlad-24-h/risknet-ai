# 🛡️ RISKNET AI

AI-Powered Fraud Ring & Customer Risk Intelligence Platform

## Problem

Traditional fraud detection often evaluates transactions or customers independently.

Fraudsters, however, operate in coordinated networks.

RISKNET AI combines:

- Behavioral risk analysis
- Machine learning
- Graph-based detection
- Fraud ring classification
- Explainable risk scoring

to identify coordinated fraud networks.

## Fraud Patterns

RISKNET AI detects:

1. Coupon / Referral Abuse Rings
2. COD Fraud Rings
3. Chargeback Rings

## Architecture

Data
↓
Feature Engineering
↓
ML Risk Prediction
↓
Fraud Graph
↓
Graph Risk
↓
Ring Detection
↓
Final Risk Engine
↓
FastAPI
↓
Streamlit Dashboard

## ML

Machine learning predicts customer-level risk.

## Graph Intelligence

Customers are connected using shared entities such as:

- Devices
- Payment instruments
- Other behavioral relationships

Graph analysis identifies suspicious connected components.

## Risk Engine

Final risk combines:

- Rule-based behavioral risk
- ML risk
- Graph risk
- Fraud-ring intelligence

## Dashboard

The dashboard provides:

- Risk overview
- Customer investigation
- Fraud ring investigation
- Risk analysis

## API

FastAPI exposes customer and health endpoints.

## Docker

The complete system can be started using:

docker compose up --build

## Testing

pytest -v

## Project Structure

...
