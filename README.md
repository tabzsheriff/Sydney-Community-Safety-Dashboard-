# Sydney Community Safety Dashboard

## Overview

The **Sydney Community Safety Dashboard** is an interactive, data-driven tool designed to help residents, tourists, students, and organisations make informed decisions about where to live, work, and travel within the Sydney region. Created by **Group 33** for the **QBUS5010 Intro to Dashboarding and Data Visualisation** unit at the University of Sydney, the dashboard provides detailed insights into suburb-level crime statistics and safety trends across Sydney.

## Problem Statement

Community safety is a critical consideration when choosing a place to live, visit, or invest. However, existing crime data platforms are fragmented, complex, and lack meaningful visualisation. Rising concerns—such as a 7.8% increase in non-domestic assaults from 2019 to 2024 (BOCSAR, 2024)—highlight the need for a more user-friendly and informative solution. Vulnerable groups, such as tourists and international students, particularly require accessible, comparative safety data.

---

## Objectives

- ✅ Enable data-driven decisions through suburb-level crime visualisation.
- ✅ Highlight crime patterns and safety trends over time.
- ✅ Provide intuitive tools for suburb comparison.
- ✅ Support transparency and public engagement (UN SDG 16).
- ✅ Offer a clean, user-friendly interface for all levels of users.

---

## Data Sources

### Crime-Related Data  
- Source: [NSW Bureau of Crime Statistics and Research (BOCSAR)](https://bocsar.nsw.gov.au/)  
- Crime types:  
  - Assault (Jul 2019 – Jun 2024)  
  - Theft (Jul 2019 – Jun 2024)  
  - Malicious Damage to Property (Jul 2019 – Jun 2024)  
  - Drug Offences (Jul 2019 – Jun 2024)

### Geospatial Data  
- Source: [GitHub - NSW Suburb GeoJSON](https://github.com/tonywr71/GeoJson-Data/blob/master/suburb-2-nsw.geojson)

---

## Data Cleaning and Processing

- **Crime Data:** Cleaned to remove non-analytical headers, renamed columns for usability.
- **Geo Data:** Filtered using a 100km buffer from Sydney CBD to focus on relevant suburbs and reduce dashboard load time.
- **Integration:** Data merged on suburb identifiers and processed to support spatial visualisation and modelling.

---

## Modelling

Two predictive models were implemented using **Linear Regression**:

1. **Safety Score Model:**  
   - Inputs: All crime rate variables  
   - Output: `Final_Safety_Score` (0-100, MinMax scaled)  

2. **Crime Trend Forecast Model:**  
   - Inputs: Historical crime rates (2020–2024)  
   - Output: Predicted rates for each crime type in 2025  

Model performance was assessed using MSE and R² metrics and used to generate forward-looking insights.

---

## Key Features

| Feature | Description |
|--------|-------------|
| 🧭 **Filter Panel** | Select up to 2 suburbs, crime type, and year to compare |
| 🗺️ **Crime Heatmap** | Spatial view of suburb crime distribution |
| 📊 **Visual Comparisons** | Pie charts and bar graphs for detailed suburb-to-suburb comparisons |
| ⚖️ **Safety Score Gauge** | Visual representation of calculated safety index (0–100) |
| 🌟 **Top 3 Safest Suburbs** | Automatically showcases the suburbs with the highest predicted safety score |
| 📝 **Instructions Panel** | Positioned top-left for optimal guidance and accessibility |

---

## Design vs. Implementation

| Design Intent | Final Implementation | Reason |
|---------------|-----------------------|--------|
| General search bar | Dropdown selectors | Improved input accuracy and usability |
| Hover-based help | Static top-left guide panel | Better visibility for all users |
| Heatmap with no values | Added colour legend and numeric display | Enhanced interpretability |
| Show both safest/unsafest suburbs | Only safest displayed | Reduce negativity and align with user priorities |
| Static safety score | Gauge metre | Easier interpretation and engagement |
| Combined bar graphs | Side-by-side suburb comparison | Avoids confusion, improves clarity |

---

## Critical Evaluation

The dashboard adheres to dashboard design best practices (Stojanovic, 2022; Lidwell et al., 2010):

- ✅ **Consistency:** Unified pastel colour scheme for readability and reduced cognitive load.
- ✅ **User-Centric Design:** Clear layout with intuitive flow (left-to-right, top-down).
- ✅ **Accessibility:** Instructions, dropdowns, and visual feedback support all user levels.
- ✅ **Actionable Insights:** Empowers relocation and investment decisions.
- ✅ **Performance:** Optimised for low load time via geospatial filtering.

---

## Reflection

This project deepened our understanding of the design-to-implementation pipeline in data visualisation. Key takeaways include:

- The importance of **empathising with users** to guide design choices.
- The necessity of **modular coding and data prep** to support dashboard responsiveness.
- The value of **iterative evaluation**—where feedback from peer reviews led to simplification and clarity enhancements.
- Collaborative learning through version control, team responsibilities, and tight integration of design and analytics.

---

## References

- BOCSAR. (2024). *NSW Recorded Crime Statistics*. Retrieved from https://bocsar.nsw.gov.au/
- Hodgkinson, Caputo & McIntyre. (2019). *Community Safety in NSW: Fragmentation and Integration*.
- National Terrorism Threat Level. (2024). *Australian National Security*.
- Lidwell, Holden, & Butler. (2010). *Universal Principles of Design*.
- Özaşçlar, M. (2015). *The Impact of Crime Statistics Transparency on Public Trust*.
- Thompson, S. (2009). *Geography of the Sydney Metropolitan Area*.
- United Nations. (n.d.). *Sustainable Development Goals*. https://sdgs.un.org/goals
- Jean-Christophe Le Coze & Reiman. (2023). *Visualisation in Safety Analytics*.
- Stojanovic, J. (2022). *Effective Dashboard Design in Public Sector Analytics*
