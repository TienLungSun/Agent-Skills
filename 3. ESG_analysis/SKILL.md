---
name: ESG Analysis Skill
description: A specialized skill for finding, extracting, and comparing Environmental, Social, and Governance (ESG) data from public company reports.
---

# ESG Analysis Skill

## Overview
This skill helps you analyze and compare the ESG performance of listed companies. It guides you through finding the latest Sustainability/ESG reports, extracting standardized metrics, and generating a comparative analysis.

## Workflow

### 1. Locate Reports
If specific report URLs are not provided, use `search_web` to find the most recent ESG or Sustainability reports for the target companies.
- Query pattern: `[Company Name] [Year] ESG Report pdf` or `[Company Name] [Year] Sustainability Report`
- prioritization: Look for direct PDF links or dedicated sustainability pages.

### 2. Extract Data
For each company/report, identify and extract the following key metrics. Data is often found in "Performance Highlights", "ESG Data Summary", or GRI/SASB index tables usually located at the end of reports.

#### Environmental (E)
- **GHG Emissions**: Scope 1, Scope 2, and Scope 3 (tCO2e).
- **Energy**: Total energy consumption, renewable energy percentage.
- **Water**: Total water withdrawal/consumption, recycling rate.
- **Waste**: Total waste generated, diversion/recycling rate.

#### Social (S)
- **Workforce**: Total employees, gender diversity (% female), turnover rate.
- **Safety**: Lost Time Injury Frequency Rate (LTIFR) or equivalent.
- **Training**: Average training hours per employee.

#### Governance (G)
- **Board**: Independent directors %, female directors %.
- **Certifications**: ISO 14001, ISO 45001, ISO 27001, etc.

### 3. Analyze & Compare
- **Year-over-Year**: Has the company improved? (e.g., lower emissions, higher diversity).
- **Peer Comparison**: If analyzing multiple companies, create a side-by-side comparison.
- **Gaps**: Note any missing data or areas where the company is vague (e.g., "committed to reduction" without numbers).

### 4. Generate Report
Use the template in `resources/comparison_template.md` to format your output.
- Be precise with units (e.g., tons vs metric tons, MWh vs GJ).
- Cite the page number or section of the report where data was found if possible.

## Tools
- Use `search_web` to find reports.
- Use `read_url_content` to read HTML pages.
- Use `browser_subagent` if navigating a complex investor relations site or viewing a PDF in a viewer is necessary.
