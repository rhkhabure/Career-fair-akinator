import pandas as pd

# ─────────────────────────────────────────────────────────────
# PROGRAMS
# Key design rule: every programme that is easily confused with
# another must have at least 3 EXCLUSIVE attributes the other
# does NOT share, plus shared ones that link related programmes.
# ─────────────────────────────────────────────────────────────
programs = [

  # ── Chandaria School of Business ─────────────────────────
  {"name": "International Business Administration",
   "level": "Undergraduate", "school": "Chandaria School of Business",
   "attributes": [
       "business", "global_focus", "leadership_focus", "capstone",
       "international_trade", "cross_border_strategy", "global_supply_chain",
       "trade_law_exposure", "multicultural_management",
   ],
   "description": "Global trade, cross-border strategy, supply-chain management, and leadership in international markets."},

  {"name": "Accounting",
   "level": "Undergraduate", "school": "Chandaria School of Business",
   "attributes": [
       "business", "quantitative", "capstone",
       "audit_focus", "tax_focus", "financial_reporting", "cpa_track",
       "bookkeeping_practice", "audit_methodology",
   ],
   "description": "Financial reporting, auditing, taxation, and CPA certification preparation."},

  {"name": "Accounting",
   "level": "Masters", "school": "Chandaria School of Business",
   "attributes": [
       "business", "quantitative", "postgraduate", "thesis", "research",
       "audit_focus", "tax_focus", "financial_reporting", "cpa_track",
       "advanced_audit_research", "tax_policy_analysis", "forensic_accounting",
   ],
   "description": "Advanced accounting with research focus, CPA preparation, and tax policy analysis."},

  {"name": "Finance",
   "level": "Undergraduate", "school": "Chandaria School of Business",
   "attributes": [
       "business", "quantitative", "finance_focus", "capstone",
       "investment_focus", "market_analysis", "portfolio_management",
       "valuation_practice", "financial_modeling",
   ],
   "description": "Investment analysis, valuation, financial modelling, and portfolio management."},

  {"name": "Hotel & Restaurant Management",
   "level": "Undergraduate", "school": "Chandaria School of Business",
   "attributes": [
       "business", "applied", "capstone",
       "hospitality_ops", "food_beverage_management", "guest_experience",
       "hotel_operations", "event_catering", "service_industry",
       "rooms_division_management",
   ],
   "description": "Hospitality operations, food and beverage management, and guest experience design."},

  {"name": "Business Administration (MBA)",
   "level": "Masters", "school": "Chandaria School of Business",
   "attributes": [
       "business", "postgraduate", "leadership_focus", "thesis", "research",
       "executive_focus",
       "executive_capstone", "case_competition", "leadership_coaching",
       "strategic_management", "mba_cohort",
   ],
   "description": "Executive leadership focused on strategy, management, and decision-making."},

  {"name": "Global Leadership & Management",
   "level": "Undergraduate", "school": "Chandaria School of Business",
   "attributes": [
       "business", "leadership_focus", "global_focus", "capstone",
       "cross_cultural_leadership", "organizational_behaviour",
       "global_policy_simulation", "leadership_development_track",
   ],
   "description": "Cross-cultural leadership, organisational behaviour, and global policy management."},

  {"name": "Global Banking and Finance",
   "level": "Masters", "school": "Chandaria School of Business",
   "attributes": [
       "business", "postgraduate", "quantitative", "global_focus", "thesis",
       "research", "finance_focus", "investment_focus",
       "international_financial_regulation", "sovereign_risk",
       "global_markets_lab", "forex_trading_simulation",
   ],
   "description": "International financial systems, sovereign risk, and global market operations at Masters level."},

  {"name": "Global Business Management",
   "level": "Masters", "school": "Chandaria School of Business",
   "attributes": [
       "business", "postgraduate", "global_focus", "leadership_focus",
       "thesis", "research",
       "cross_border_mergers", "multinational_strategy",
       "international_expansion_projects",
   ],
   "description": "Multinational strategy, mergers, and global organisational management at Masters level."},

  {"name": "Health Leadership and Management",
   "level": "Masters", "school": "Chandaria School of Business",
   "attributes": [
       "business", "postgraduate", "healthcare_focus", "leadership_focus",
       "thesis", "research",
       "hospital_administration", "health_economics", "healthcare_policy",
       "health_systems_management", "non_clinical_health",
   ],
   "description": "Healthcare policy, hospital administration, and health economics — no clinical practice."},

  {"name": "Management and Organizational Development",
   "level": "Masters", "school": "Chandaria School of Business",
   "attributes": [
       "business", "postgraduate", "leadership_focus", "thesis", "research",
       "org_development", "change_management", "od_intervention",
       "workplace_diagnosis", "organizational_psychology",
   ],
   "description": "Organisational psychology, change management, and OD interventions at Masters level."},

  {"name": "Doctor of Business Administration",
   "level": "PhD", "school": "Chandaria School of Business",
   "attributes": [
       "business", "postgraduate", "dissertation", "research", "quantitative",
       "executive_research", "applied_action_research",
       "practitioner_scholar", "advanced_research_methods",
   ],
   "description": "Research-intensive doctorate with applied executive research and advanced methodologies."},


  # ── School of Humanities & Social Sciences ────────────────
  {"name": "International Relations",
   "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "politics", "global_focus", "policy_focus",
       "capstone", "field_work",
       "diplomacy_focus", "geopolitics", "international_organisations",
       "treaty_analysis", "foreign_policy_study",
   ],
   "description": "Diplomacy, global politics, international organisations, and policy analysis."},

  {"name": "Psychology",
   "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "capstone", "research_methods",
       "mental_health_focus", "therapy_theory", "psychological_assessment",
       "brain_behaviour", "cognitive_science",
       "experimental_psych_lab", "psychometrics",
   ],
   "description": "Human behaviour, mental health theory, psychological assessment, and experimental research."},

  {"name": "Criminal Justice Studies",
   "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "applied", "capstone", "field_work",
       "crime_focus", "law_enforcement", "legal_system",
       "corrections_policing", "criminology",
       "crime_scene_observation", "legal_process_simulation",
   ],
   "description": "Crime, law enforcement, legal processes, and applied criminal justice practice."},

  {"name": "Sociology",
   "level": "Undergraduate", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "humanities", "qualitative", "research_methods",
       "capstone",
       "community_ethnography", "social_theory", "societal_structures",
       "group_dynamics_study", "inequality_analysis",
   ],
   "description": "Social structures, community ethnography, qualitative research, and social theory."},

  {"name": "Criminal and Transitional Justice",
   "level": "Masters", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "postgraduate", "policy_focus", "thesis",
       "research", "field_work",
       "crime_focus", "law_enforcement", "legal_system",
       "transitional_justice", "truth_commission", "post_conflict_studies",
       "restorative_justice", "international_criminal_law",
   ],
   "description": "Justice in post-conflict societies, truth commissions, and restorative practices."},

  {"name": "Clinical Psychology",
   "level": "Masters", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "postgraduate", "clinical_practice", "practicum",
       "thesis", "research",
       "mental_health_focus", "therapy_theory", "psychological_assessment",
       "clinical_supervision", "licensure_track", "evidence_based_therapy",
       "psychopathology", "diagnostic_assessment",
   ],
   "description": "Clinical practice, supervised therapy, evidence-based interventions, and licensure preparation."},

  {"name": "Counseling Psychology",
   "level": "Masters", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "postgraduate", "clinical_practice", "practicum",
       "thesis", "research",
       "mental_health_focus", "therapy_theory",
       "counseling_techniques", "career_counseling",
       "life_transitions_focus", "wellness_counseling",
       "school_counseling_option",
   ],
   "description": "Counseling techniques, career guidance, life transitions, and practicum-based supervision."},

  {"name": "International Relations (MA)",
   "level": "Masters", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "politics", "postgraduate", "policy_focus",
       "thesis", "research", "global_focus",
       "diplomacy_focus", "geopolitics", "international_organisations",
       "advanced_diplomatic_practicum", "international_policy_research",
       "security_studies",
   ],
   "description": "Advanced diplomacy, global policy research, and international security studies."},

  {"name": "Marriage and Family Therapy",
   "level": "Masters", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "postgraduate", "clinical_practice", "practicum",
       "thesis", "research",
       "mental_health_focus", "therapy_theory",
       "family_systems_therapy", "couples_therapy", "systemic_therapy",
       "relational_focus", "family_therapy_hours",
   ],
   "description": "Systemic and family therapy, couples work, and supervised clinical hours."},

  {"name": "PhD International Relations",
   "level": "PhD", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "politics", "postgraduate", "dissertation",
       "research", "policy_focus",
       "diplomacy_focus", "geopolitics",
       "advanced_ir_theory", "comparative_politics_research",
       "archival_methods", "scholarly_publication",
   ],
   "description": "Doctoral comparative politics, advanced IR theory, and archival research methods."},

  {"name": "Doctor of Psychology (Clinical)",
   "level": "PhD", "school": "School of Humanities & Social Sciences",
   "attributes": [
       "social_science", "postgraduate", "dissertation", "research",
       "clinical_practice",
       "mental_health_focus", "therapy_theory", "psychological_assessment",
       "advanced_clinical_research", "licensure_track",
       "clinical_supervision_research", "longitudinal_clinical_trials",
   ],
   "description": "Doctoral clinical practice, advanced research, and professional licensure in psychology."},


  # ── School of Science & Technology ───────────────────────
  {"name": "Applied Computer Technology",
   "level": "Undergraduate", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "computational", "applied", "capstone",
       "embedded_systems", "hardware_integration", "microcontroller_work",
       "physical_computing", "low_level_programming",
   ],
   "description": "Hardware integration, embedded systems, microcontrollers, and applied computing."},

  {"name": "Information Systems & Technology",
   "level": "Undergraduate", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "computational", "applied", "capstone",
       "enterprise_systems", "business_it_alignment", "erp_systems",
       "it_project_management", "database_administration",
       "systems_integration",
   ],
   "description": "Enterprise systems, IT-business alignment, ERP, and systems integration."},

  {"name": "Data Science & Analytics",
   "level": "Undergraduate", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "computational", "quantitative", "capstone",
       "statistical_modeling", "ml_algorithms", "data_pipeline",
       "predictive_analytics", "feature_engineering",
       "data_visualization", "big_data_platforms",
   ],
   "description": "Statistical modelling, machine learning, data pipelines, and predictive analytics."},

  {"name": "Artificial Intelligence & Robotics",
   "level": "Undergraduate", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "computational", "experimental", "capstone",
       "statistical_modeling", "ml_algorithms",
       "robotics_lab", "control_systems", "sensor_integration",
       "autonomous_systems", "physical_ai",
   ],
   "description": "Robotics, control systems, AI, and sensor integration for autonomous physical systems."},

  {"name": "Software Engineering",
   "level": "Undergraduate", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "computational", "applied", "capstone",
       "build_user_products", "software_architecture", "version_control",
       "testing_pipelines", "ci_cd", "agile_scrum",
       "large_scale_system_design",
   ],
   "description": "Software architecture, CI/CD, agile methods, and building large-scale user-facing systems."},

  {"name": "Information Security",
   "level": "Masters", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "postgraduate", "thesis", "computational",
       "research",
       "cybersecurity_focus", "penetration_testing", "cryptography",
       "network_security", "red_team_labs", "security_cert_prep",
   ],
   "description": "Cybersecurity, cryptography, red-team labs, and professional security certification."},

  {"name": "Information Systems and Technology",
   "level": "Masters", "school": "School of Science & Technology",
   "attributes": [
       "science", "coding", "postgraduate", "thesis", "computational",
       "research",
       "enterprise_systems", "business_it_alignment",
       "enterprise_architecture_research", "it_governance",
       "systems_security_practicum", "digital_transformation",
   ],
   "description": "Enterprise architecture, IT governance, digital transformation, and systems security research."},


  # ── School of Pharmacy & Health Sciences ──────────────────
  {"name": "Bachelor of Pharmacy",
   "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
   "attributes": [
       "science", "chemical", "lab_work", "healthcare_focus", "applied",
       "capstone", "licensure",
       "drug_formulation", "pharmacy_compounding", "dispensing_practice",
       "pharmacotherapy", "drug_regulatory",
   ],
   "description": "Drug formulation, compounding, dispensing, pharmacotherapy, and licensure preparation."},

  {"name": "Nursing",
   "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
   "attributes": [
       "science", "lab_work", "field_work", "healthcare_focus", "applied",
       "capstone", "practicum", "licensure", "clinical_practice",
       "patient_bedside_care", "clinical_placements", "patient_assessment",
       "vital_signs_monitoring", "ward_rotations",
   ],
   "description": "Patient bedside care, clinical placements, ward rotations, and nursing licensure."},

  {"name": "Epidemiology & Biostatistics",
   "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
   "attributes": [
       "science", "quantitative", "research_methods", "healthcare_focus",
       "capstone",
       "public_health_focus", "disease_surveillance", "population_health",
       "health_data_analysis", "epidemiology_methods",
       "biostatistics", "outbreak_investigation",
   ],
   "description": "Disease surveillance, public health data, population health, and biostatistics."},

  {"name": "Analytical Chemistry",
   "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
   "attributes": [
       "science", "chemical", "experimental", "lab_work", "research_methods",
       "capstone",
       "chromatography", "instrument_calibration", "spectroscopy",
       "analytical_method_validation", "pure_chemistry_focus",
   ],
   "description": "Laboratory techniques, chromatography, spectroscopy, and analytical method validation."},

  {"name": "Applied Biochemistry",
   "level": "Undergraduate", "school": "School of Pharmacy & Health Sciences",
   "attributes": [
       "science", "chemical", "experimental", "lab_work", "research_methods",
       "capstone",
       "protein_assays", "enzyme_kinetics", "molecular_biology",
       "cell_biology", "biochemical_pathways",
   ],
   "description": "Protein assays, enzyme kinetics, molecular biology, and cell biology laboratory work."},

  {"name": "Clinical Pharmacology and Therapeutics",
   "level": "Masters", "school": "School of Pharmacy & Health Sciences",
   "attributes": [
       "science", "chemical", "postgraduate", "thesis", "clinical_practice",
       "research", "licensure", "healthcare_focus",
       "drug_formulation", "drug_regulatory",
       "clinical_trials", "pharmacovigilance", "drug_safety_monitoring",
       "therapeutic_protocols",
   ],
   "description": "Clinical trials, drug regulation, pharmacovigilance, and therapeutic protocol research."},


  # ── School of Communication, Cinematic & Creative Arts ───
  {"name": "Journalism",
   "level": "Undergraduate",
   "school": "School of Communication, Cinematic & Creative Arts",
   "attributes": [
       "creative", "communication", "humanities", "qualitative", "portfolio",
       "capstone", "field_work",
       "news_writing", "investigative_reporting", "newsroom_practice",
       "media_ethics", "editorial_workflow", "source_verification",
   ],
   "description": "News writing, investigative reporting, newsroom practice, and media ethics."},

  {"name": "Animation",
   "level": "Undergraduate",
   "school": "School of Communication, Cinematic & Creative Arts",
   "attributes": [
       "creative", "communication", "design", "portfolio", "studio",
       "capstone",
       "character_animation", "vfx_pipeline", "3d_modelling",
       "character_rigging", "motion_graphics",
       "animation_software_tools",
   ],
   "description": "Character animation, VFX pipelines, 3D modelling, rigging, and motion graphics."},

  {"name": "Film Production & Directing",
   "level": "Undergraduate",
   "school": "School of Communication, Cinematic & Creative Arts",
   "attributes": [
       "creative", "communication", "design", "studio", "portfolio",
       "capstone",
       "cinematography", "directing", "film_set_work",
       "post_production", "screenwriting",
       "camera_operation", "film_editing",
   ],
   "description": "Cinematography, directing, screenwriting, film set work, and post-production editing."},

  {"name": "Communication Studies",
   "level": "Masters",
   "school": "School of Communication, Cinematic & Creative Arts",
   "attributes": [
       "creative", "communication", "humanities", "postgraduate", "thesis",
       "research", "portfolio",
       "audience_research", "media_theory", "editorial_strategy",
       "communication_theory", "media_effects_research",
   ],
   "description": "Media theory, audience research, editorial strategy, and communication theory research."},
]


