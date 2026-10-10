# Sprint Planning: 11.11 Sale Analytics

## User Stories
1. **Store Owner:** Bilang may-ari ng tindahan, gusto kong makita ang kabuuang kita (total revenue), bilang ng order, at average order value sa isang executive summary upang masuri ko ang pangkalahatang tagumpay ng 11.11 sale[cite: 5].
   - *Acceptance Criteria 1:* Lumilitaw ang total revenue at total orders sa pinakataas ng dashboard[cite: 5].
   - *Acceptance Criteria 2:* Naipakikita ang average order value nang tama batay sa mga na-deliver na order[cite: 5].

2. **Marketing Team:** Bilang miyembro ng marketing team, gusto kong masuri ang bawat kategorya ng produkto at kung saang rehiyon nagmula ang pinakamaraming bumili upang mapag-aralan namin kung aling produkto ang mabenta[cite: 3, 5].
   - *Acceptance Criteria 1:* May bar chart ng revenue bawat kategorya[cite: 5].
   - *Acceptance Criteria 2:* May rehiyonal na buod at filter na nag-u-update ng view[cite: 5].

3. **Delivery Partner:** Bilang delivery partner, gusto kong malaman ang oras ng peak ng mga order at ang dami ng kinanselang order bawat paraan ng pagbabayad upang maihanda namin ang logistics at tauhan sa susunod na sale[cite: 3, 5].
   - *Acceptance Criteria 1:* May line chart na nagpapakita ng orders per hour[cite: 5].
   - *Acceptance Criteria 2:* Naipapakita ang cancellation rate batay sa payment method (tulad ng COD)[cite: 5].

## Task Backlog
- [x] **To Do / Doing:** Gumawa at mag-generate ng 1,000,000 simulated orders sa Google Colab[cite: 4, 5].
- [x] **To Do / Doing:** Linisin ang data gamit ang PySpark (mga duplicate, maling rehiyon, at presyo)[cite: 5].
- [x] **To Do / Doing:** I-export ang mga resulta ng pagsusuri sa `results/` folder[cite: 5].
- [x] **Done:** Buuin ang Streamlit dashboard (`app.py`) na may mga chart at rehiyonal na filter[cite: 5].
- [x] **Done:** Isama ang Gemini AI briefing button at itago ang API key sa Streamlit Secrets.
- [x] **Done:** I-deploy ang app sa Streamlit Community Cloud[cite: 6].
