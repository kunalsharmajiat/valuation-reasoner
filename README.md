🏢 ValuCompany — Transparent Valuation Reasoning System

Project Name: Valuation Reasoner
Developed for: ValuCompany – Financial Transparency Initiative (Hiring Assessment 5)
Author: Kunal Sharma

📘 Overview

This project was developed as part of ValuCompany’s hiring assessment, where the goal was to design a transparent valuation reasoning system that not only performs accurate financial valuations but also clearly explains how each result is derived.

The system simulates a reasoning engine capable of walking through the valuation process step by step — combining quantitative finance with narrative clarity.

🧮 What It Does

The Valuation Reasoner script performs both:

Discounted Cash Flow (DCF) Valuation — Projects revenue, computes free cash flows, discounts them using WACC, and calculates terminal value via the Gordon Growth Model.

Multiples-Based Valuation — Uses an exit EV/EBITDA multiple to estimate enterprise value and provides a reconciliation between the two valuation approaches.

It also generates a sensitivity analysis grid to show how changes in discount rate and terminal growth affect valuation results.

🔍 Key Features

Transparent, step-by-step explanation for each financial calculation

Numerical and narrative outputs for every valuation method

Generates machine-readable files (.json, .csv) and human-readable reports (.txt)

Includes sensitivity grid for valuation robustness

Fully documented with modular, extendable Python code

🧠 How It Works

The script accepts financial assumptions (revenue, margins, growth, WACC, etc.) as inputs, then:

Projects revenues and cash flows over the forecast period.

Discounts those cash flows to present value using the DCF model.

Calculates terminal value using the Gordon Growth model.

Computes an alternative valuation using the EV/EBITDA multiple approach.

Produces a clear, written explanation of each computation and its rationale.

📂 Output Files

Running the script generates the following files automatically:

valuation_output_dcf.json — Detailed numeric DCF results

valuation_output_multiples.json — Numeric output for multiples-based valuation

valuation_explanation_dcf.txt — Full DCF narrative explanation

valuation_explanation_multiples.txt — Multiples method explanation

sensitivity_grid.csv — Valuation grid showing effects of discount and terminal growth

README_Valuation_Reasoner.txt — Summary documentation

🧾 Example Use Case

ValuCompany’s analysts can use this reasoning engine to:

Demonstrate valuation transparency to investors and regulators

Audit how assumptions affect enterprise value

Provide clients with both numeric and narrative valuation reports

🛠️ Technologies Used

Python 3.10+

Built-in libraries: dataclasses, json, csv, math

No external dependencies required

🚀 How to Run
python Valuation_Reasoner.py


All output files will be automatically generated in the project directory.

📄 License

This project is developed solely for ValuCompany’s internal assessment and educational use.
All rights reserved © 2025 Kunal Sharma.
