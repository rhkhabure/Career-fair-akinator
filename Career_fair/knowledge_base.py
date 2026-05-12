import pandas as pd

# ─────────────────────────────────────────────────────────────
# PROGRAMS
# ─────────────────────────────────────────────────────────────
programs = [
  # Chandaria School of Business
    {"name": "International Business Administration", "level": "Undergraduate", "school": "Chandaria School of Business",
      "attributes": ["business","maths_for_business","research","global_focus","leadership_focus","capstone","internship",
                     "international_trade_simulations","cross_border_strategy","global_supply_chain_practicum"],
      "description": "Focuses on global trade, cross-border strategy, and leadership in international markets."},

    {"name": "Accounting", "level": "Undergraduate", "school": "Chandaria School of Business",
      "attributes": ["business","maths_for_business","quantitative","professional_certification","capstone","internship",
                     "professional_certification_cpa","tax_practice","audit_methodology"],
      "description": "Covers financial reporting, auditing, taxation, and professional CPA certification preparation."},

    {"name": "Accounting", "level": "Masters", "school": "Chandaria School of Business",
     "attributes": ["business","maths_for_business","quantitative","postgraduate","thesis","professional_certification","research",
                    "professional_certification_cpa","advanced_audit_research","tax_policy_analysis"],
     "description": "Advanced accounting program with research focus, preparing for CPA and policy analysis."},

    {"name": "Finance", "level": "Undergraduate", "school": "Chandaria School of Business",
     "attributes": ["business","maths_for_business","quantitative","finance_focus","capstone","internship",
                    "financial_modeling_practice","valuation_projects","market_microstructure"],
     "description": "Emphasizes investment analysis, valuation, and financial modeling for corporate and global markets."},

    {"name": "Hotel & Restaurant Management", "level": "Undergraduate", "school": "Chandaria School of Business",
     "attributes": ["business","applied","service_industry","capstone","internship",
                    "service_industry_practice","hospitality_operations_lab","guest_experience_management"],
     "description": "Centers on hospitality operations, service management, and guest experience design."},

    {"name": "Business Administration (MBA)", "level": "Masters", "school": "Chandaria School of Business",
     "attributes": ["business","maths_for_business","postgraduate","leadership_focus","thesis","research","executive_focus",
                    "executive_capstone","case_competitions","leadership_coaching"],
    "description": "Advanced management program focusing on leadership, strategy, and executive decision-making."},

    {"name": "Global Leadership & Management", "level": "Undergraduate", "school": "Chandaria School of Business",
     "attributes": ["business","leadership_focus","global_focus","capstone","internship",
                    "cross_cultural_leadership","global_policy_simulations","organizational_psychology_intro"],
    "description": "Explores cross-cultural leadership, organizational psychology, and global policy management."},

    {"name": "Global Banking and Finance", "level": "Masters", "school": "Chandaria School of Business",
     "attributes": ["business","maths_for_business","postgraduate","quantitative","global_focus","thesis","research",
                    "international_financial_regulation","sovereign_risk_analysis","global_markets_lab"],
     "description": "Examines international financial systems, sovereign risk, and global market operations."},

    {"name": "Global Business Management", "level": "Masters", "school": "Chandaria School of Business",
     "attributes": ["business","postgraduate","global_focus","leadership_focus","thesis","research",
                    "global_strategy_capstone","cross_border_mergers","multinational_management_practicum"],
     "description": "Develops skills in multinational strategy, mergers, and global organizational management."},

    {"name": "Health Leadership and Management", "level": "Masters", "school": "Chandaria School of Business",
     "attributes": ["business","postgraduate","healthcare_focus","leadership_focus","thesis","research",
                    "healthcare_policy_simulations","hospital_administration_practicum","health_economics_modeling"],
     "description": "Integrates healthcare policy, hospital administration, and health economics leadership."},

    {"name": "Management and Organizational Development", "level": "Masters", "school": "Chandaria School of Business",
     "attributes": ["business","postgraduate","leadership_focus","organizational_psychology","thesis","research",
                    "organizational_diagnosis_projects","change_management_lab","OD_intervention_practicum"],
     "description": "Focuses on organizational psychology, change management, and OD interventions."},

    {"name": "Doctor of Business Administration", "level": "PhD", "school": "Chandaria School of Business",
     "attributes": ["business","postgraduate","dissertation","research","executive_research","quantitative",
                "executive_research_project","applied_action_research","advanced_research_methods"],
     "description": "Research-intensive doctorate emphasizing applied executive research and advanced methodologies."},

    # School of Humanities & Social Sciences
    {"name": "International Relations", "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","politics","humanities","policy_focus","capstone","field_work",
                    "policy_simulations","diplomacy_exercises","regional_studies_projects"],
     "description": "Explores diplomacy, global politics, and policy analysis with practical simulations and regional studies."},

    {"name": "Psychology", "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","humanities","qualitative","quantitative","capstone","research_methods",
                    "experimental_psych_lab","psychometrics_intro","behavioral_research_projects"],
     "description": "Introduces theories of human behavior, research methods, and experimental labs in cognitive and social psychology."},

    {"name": "Criminal Justice Studies", "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","justice_focus","field_work","applied","capstone","internship",
                    "justice_field_practice","crime_scene_observation","legal_process_simulations"],
     "description": "Focuses on law enforcement, legal systems, and applied justice practices including internships and fieldwork."},

    {"name": "Criminal and Transitional Justice", "level": "Masters", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","justice_focus","postgraduate","policy_focus","thesis","research","field_work",
                    "transitional_justice_clinics","truth_commission_simulations","restorative_practice_projects"],
     "description": "Examines justice in post-conflict societies, truth commissions, and restorative practices with policy focus."},

    {"name": "Sociology", "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","humanities","qualitative","research_methods","capstone",
                    "qualitative_methods_practice","community_ethnography","social_theory_seminar"],
     "description": "Studies social structures, community ethnography, and qualitative research methods in social theory."},

    {"name": "Clinical Psychology", "level": "Masters", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","humanities","postgraduate","clinical_practice","practicum","thesis","research",
                    "clinical_supervision","licensure_preparation","evidence_based_therapy_training"],
     "description": "Prepares students for clinical practice with supervised therapy, evidence-based interventions, and licensure preparation."},

    {"name": "Counseling Psychology", "level": "Masters", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","humanities","postgraduate","clinical_practice","practicum","thesis","research",
                    "counseling_techniques_lab","career_counseling_practicum","clinical_supervision"],
     "description": "Emphasizes counseling techniques, career guidance, and practicum-based clinical supervision."},

    {"name": "International Relations (MA)", "level": "Masters", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","politics","humanities","postgraduate","policy_focus","thesis","research","global_focus",
                    "policy_simulations_advanced","diplomatic_practicum","international_policy_research"],
     "description": "Advanced study of diplomacy, global policy, and international relations research with thesis requirement."},

    {"name": "Marriage and Family Therapy", "level": "Masters", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","humanities","postgraduate","clinical_practice","practicum","thesis","research",
                    "family_therapy_practicum","systemic_therapy","licensure_track"],
     "description": "Trains students in systemic therapy models, supervised practicum hours, and licensure track preparation."},

    {"name": "PhD International Relations", "level": "PhD", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","politics","humanities","postgraduate","dissertation","research","policy_focus","theoretical",
                    "advanced_theory_seminar","comparative_politics_research","archival_research_methods"],
     "description": "Doctoral research in comparative politics, advanced theory, and archival methods for global policy analysis."},

    {"name": "Doctor of Psychology (Clinical)", "level": "PhD", "school": "School of Humanities & Social Sciences",
     "attributes": ["social_science","humanities","postgraduate","dissertation","research","clinical_practice","licensure",
                    "advanced_clinical_research","longitudinal_clinical_trials","clinical_supervision_research"],
     "description": "Doctorate focusing on advanced clinical research, longitudinal trials, and professional licensure in psychology."},

    # School of Science & Technology
    {"name": "Applied Computer Technology", "level": "Undergraduate", "school": "School of Science & Technology",
     "attributes": ["science","coding","maths_for_programming","computational","applied","capstone","internship",
                    "embedded_systems_lab","hardware_integration_projects","applied_systems_practicum"],
     "description": "Focuses on hardware integration, embedded systems, and applied computing solutions with practical labs."},

    {"name": "Information Systems & Technology", "level": "Undergraduate", "school": "School of Science & Technology",
     "attributes": ["science","coding","maths_for_programming","computational","applied","capstone","internship",
                    "enterprise_systems_projects","business_it_alignment","systems_integration_practicum"],
     "description": "Covers enterprise systems, IT alignment with business processes, and systems integration projects."},

    {"name": "Data Science & Analytics", "level": "Undergraduate", "school": "School of Science & Technology",
     "attributes": ["science","coding","maths_for_programming","computational","quantitative","capstone","internship",
                    "big_data_platforms","model_deployment","feature_engineering"],
     "description": "Emphasizes big data platforms, statistical modeling, and feature engineering for predictive analysis."},

    {"name": "Artificial Intelligence & Robotics", "level": "Undergraduate", "school": "School of Science & Technology",
     "attributes": ["science","coding","maths_for_programming","computational","experimental","capstone","internship",
                    "robotics_lab","control_systems_projects","sensor_integration_practicum"],
     "description": "Explores robotics, control systems, and AI applications with hands-on sensor integration projects."},

    {"name": "Software Engineering", "level": "Undergraduate", "school": "School of Science & Technology",
     "attributes": ["science","coding","maths_for_programming","computational","applied","capstone","internship",
                    "software_engineering_practices","ci_cd_projects","large_scale_system_design"],
     "description": "Centers on software design, CI/CD practices, and building large-scale systems with engineering principles."},

    {"name": "Information Security", "level": "Masters", "school": "School of Science & Technology",
      "attributes": ["science","coding","maths_for_programming","postgraduate","thesis","computational","research","professional_certification",
                     "security_cert_prep","hands_on_red_team_labs","cryptography_research"],
      "description": "Advanced study of cybersecurity, cryptography, and red-team labs with professional certification preparation."},

    {"name": "Information Systems and Technology", "level": "Masters", "school": "School of Science & Technology",
      "attributes": ["science","coding","maths_for_programming","postgraduate","thesis","computational","research",
                "enterprise_architecture_research","it_governance_projects","systems_security_practicum"],
      "description": "Masters-level program focusing on enterprise architecture, IT governance, and systems security research."},

    # School of Pharmacy & Health Sciences
    {"name": "Bachelor of Pharmacy", "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
     "attributes": ["science","chemical","maths_for_chemistry","lab_work","healthcare_focus","applied","capstone","licensure","professional_certification",
                    "pharmacy_compounding","pharm_lab_safety","drug_formulation_practicum"],
     "description": "Prepares students for pharmaceutical practice with compounding, drug formulation, and licensure requirements."},

    {"name": "Nursing", "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
     "attributes": ["science","maths_for_bio","lab_work","field_work","healthcare_focus","applied","capstone","practicum","licensure",
                    "clinical_placements_long","patient_care_simulation","practicum_hours"],
     "description": "Focuses on patient care, clinical placements, and supervised practicum hours for professional licensure."},

    {"name": "Epidemiology & Biostatistics", "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
     "attributes": ["science","maths_for_bio","quantitative","research_methods","healthcare_focus","capstone","internship",
                    "epidemiology_practice","public_health_surveillance","biostatistics_projects"],
     "description": "Covers public health surveillance, statistical analysis, and applied epidemiology projects."},

    {"name": "Analytical Chemistry", "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
     "attributes": ["science","chemical","maths_for_chemistry","experimental","lab_work","research_methods","capstone",
                    "chromatography_techniques","instrument_calibration","analytical_method_validation"],
     "description": "Emphasizes laboratory techniques, chromatography, and analytical method validation in chemical sciences."},

    {"name": "Applied Biochemistry", "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
     "attributes": ["science","chemical","maths_for_bio","experimental","lab_work","research_methods","capstone",
                     "protein_assays_practicum","enzyme_kinetics_lab","molecular_biology_techniques"],
     "description": "Explores protein assays, enzyme kinetics, and molecular biology techniques in applied laboratory settings."},

    {"name": "Clinical Pharmacology and Therapeutics", "level": "Masters", "school": "School of Pharmacy & Health Sciences",
     "attributes": ["science","chemical","maths_for_chemistry","postgraduate","thesis","clinical_practice","research","licensure",
                    "clinical_trials","drug_regulatory","pharmacovigilance_projects"],
     "description": "Advanced study of drug regulation, clinical trials, and pharmacovigilance with licensure preparation."},

    # School of Communication, Cinematic & Creative Arts
    {"name": "Journalism", "level": "Undergraduate", "school": "School of Communication, Cinematic & Creative Arts",
     "attributes": ["creative","communication","linguistics","humanities","maths_for_arts","qualitative","portfolio","capstone","field_work",
                    "newsroom_internship","investigative_reporting","editorial_workflow"],
     "description": "Focuses on reporting, media writing, and newsroom practice with internships and investigative projects."},

    {"name": "Animation", "level": "Undergraduate", "school": "School of Communication, Cinematic & Creative Arts",
     "attributes": ["creative","communication","maths_for_arts","design","portfolio","studio","capstone",
                    "vfx_pipeline","animation_production_workflow","character_rigging_practicum"],
     "description": "Covers visual effects, character design, and animation production workflows with studio-based projects."},

    {"name": "Film Production & Directing", "level": "Undergraduate", "school": "School of Communication, Cinematic & Creative Arts",
     "attributes": ["creative","communication","maths_for_arts","design","studio","portfolio","capstone","internship",
                    "studio_production","cinematography_practicum","post_production_pipeline"],
     "description": "Explores cinematography, directing, and post-production pipelines with hands-on studio internships."},

    {"name": "Communication Studies", "level": "Masters", "school": "School of Communication, Cinematic & Creative Arts",
     "attributes": ["creative","communication","linguistics","humanities","maths_for_arts","postgraduate","thesis","research","portfolio",
                    "media_editing_workflow","audience_research_projects","editorial_strategy_studies"],
     "description": "Advanced program in media research, editorial strategy, and communication theory with thesis requirement."}
]


