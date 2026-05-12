so i have that project with those files already existing. and this is the readme for it 'USIU Career Fair Akinator Game
🎯 Project Overview
This project is an interactive Akinator-style guessing game designed for the USIU-Africa Career Fair booth. The game engages students and guests by guessing:

1. Level 1 – Their academic program (Degree, Masters, PhD) at USIU.
2. Level 2 – Their career path (current job or desired job).
The goal is to make career services fun, interactive, and a conversation starter.
🧩 Core Logic
The game is based on the Akinator decision-tree model:

* Knowledge Base: A structured dataset of USIU programs and careers.
* Attributes: Each program/job is tagged with binary attributes (e.g., business, science, coding, creative).
* Question Engine: Dynamically generates closed-ended questions to narrow down possibilities.
* Probability Weights: Each answer adjusts candidate weights (Yes = boost, No = reduce, Probably = moderate).
* Guess Threshold: When one candidate’s probability exceeds a threshold, the system makes a guess.
* Learning Loop: If wrong, the system logs the correct answer to improve future guesses.
📚 Knowledge Base (Current Progress)
We have curated all USIU schools and programs:
1. Chandaria School of Business

* Undergraduate: International Business Administration, Accounting, Finance, Hotel & Restaurant Management, Global Leadership & Management
* Masters: Accounting, MBA, Global Banking & Finance, Global Business Management, Health Leadership & Management, Management & Organizational Development
* PhD: Doctor of Business Administration
2. School of Humanities & Social Sciences

* Undergraduate: International Relations, Psychology, Criminal Justice Studies, Sociology
* Masters: Criminal & Transitional Justice, Clinical Psychology, Counseling Psychology, International Relations (MA), Marriage & Family Therapy
* PhD: PhD International Relations, Doctor of Psychology (Clinical)
3. School of Science & Technology

* Undergraduate: Applied Computer Technology, Information Systems & Technology, Data Science & Analytics, Artificial Intelligence & Robotics, Software Engineering
* Masters: Information Security, Information Systems & Technology
4. School of Pharmacy & Health Sciences

* Undergraduate: Bachelor of Pharmacy, Nursing, Epidemiology & Biostatistics, Analytical Chemistry, Applied Biochemistry
* Masters: Clinical Pharmacology & Therapeutics
5. School of Communication, Cinematic & Creative Arts

* Undergraduate: Journalism, Animation, Film Production & Directing
* Masters: Communication Studies
🛠️ Implementation Steps

1. Prototype in Jupyter Notebook
   * Define knowledge base as list of dictionaries with attributes.
   * Convert to Pandas DataFrame for easy filtering.
2. Attributes Added
   * `business`, `science`, `social_science`, `creative`, `coding`, `postgraduate`
3. Question Engine (Next Step)
   * Dynamically select questions based on remaining candidates.
   * Use information gain to maximize efficiency.
4. Deployment Plan
   * Move prototype to `.py` file.
   * Deploy via Streamlit for interactive booth experience.
   * Add simple UI with genie/mascot visuals later.
🚀 Next Milestones

* Implement dynamic question generator.
* Add career path knowledge base for Level 2.
* Build Streamlit UI with two levels of play.
* Test timing (~2 minutes per participant).
* Add optional leaderboard/stats for booth engagement.' so thats what im trying build but as you can see im not as accurate as i would like to be and i want to improve the accuracy of the akinator. as well as have it constantly learn from each game,and have it update its knowledge base and most importantly. So i want to know what you can do to improve what i already have
