UrbanSC Fix: Market Intelligence Dashboard 🚀
🔗 Project Links
[Live Interactive Dashboard](https://la-permits-analysis.streamlit.app/)

[Full Storytelling Report (PDF)](https://github.com/Zheyu-1991/LA_Permits_Analysis/blob/main/UrbanSC%20Fix.pdf)

Data Processing Notebook

📊 Business Problem
UrbanSC Fix is a startup General Contractor entering the highly competitive Los Angeles construction market. Instead of relying on intuition, this project uses public permit data to identify "Blue Ocean" market gaps ignored by established giants.



🛠️ Tech Stack

Data Warehouse: Snowflake 



Data Processing: Python (Pandas, Numpy), Snowpark 


Visualization: Streamlit, Matplotlib 


📈 Key Insights & Strategic Decisions

Hyper-Localization Strategy: Data revealed that 97% of contractors travel long distances to work. By enforcing a "Local-Only" radius, we guarantee "On-Site in 15 Minutes" efficiency.



Market Segment Targeting: Large firms (Top 10) dominate nearly 20% of high-valuation projects (skyscrapers/stadiums). UrbanSC Fix focuses on the neglected "Moderate Income" residential sector ($50k–$300k range).




Risk Mitigation as Differentiation: In the swimming pool sector, 17.7% of contractors claim "Exempt" insurance status to illegally save costs. We leverage this compliance data to win client trust by positioning ourselves as the safe, insured alternative.



🧪 Data Methodology
The project integrated over 334,000 records（to reduce the size of dataset, 30,000 records now） from LA Permit Data and Master License datasets.




Cleaning: Handled complex string formatting in valuations and standardized date fields.



Merging: Joined permit records with contractor licenses using LICENSE_NUM.


Engineering: Derived IS_LOCAL features and LICENSE_AGE to understand market maturity.