# ─────────────────────────────────────────────────────────────
# QUESTION BANK  —  Behavioural / experiential framing
#
# Design principle: ask what the student DOES, FEELS, or CARES
# about — never ask which school or department they belong to.
# The Bayesian engine infers the school from the pattern of
# answers. Each question should feel like a curious friend
# trying to figure it out, not a registration form.
# ─────────────────────────────────────────────────────────────

LIKERT = ["Definitely Yes", "Probably Yes", "Neutral", "Probably No", "Definitely No"]

questions = {

    # ── OPENING — STUDY LEVEL ────────────────────────────────
    "q_postgraduate": {
        "text": "Do you already hold an undergraduate degree and are currently studying beyond that?",
        "tags": ["postgraduate"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_phd", "q_thesis"],
            "Definitely No":  ["q_internship"],
        },
    },

    "q_phd": {
        "text": "Are you working on original research that could contribute new knowledge to your field — like a dissertation?",
        "tags": ["dissertation"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_research", "q_executive_research"],
            "Definitely No":  ["q_thesis"],
        },
    },

    "q_thesis": {
        "text": "Is there a major independent research project or thesis sitting at the end of your programme?",
        "tags": ["thesis"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_research"],
        },
    },

    # ── BROAD INTEREST SIGNALS ────────────────────────────────
    "q_business": {
        "text": "When you picture your future career, do you see yourself working inside a company — managing, strategising, or growing a business?",
        "tags": ["business"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_leadership", "q_finance", "q_global_focus"],
            "Probably Yes":   ["q_leadership", "q_finance"],
            "Definitely No":  ["q_coding", "q_lab_work", "q_people_focused"],
        },
    },

    "q_people_focused": {
        "text": "Is a big part of your studies about understanding people — their minds, behaviour, or the way societies work?",
        "tags": ["social_science"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_psychology", "q_politics", "q_justice"],
            "Probably Yes":   ["q_psychology", "q_politics"],
            "Definitely No":  ["q_lab_work", "q_coding", "q_creative"],
        },
    },

    "q_coding": {
        "text": "Do you write code or build software as a regular part of your coursework?",
        "tags": ["coding"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_data", "q_security", "q_hardware", "q_software_eng"],
            "Probably Yes":   ["q_data", "q_security"],
            "Definitely No":  ["q_lab_work", "q_business", "q_people_focused"],
        },
    },

    "q_lab_work": {
        "text": "Do you spend meaningful time in a physical laboratory — running experiments, handling equipment, or testing substances?",
        "tags": ["lab_work"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_chemical", "q_health_science"],
            "Probably Yes":   ["q_chemical"],
            "Definitely No":  ["q_coding", "q_business", "q_people_focused"],
        },
    },

    "q_health_science": {
        "text": "Is your work ultimately aimed at keeping people healthy — whether through medicine, drugs, patient care, or public health?",
        "tags": ["healthcare_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_clinical_practice", "q_chemical", "q_nursing"],
            "Probably Yes":   ["q_clinical_practice", "q_chemical"],
            "Definitely No":  ["q_creative"],
        },
    },

    "q_creative": {
        "text": "Is creating something — a film, an illustration, a written piece, an animation — actually part of how you are assessed?",
        "tags": ["creative"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_portfolio", "q_design", "q_journalism"],
            "Probably Yes":   ["q_portfolio", "q_design"],
        },
    },

    # ── CROSS-CUTTING SIGNALS ─────────────────────────────────
    "q_research": {
        "text": "Do you spend a significant amount of time reading academic papers and writing research-heavy assignments?",
        "tags": ["research"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_quantitative": {
        "text": "Are numbers, data, or statistics central to how you think through problems in your field?",
        "tags": ["quantitative"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_finance", "q_coding", "q_data"],
        },
    },

    "q_internship": {
        "text": "Does your programme send you out to work inside a real company or organisation as part of the curriculum?",
        "tags": ["internship"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_practicum": {
        "text": "Are you required to clock supervised practical hours — like sitting in on therapy sessions, hospital wards, or clinical settings?",
        "tags": ["practicum"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_clinical_practice", "q_licensure"],
        },
    },

    "q_licensure": {
        "text": "Is passing a professional board exam — like a pharmacy board, nursing council, or CPA exam — a goal built into your programme?",
        "tags": ["licensure"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_professional_certification"],
        },
    },

    "q_professional_certification": {
        "text": "Are you specifically studying toward a globally recognised professional qualification — like CPA, ACCA, or a cybersecurity certification?",
        "tags": ["professional_certification"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_field_work": {
        "text": "Does your programme regularly take you off-campus — into communities, courtrooms, newsrooms, or fieldwork sites?",
        "tags": ["field_work"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── BUSINESS SCHOOL ───────────────────────────────────────
    "q_finance": {
        "text": "Do concepts like investment returns, market valuation, or banking systems come up regularly in your studies?",
        "tags": ["finance_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus", "q_quantitative"],
            "Probably Yes":   ["q_global_focus"],
        },
    },

    "q_accounting": {
        "text": "Do you spend time learning how to track money flowing in and out of organisations — things like audits, tax, or financial statements?",
        "tags": ["professional_certification_cpa"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_postgraduate", "q_quantitative"],
        },
    },

    "q_leadership": {
        "text": "Is a big theme of your programme about how to lead people and make strategic decisions inside organisations?",
        "tags": ["leadership_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus", "q_executive_focus", "q_org_psychology"],
            "Probably Yes":   ["q_global_focus", "q_executive_focus"],
        },
    },

    "q_global_focus": {
        "text": "Do your studies frequently zoom out to an international level — comparing countries, global markets, or international policy?",
        "tags": ["global_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_executive_focus": {
        "text": "Are most of the people in your programme already working professionals rather than fresh school-leavers?",
        "tags": ["executive_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_phd", "q_research"],
        },
    },

    "q_executive_research": {
        "text": "Is your research tied to solving a real problem in an organisation you already work in — rather than purely academic inquiry?",
        "tags": ["executive_research"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_service_industry": {
        "text": "Does your programme prepare you to run or manage places where people eat, stay, or are hosted — like hotels or restaurants?",
        "tags": ["service_industry"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_org_psychology": {
        "text": "Do you study why organisations succeed or struggle from a human side — things like workplace culture, motivation, or managing change?",
        "tags": ["organizational_psychology"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_healthcare_mgmt": {
        "text": "Are you learning to run healthcare systems — hospitals, clinics, or health policy — rather than providing direct patient care?",
        "tags": ["healthcare_focus", "leadership_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── SCIENCE & TECHNOLOGY ─────────────────────────────────
    "q_data": {
        "text": "Do you build models that find patterns in data — training algorithms, making predictions, or visualising insights from large datasets?",
        "tags": ["big_data_platforms", "feature_engineering"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_quantitative"],
        },
    },

    "q_ai_robotics": {
        "text": "Do you work with physical machines, robotic systems, or AI that interacts with the real world — sensors, motors, control loops?",
        "tags": ["robotics_lab", "control_systems_projects"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_security": {
        "text": "Do you study how to break into or defend computer systems — things like penetration testing, cryptography, or network security?",
        "tags": ["security_cert_prep", "hands_on_red_team_labs"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_professional_certification", "q_postgraduate"],
        },
    },

    "q_hardware": {
        "text": "Does your work involve actual physical computing hardware — circuit boards, microcontrollers, or embedded systems?",
        "tags": ["embedded_systems_lab", "hardware_integration_projects"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_software_eng": {
        "text": "Do you think a lot about how to build software that works at scale — system architecture, testing pipelines, or engineering best practices?",
        "tags": ["software_engineering_practices", "large_scale_system_design"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_enterprise_it": {
        "text": "Do you study how technology fits inside organisations — aligning IT systems with business goals, governance, or security policy?",
        "tags": ["enterprise_systems_projects", "business_it_alignment"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── PHARMACY & HEALTH SCIENCES ────────────────────────────
    "q_chemical": {
        "text": "Do molecules, chemical reactions, or drug compounds feature heavily in your coursework?",
        "tags": ["chemical"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_pharmacy", "q_biochem"],
            "Probably Yes":   ["q_pharmacy"],
        },
    },

    "q_pharmacy": {
        "text": "Is your work specifically about how drugs are made, tested, and safely dispensed to patients?",
        "tags": ["pharmacy_compounding", "drug_formulation_practicum"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_licensure", "q_postgraduate"],
        },
    },

    "q_biochem": {
        "text": "Do you work at the molecular level of living things — things like enzyme reactions, protein structures, or DNA analysis?",
        "tags": ["protein_assays_practicum", "enzyme_kinetics_lab"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_nursing": {
        "text": "Is a core part of your training spent at a patient's bedside — learning to monitor, care for, and support people who are sick?",
        "tags": ["clinical_placements_long", "patient_care_simulation"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_licensure", "q_practicum"],
        },
    },

    "q_epidemiology": {
        "text": "Do you study disease patterns across populations — tracking outbreaks, analysing public health data, or modelling how illness spreads?",
        "tags": ["epidemiology_practice", "public_health_surveillance"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_quantitative", "q_research"],
        },
    },

    # ── HUMANITIES & SOCIAL SCIENCES ─────────────────────────
    "q_psychology": {
        "text": "Are you studying why people think, feel, and behave the way they do — and how to help when things go wrong mentally or emotionally?",
        "tags": ["social_science", "humanities"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_clinical_practice", "q_postgraduate"],
            "Probably Yes":   ["q_clinical_practice"],
            "Definitely No":  ["q_politics", "q_justice"],
        },
    },

    "q_clinical_practice": {
        "text": "Do you actually sit with real clients or patients — having sessions, making assessments, or providing some form of direct care?",
        "tags": ["clinical_practice"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_licensure", "q_practicum", "q_family_therapy"],
            "Probably Yes":   ["q_practicum"],
        },
    },

    "q_family_therapy": {
        "text": "Is your clinical work focused specifically on relationships — couples, families, or group dynamics — rather than individual therapy?",
        "tags": ["family_therapy_practicum", "systemic_therapy"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_politics": {
        "text": "Do you spend a lot of time analysing how power works — between nations, governments, or inside global institutions?",
        "tags": ["politics"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus", "q_postgraduate", "q_policy_focus"],
            "Probably Yes":   ["q_policy_focus"],
        },
    },

    "q_policy_focus": {
        "text": "Do you study how governments and organisations make big decisions — drafting policies, simulating negotiations, or critiquing governance?",
        "tags": ["policy_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_justice": {
        "text": "Is a core interest of your studies the legal system — crime, punishment, courts, or what happens when society tries to fix past wrongs?",
        "tags": ["justice_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_postgraduate", "q_field_work"],
            "Probably Yes":   ["q_field_work"],
        },
    },

    "q_qualitative": {
        "text": "Do you gather insight mostly through interviews, observation, and analysis of text or meaning — rather than surveys and statistics?",
        "tags": ["qualitative"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_people_focused"],
        },
    },

    # ── COMMUNICATION & CREATIVE ARTS ────────────────────────
    "q_portfolio": {
        "text": "Will you graduate with a portfolio, showreel, or body of creative work that you can actually show to future employers?",
        "tags": ["portfolio"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_design", "q_journalism", "q_studio"],
        },
    },

    "q_design": {
        "text": "Do you spend time designing or producing visual content — graphics, animations, motion graphics, or digital art?",
        "tags": ["design"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_studio", "q_film"],
        },
    },

    "q_journalism": {
        "text": "Are you learning to find stories, verify facts, and communicate them to a public audience — through articles, broadcasts, or investigations?",
        "tags": ["investigative_reporting", "editorial_workflow"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_studio": {
        "text": "Do you do hands-on production work in a studio environment — on a film set, in an animation lab, or in a broadcast booth?",
        "tags": ["studio"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_film"],
        },
    },

    "q_film": {
        "text": "Is directing, shooting, or editing film and video at the heart of what you study?",
        "tags": ["cinematography_practicum", "studio_production"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_communication_studies": {
        "text": "Do you study how media shapes public opinion — analysing audiences, framing, editorial strategy, or communication theory at a research level?",
        "tags": ["audience_research_projects", "editorial_strategy_studies"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_postgraduate", "q_research"],
        },
    },
}


# ─────────────────────────────────────────────────────────────
# SCHOOL QUESTION POOLS
# ─────────────────────────────────────────────────────────────
school_questions = {
    "Chandaria School of Business": [
        "q_postgraduate", "q_phd", "q_leadership", "q_finance",
        "q_accounting", "q_global_focus", "q_executive_focus",
        "q_service_industry", "q_org_psychology", "q_healthcare_mgmt",
        "q_executive_research", "q_quantitative", "q_thesis",
    ],
    "School of Humanities & Social Sciences": [
        "q_postgraduate", "q_phd", "q_psychology", "q_politics",
        "q_justice", "q_clinical_practice", "q_family_therapy",
        "q_policy_focus", "q_qualitative", "q_field_work",
        "q_thesis", "q_research",
    ],
    "School of Science & Technology": [
        "q_coding", "q_postgraduate", "q_data", "q_ai_robotics",
        "q_security", "q_hardware", "q_software_eng", "q_enterprise_it",
        "q_quantitative", "q_thesis",
    ],
    "School of Pharmacy & Health Sciences": [
        "q_lab_work", "q_chemical", "q_pharmacy", "q_nursing",
        "q_epidemiology", "q_biochem", "q_licensure", "q_practicum",
        "q_postgraduate", "q_clinical_practice",
    ],
    "School of Communication, Cinematic & Creative Arts": [
        "q_portfolio", "q_design", "q_journalism", "q_studio",
        "q_film", "q_communication_studies", "q_postgraduate",
        "q_qualitative", "q_research",
    ],
}