# ─────────────────────────────────────────────────────────────
# QUESTION BANK
# Design rules:
#  1. Never name a school, department, or degree title directly
#  2. Every question targets the confused pairs specifically
#  3. q_internship REMOVED — all USIU undergrads do internships (zero signal)
#  4. Followup chains go: broad signal → fine discriminator
# ─────────────────────────────────────────────────────────────

LIKERT = ["Definitely Yes", "Probably Yes", "Neutral", "Probably No", "Definitely No"]

questions = {

    # ── STUDY LEVEL ───────────────────────────────────────────
    "q_postgraduate": {
        "text": "Is the qualification you are currently working toward your second university degree — one that builds on top of a degree you have already finished?",
        "tags": ["postgraduate"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_phd", "q_thesis"],
            "Probably Yes":   ["q_thesis"],
        },
    },

    "q_phd": {
        "text": "Are you working toward the highest academic qualification possible — one that requires you to produce original research that adds completely new knowledge to your field?",
        "tags": ["dissertation"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_research", "q_executive_research"],
            "Definitely No":  ["q_thesis"],
        },
    },

    "q_thesis": {
        "text": "Does your programme end with a substantial piece of independent research that you write and defend yourself?",
        "tags": ["thesis"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_research"],
        },
    },

    # ── BROAD FIRST-FORK SIGNALS ──────────────────────────────
    "q_business": {
        "text": "When you picture your future career, do you see yourself inside a company — managing teams, steering strategy, or driving a business forward?",
        "tags": ["business"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_numbers_or_people", "q_global_focus"],
            "Probably Yes":   ["q_numbers_or_people"],
            "Definitely No":  ["q_coding", "q_lab_work", "q_people_focused"],
        },
    },

    "q_coding": {
        "text": "Do you regularly write code — not just use software, but actually build it yourself as part of your coursework?",
        "tags": ["coding"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_build_or_analyse", "q_enterprise_it"],
            "Probably Yes":   ["q_build_or_analyse"],
            "Definitely No":  ["q_lab_work", "q_people_focused", "q_creative"],
        },
    },

    "q_lab_work": {
        "text": "Is a significant chunk of your time spent in an actual physical laboratory — handling chemicals, running experiments, or using scientific equipment?",
        "tags": ["lab_work"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_health_or_chemistry", "q_patient_focused"],
            "Probably Yes":   ["q_health_or_chemistry"],
            "Definitely No":  ["q_coding", "q_people_focused", "q_creative"],
        },
    },

    "q_people_focused": {
        "text": "Is understanding how human beings think, feel, interact, or organise themselves the main lens through which you study your field?",
        "tags": ["social_science"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_mind_or_society", "q_justice"],
            "Probably Yes":   ["q_mind_or_society"],
            "Definitely No":  ["q_lab_work", "q_coding", "q_creative"],
        },
    },

    "q_creative": {
        "text": "Is producing something creative — a film, animation, article, or visual work — literally part of how you are graded?",
        "tags": ["creative"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_portfolio", "q_screen_or_words"],
            "Probably Yes":   ["q_portfolio"],
        },
    },

    # ── BUSINESS: Finance vs Accounting ──────────────────────
    "q_numbers_or_people": {
        "text": "In your business studies, do you spend more time working with numbers and financial data than with people and leadership concepts?",
        "tags": ["quantitative"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_invest_or_audit"],
            "Probably Yes":   ["q_invest_or_audit"],
            "Probably No":    ["q_leadership", "q_org_psychology"],
            "Definitely No":  ["q_leadership", "q_org_psychology"],
        },
    },

    "q_invest_or_audit": {
        "text": "Do you spend more time studying how to GROW money — picking investments, valuing companies, and managing portfolios — than verifying that financial records are accurate?",
        "tags": ["investment_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus", "q_finance"],
            "Definitely No":  ["q_audit_focus", "q_accounting"],
        },
    },

    "q_finance": {
        "text": "Do concepts like equity markets, bond pricing, derivatives, or portfolio theory come up regularly in your coursework?",
        "tags": ["finance_focus", "market_analysis"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus"],
        },
    },

    "q_accounting": {
        "text": "Is a core part of your studies learning how to prepare, verify, and report an organisation's financial statements accurately?",
        "tags": ["audit_focus", "financial_reporting", "cpa_track"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_postgraduate"],
        },
    },

    "q_audit_focus": {
        "text": "Do you study how to audit — checking that financial records are truthful, compliant with regulations, and free from misrepresentation?",
        "tags": ["audit_focus", "tax_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_leadership": {
        "text": "Is a central theme of your programme how to lead people — motivating teams, setting strategy, or driving organisational change?",
        "tags": ["leadership_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus", "q_executive_focus", "q_org_psychology"],
            "Probably Yes":   ["q_global_focus"],
        },
    },

    "q_global_focus": {
        "text": "Do your studies regularly zoom out to an international scale — comparing countries, analysing global markets, or studying cross-border policy?",
        "tags": ["global_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_executive_focus": {
        "text": "Are most of your classmates already deep into professional careers — rather than studying straight from completing their first degree?",
        "tags": ["executive_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_executive_research": {
        "text": "Is your research anchored in a real organisation you already work in — solving an actual management problem rather than a purely theoretical one?",
        "tags": ["executive_research"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_org_psychology": {
        "text": "Do you study why organisations succeed or struggle from a human angle — workplace culture, motivation, resistance to change, or group dynamics?",
        "tags": ["org_development", "organizational_psychology"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_hospitality": {
        "text": "Does your programme specifically prepare you to run hotels, restaurants, or similar hospitality venues — managing rooms, kitchens, events, and the guest experience?",
        "tags": ["hospitality_ops", "food_beverage_management", "hotel_operations"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── TECH: SE vs DS vs IS&T vs AI vs ACT ──────────────────
    "q_build_or_analyse": {
        "text": "When you write code, is your main goal BUILDING something people actually use — an app, platform, or system — rather than analysing datasets or training prediction models?",
        "tags": ["build_user_products", "software_architecture"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_software_style", "q_enterprise_it"],
            "Probably Yes":   ["q_software_style"],
            "Definitely No":  ["q_statistics_models", "q_physical_ai"],
            "Probably No":    ["q_statistics_models"],
        },
    },

    "q_software_style": {
        "text": "Do you spend time thinking about software engineering disciplines — clean architecture, version control strategies, automated testing, or deployment pipelines?",
        "tags": ["software_architecture", "testing_pipelines", "ci_cd"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_enterprise_it"],
        },
    },

    "q_statistics_models": {
        "text": "Do you regularly fit statistical models or train machine learning algorithms — splitting data, tuning hyperparameters, and evaluating prediction performance?",
        "tags": ["statistical_modeling", "ml_algorithms"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_health_data_or_general"],
            "Probably Yes":   ["q_health_data_or_general"],
        },
    },

    "q_health_data_or_general": {
        "text": "Is your data work specifically about health outcomes — disease rates, patient data, or how public health interventions work — rather than general business or technology data?",
        "tags": ["public_health_focus", "population_health"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_epidemiology"],
            "Definitely No":  ["q_physical_ai"],
        },
    },

    "q_enterprise_it": {
        "text": "Is a core focus of your computing work aligning IT systems with business needs — ERP systems, IT governance, or enterprise architecture — rather than building consumer-facing products?",
        "tags": ["enterprise_systems", "business_it_alignment", "erp_systems"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_physical_ai": {
        "text": "Does your AI or computing work extend into the physical world — controlling robots, reading sensor data, or making machines move and respond to their environment?",
        "tags": ["robotics_lab", "control_systems", "autonomous_systems"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_hardware": {
        "text": "Do you work with actual physical computing components — circuit boards, microcontrollers, or embedded systems that interface with hardware directly?",
        "tags": ["embedded_systems", "hardware_integration", "microcontroller_work"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_security": {
        "text": "Do you study how to attack or defend computer systems — penetration testing, cryptography, or protecting networks from intrusion?",
        "tags": ["cybersecurity_focus", "penetration_testing", "cryptography"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_professional_certification", "q_postgraduate"],
        },
    },

    # ── SOCIAL SCIENCE: Psychology vs CJS vs IR vs Sociology ─
    "q_mind_or_society": {
        "text": "Is your main focus the individual mind — understanding a person's thoughts, emotions, and mental health — rather than how groups, institutions, or societies function?",
        "tags": ["mental_health_focus", "brain_behaviour"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_clinical_practice", "q_therapy_type"],
            "Probably Yes":   ["q_clinical_practice"],
            "Definitely No":  ["q_society_angle"],
            "Probably No":    ["q_society_angle"],
        },
    },

    "q_therapy_type": {
        "text": "In your clinical or therapeutic work, is your focus on RELATIONSHIPS — working with couples or families as a system — rather than treating individuals in isolation?",
        "tags": ["family_systems_therapy", "couples_therapy", "relational_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_society_angle": {
        "text": "Is your social science work more about how power, laws, and institutions shape society — like politics, justice, or diplomacy — than about the inner workings of individual minds?",
        "tags": ["politics", "crime_focus", "policy_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_justice", "q_politics"],
            "Probably Yes":   ["q_politics"],
        },
    },

    "q_justice": {
        "text": "Is the legal system, crime, punishment, or what happens when society tries to correct past wrongs a central theme of your studies?",
        "tags": ["crime_focus", "law_enforcement", "legal_system"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_postgraduate", "q_field_work"],
            "Probably Yes":   ["q_field_work"],
        },
    },

    "q_politics": {
        "text": "Do you spend a lot of your study time analysing how power operates — between governments, states, or international institutions?",
        "tags": ["politics", "diplomacy_focus", "geopolitics"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_global_focus", "q_policy_focus"],
        },
    },

    "q_policy_focus": {
        "text": "Do you study how governments design and implement policy — sitting in simulated negotiations, drafting policy briefs, or critiquing governance decisions?",
        "tags": ["policy_focus"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_qualitative": {
        "text": "Is most of your research done through interviews, observation, or interpreting texts and meaning — rather than running statistical tests on numerical data?",
        "tags": ["qualitative"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_field_work": {
        "text": "Does your programme regularly take you off-campus — into communities, courts, hospitals, newsrooms, or fieldwork sites as part of your formal learning?",
        "tags": ["field_work"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── HEALTH SCIENCES: Nursing vs Pharmacy vs Biochem vs Epi
    "q_health_or_chemistry": {
        "text": "Is the chemistry you study primarily about biological systems and living things — like drugs, cells, and enzymes — rather than industrial or purely analytical chemistry?",
        "tags": ["chemical", "healthcare_focus"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_patient_focused", "q_drug_or_cell"],
            "Probably Yes":   ["q_drug_or_cell"],
            "Definitely No":  ["q_pure_chemistry"],
        },
    },

    "q_patient_focused": {
        "text": "Is your work ultimately aimed at directly helping sick or vulnerable people — giving them medicine, care, or treatment in a clinical setting?",
        "tags": ["healthcare_focus", "clinical_practice"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_bedside_or_dispensing"],
            "Probably Yes":   ["q_bedside_or_dispensing"],
            "Definitely No":  ["q_population_health_focus"],
        },
    },

    "q_bedside_or_dispensing": {
        "text": "Is your patient contact primarily at the bedside — monitoring vital signs, providing physical care, and supporting recovery — rather than preparing and dispensing medicines?",
        "tags": ["patient_bedside_care", "clinical_placements"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_practicum", "q_licensure"],
            "Definitely No":  ["q_pharmacy_specific"],
        },
    },

    "q_pharmacy_specific": {
        "text": "Is your work specifically about the science of medicines — how drugs are formulated, compounded, tested, and safely dispensed to patients?",
        "tags": ["drug_formulation", "pharmacy_compounding", "dispensing_practice"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_licensure"],
        },
    },

    "q_drug_or_cell": {
        "text": "In your lab work, is your primary focus on drug molecules and their effects on the body — rather than on cells, proteins, and fundamental biochemical processes?",
        "tags": ["drug_formulation", "pharmacotherapy"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_pharmacy_specific"],
            "Definitely No":  ["q_biochem_focus"],
        },
    },

    "q_biochem_focus": {
        "text": "Do you work at the molecular level of living systems — studying enzyme reactions, protein structures, or how cells carry out basic biological processes?",
        "tags": ["protein_assays", "enzyme_kinetics", "molecular_biology"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_pure_chemistry": {
        "text": "Is your lab work focused on precise chemical measurement and analysis — techniques like chromatography, spectroscopy, or calibrating analytical instruments?",
        "tags": ["chromatography", "spectroscopy", "analytical_method_validation"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_population_health_focus": {
        "text": "Do you study health at a population level — tracking how diseases spread, measuring health outcomes across communities, or evaluating public health programmes?",
        "tags": ["public_health_focus", "disease_surveillance", "population_health"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_epidemiology"],
        },
    },

    "q_epidemiology": {
        "text": "Do you use statistical tools specifically to understand how diseases spread across populations, who is most at risk, and how interventions slow them down?",
        "tags": ["epidemiology_methods", "biostatistics", "outbreak_investigation"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_healthcare_mgmt": {
        "text": "Are you learning to run healthcare organisations — managing hospitals, designing health policy, or improving health systems — without providing direct patient care yourself?",
        "tags": ["hospital_administration", "health_systems_management", "non_clinical_health"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── CLINICAL PRACTICE ─────────────────────────────────────
    "q_clinical_practice": {
        "text": "Do you actually sit with real clients or patients — conducting sessions, running assessments, or providing direct therapeutic care as part of your training?",
        "tags": ["clinical_practice"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_licensure", "q_practicum", "q_therapy_type"],
            "Probably Yes":   ["q_practicum"],
        },
    },

    "q_practicum": {
        "text": "Are you required to log a minimum number of supervised clinical or practical hours — sitting in on or conducting real sessions with clients or patients?",
        "tags": ["practicum"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_licensure": {
        "text": "Is passing a professional board exam — pharmacy board, nursing council, or psychology licensing test — a formal goal built into your programme?",
        "tags": ["licensure"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_professional_certification"],
        },
    },

    "q_professional_certification": {
        "text": "Are you specifically working toward a globally recognised professional qualification — like CPA, ACCA, CISSP, or a pharmacy or nursing board certification?",
        "tags": ["cpa_track", "security_cert_prep"],
        "responses": LIKERT,
        "followups": {},
    },

    # ── RESEARCH ─────────────────────────────────────────────
    "q_research": {
        "text": "Does your programme expect you to engage deeply with academic literature — reading journal papers, critiquing studies, and writing research-heavy work?",
        "tags": ["research"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_quantitative": {
        "text": "Are numbers, statistics, or mathematical modelling genuinely central to how you analyse and solve problems in your field?",
        "tags": ["quantitative"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_invest_or_audit", "q_statistics_models"],
        },
    },

    # ── CREATIVE ARTS: Film vs Animation vs Journalism ────────
    "q_portfolio": {
        "text": "Will you leave your programme with a portfolio, showreel, or body of creative work you can actually show to future employers or clients?",
        "tags": ["portfolio"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_screen_or_words", "q_studio"],
        },
    },

    "q_screen_or_words": {
        "text": "Is your creative output primarily VISUAL — things people watch on a screen like films, animations, or motion graphics — rather than written content like articles or news reports?",
        "tags": ["design"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_film_or_animation"],
            "Probably Yes":   ["q_film_or_animation"],
            "Definitely No":  ["q_journalism"],
            "Probably No":    ["q_journalism"],
        },
    },

    "q_film_or_animation": {
        "text": "Is your visual work about bringing CHARACTERS and WORLDS to life through drawing and digital illustration — as opposed to shooting and directing real people and locations on a camera?",
        "tags": ["character_animation", "3d_modelling"],
        "responses": LIKERT,
        "followups": {
            "Definitely Yes": ["q_studio"],
            "Definitely No":  ["q_film"],
        },
    },

    "q_journalism": {
        "text": "Are you learning to find real stories, verify facts, and communicate them accurately to a public audience — through articles, investigations, or broadcast journalism?",
        "tags": ["news_writing", "investigative_reporting", "newsroom_practice"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_studio": {
        "text": "Do you do hands-on production work in a dedicated studio space — on a film set, in an animation suite, or in a broadcast facility?",
        "tags": ["studio"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_film": {
        "text": "Is directing, shooting on a camera, or editing real footage into a finished film or video at the heart of what you study?",
        "tags": ["cinematography", "directing", "film_set_work"],
        "responses": LIKERT,
        "followups": {},
    },

    "q_communication_studies": {
        "text": "Do you study how media shapes public opinion at a theoretical level — analysing audiences, media effects, or editorial strategy — rather than producing content yourself?",
        "tags": ["audience_research", "media_theory", "communication_theory"],
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
        "q_numbers_or_people", "q_invest_or_audit", "q_finance",
        "q_accounting", "q_audit_focus", "q_leadership",
        "q_global_focus", "q_executive_focus", "q_org_psychology",
        "q_hospitality", "q_executive_research", "q_postgraduate",
    ],
    "School of Humanities & Social Sciences": [
        "q_mind_or_society", "q_therapy_type", "q_society_angle",
        "q_justice", "q_politics", "q_policy_focus",
        "q_clinical_practice", "q_qualitative", "q_field_work",
        "q_postgraduate", "q_thesis", "q_research",
    ],
    "School of Science & Technology": [
        "q_build_or_analyse", "q_software_style", "q_statistics_models",
        "q_enterprise_it", "q_physical_ai", "q_hardware",
        "q_security", "q_postgraduate",
    ],
    "School of Pharmacy & Health Sciences": [
        "q_health_or_chemistry", "q_patient_focused", "q_bedside_or_dispensing",
        "q_pharmacy_specific", "q_drug_or_cell", "q_biochem_focus",
        "q_pure_chemistry", "q_population_health_focus", "q_epidemiology",
        "q_practicum", "q_licensure", "q_healthcare_mgmt",
    ],
    "School of Communication, Cinematic & Creative Arts": [
        "q_screen_or_words", "q_film_or_animation", "q_journalism",
        "q_studio", "q_film", "q_communication_studies",
        "q_portfolio", "q_postgraduate",
    ],
}
