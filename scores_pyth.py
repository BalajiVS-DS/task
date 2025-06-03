import re
from difflib import get_close_matches
from itertools import combinations
from collections import defaultdict


tech_roles = {
    "backend_roles": {
        "Backend Developer", "API Developer", "Database Developer", "DevOps Engineer",
         "Cloud Backend Engineer", "Platform Engineer",
        "Infrastructure Engineer", "Systems Engineer", "Software Engineer - Backend",
        "Microservices Developer", "Integration Engineer", "Middleware Engineer",
        "Data Engineer", "Server-side Developer", "Security Engineer - Backend",
        "Performance Engineer", "Application Support Engineer", "Backend Architect",
        "Scalability Engineer", "Java Backend Developer", "Python Backend Developer",
        "Node.js Backend Developer", "Golang Backend Developer", "Ruby Backend Developer",
        "C#/.NET Backend Developer", "PHP Backend Developer", "REST API Developer",
        "GraphQL Developer", "Kubernetes Engineer", "NodeJS Developer", "CI/CD Engineer"
    },
    "frontend_roles": {
        "Frontend Developer", "UI/UX Designer", "Web Designer", "JavaScript Developer",
        "React Developer", "Angular Developer", "Vue.js Developer", "HTML/CSS Developer",
        "Mobile Frontend Developer", "Accessibility Engineer", "Frontend Architect",
        "Interaction Designer", "Motion Designer", "Web Animator", "SASS/LESS Developer",

    },
    "fullstack_roles": {
        "Full Stack Developer", "MEAN Stack Developer", "MERN Stack Developer",
        "LAMP Stack Developer", "Software Engineer - Full Stack", "Web Application Developer",
        "Mobile Full Stack Developer", "Frontend-Backend Integrator", "Cross-Platform Developer",
        "Technical Lead - Full Stack","React","Angular"
    },
    "data_roles": {
        "Data Scientist", "Data Analyst", "Data Engineer", "Data Architect",
        "Data Modeler", "Data Storyteller", "Business Intelligence Analyst",
        "Data Visualization Specialist", "Big Data Engineer", "Quantitative Analyst",
        "Statistician", "Data Governance Analyst", "Data Quality Analyst",
        "Data Mining Specialist", "Predictive Modeler", "ETL Developer",
        "Data Warehouse Engineer", "NLP Engineer", "Computer Vision Engineer",
        "Deep Learning Engineer"
    },
    "ai_ml_roles": {
        "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer",
        "Natural Language Processing (NLP) Engineer", "Computer Vision Engineer",
        "AI Research Scientist", "AI Trainer", "Generative AI Designer", "Prompt Engineer",
        "AI Operations Specialist", "AI Architect", "AI Product Manager",
        "AI Ethics Specialist", "Reinforcement Learning Engineer", "Speech Recognition Engineer",
        "Recommendation Systems Engineer", "AI Solutions Consultant", "AI Data Analyst",
        "AI Software Developer", "AI QA Engineer"
    },
    "cybersecurity_roles": {
        "Security Analyst", "Penetration Tester", "Network Security Engineer",
        "Application Security Engineer", "Security Architect", "Cryptographer",
        "Digital Forensics Analyst", "Threat Intelligence Analyst", "CISO", "ISSO",
        "Incident Response Analyst", "GRC Analyst", "IAM Analyst", "CTI Analyst", "DPO",
        "DRM", "ICS Security Analyst", "SCADA Security Analyst", "IT Auditor", "SOC Analyst"
    },
    "cloud_roles": {
        "Cloud Engineer", "Cloud Architect", "Cloud Consultant", "Cloud Security Engineer",
        "Cloud DevOps Engineer", "Cloud Systems Administrator", "Cloud Network Engineer",
        "Cloud Support Engineer", "Cloud Solutions Architect", "Cloud Operations Manager",
        "Cloud Compliance Manager", "Cloud Automation Engineer", "Cloud Product Manager",
        "Cloud Sales Engineer"
    },
    "devops_roles": {
        "DevOps Engineer", "Site Reliability Engineer", "IaC Engineer",
        "Release Manager", "Automation Engineer", "Build and Release Engineer",
        "Cloud DevOps Engineer", "Platform Engineer", "Monitoring Engineer"
    },
    "qa_roles": {
        "QA Engineer", "Test Automation Engineer", "Manual Tester", "QA",  "Performance Tester",
        "Security Tester", "Mobile QA Engineer", "QA Analyst", "Test Lead", "SDET",
        "Usability Tester"
    },
    "product_roles": {
        "Product Manager", "Product Owner", "Technical Product Manager", "Product Analyst",
        "Product Designer", "UX Researcher", "Growth Product Manager", "Product Marketing Manager",
        "CPO", "Product Strategist"
    },
    "project_management_roles": {
        "Project Manager", "Scrum Master", "Agile Coach", "Product Owner", "Technical Project Manager",
        "Program Manager", "Delivery Manager", "Release Manager", "Project Coordinator",
        "Portfolio Manager"
    },
    "network_roles": {
        "Network Engineer", "Network Administrator", "Network Architect", "Network Analyst",
        "Wireless Network Engineer", "VoIP Engineer", "Network Security Engineer",
        "NOC Engineer", "LAN/WAN Engineer", "Telecom Engineer"
    },
    "database_roles": {
        "Database Administrator (DBA)", "Database Developer", "Data Architect", "SQL Developer",
        "NoSQL Developer", "Database Analyst", "Data Warehouse Developer", "ETL Developer",
        "Big Data Engineer", "Database Reliability Engineer"
    },
    "support_roles": {
        "Technical Support Engineer", "Help Desk Technician", "IT Support Specialist",
        "Application Support Analyst", "Desktop Support Engineer", "Customer Support Engineer",
        "Field Service Technician", "IT Technician", "Support Analyst", "Service Desk Analyst"
    }
}

business_roles = {
    "marketing_roles": {
        "Marketing Manager", "Digital Marketing Specialist", "SEO Specialist",
        "Content Marketer", "Social Media Manager", "Brand Manager",
        "Product Marketing Manager", "Growth Marketer", "Email Marketing Specialist",
        "Marketing Analyst", "Performance Marketing Manager", "SEM Specialist",
        "Influencer Marketing Manager", "Marketing Coordinator", "Affiliate Marketing Manager"
    },
    "sales_roles": {
        "Sales Executive", "Sales Manager", "Account Executive", "Business Development Manager",
        "Inside Sales Representative", "Territory Sales Manager", "Regional Sales Manager",
        "Sales Analyst", "Channel Sales Manager", "Key Account Manager",
        "Enterprise Sales Executive", "Pre-Sales Consultant", "Client Relationship Manager"
    },
    "finance_roles": {
        "Financial Analyst", "Accountant", "Finance Manager", "Auditor",
        "Controller", "Budget Analyst", "Tax Consultant", "Treasury Analyst",
        "Investment Analyst", "Compliance Officer", "CFO", "Finance Business Partner",
        "Cost Accountant", "Payroll Specialist", "Risk Analyst"
    },
    "hr_roles": {
        "HR Manager", "HR Business Partner", "Recruiter", "Talent Acquisition Specialist",
        "Compensation and Benefits Analyst", "HR Generalist", "HR Specialist",
        "Employee Relations Manager", "Organizational Development Consultant",
        "Learning and Development Manager", "People Operations Specialist", "HR Analyst"
    },
    "operations_roles": {
        "Operations Manager", "Operations Analyst", "Process Improvement Specialist",
        "Supply Chain Manager", "Logistics Coordinator", "Inventory Manager",
        "Vendor Manager", "Procurement Analyst", "Business Operations Associate",
        "Facilities Manager", "Service Delivery Manager"
    },
    "customer_success_roles": {
        "Customer Success Manager", "Client Services Manager", "Customer Support Specialist",
        "Account Manager", "Customer Experience Manager", "Customer Onboarding Specialist",
        "Retention Specialist", "Customer Advocacy Manager", "Customer Engagement Manager"
    },
    "legal_roles": {
        "Legal Counsel", "Compliance Officer", "Contract Manager", "Corporate Lawyer",
        "Legal Analyst", "Intellectual Property Specialist", "Regulatory Affairs Specialist",
        "Legal Assistant", "Paralegal"
    },
    "admin_roles": {
        "Administrative Assistant", "Executive Assistant", "Office Manager",
        "Receptionist", "Clerical Assistant", "Data Entry Clerk", "Administrative Coordinator",
        "Personal Assistant", "Office Administrator"
    },
    "strategy_roles": {
        "Business Analyst", "Strategy Consultant", "Corporate Strategist",
        "Management Consultant", "Competitive Intelligence Analyst", "Strategy Manager",
        "Business Planner", "Business Intelligence Analyst"
    },
    "training_roles": {
        "Corporate Trainer", "Training Manager", "Learning and Development Specialist",
        "Instructional Designer", "Training Coordinator", "Leadership Coach",
        "E-learning Specialist", "Facilitator"
    }
}


medical_roles = {
    "clinical_roles": {
        "Physician", "General Practitioner", "Primary Care Physician", "Hospitalist", "Surgeon", "Doctor",
        "Cardiologist", "Neurologist", "Oncologist", "Orthopedic Surgeon", "Urologist",
        "Dermatologist", "Gastroenterologist", "Endocrinologist", "Pulmonologist",
        "Nephrologist", "Infectious Disease Specialist", "Pediatrician", "Geriatrician",
        "ENT Specialist", "Radiologist", "Anesthesiologist", "Critical Care Physician"
    },
    "nursing_roles": {
        "Registered Nurse", "Licensed Practical Nurse", "Nurse Practitioner", "Critical Care Nurse", "Nurse",
        "Surgical Nurse", "Pediatric Nurse", "Geriatric Nurse", "Oncology Nurse", "Neonatal Nurse",
        "Psychiatric Nurse", "Nurse Midwife", "Nurse Anesthetist", "Cardiac Nurse", "Emergency Room Nurse"
    },
    "allied_health_roles": {
        "Physiotherapist", "Occupational Therapist", "Speech-Language Pathologist", "Radiologic Technologist",
        "Respiratory Therapist", "Anesthesia Technician", "Medical Laboratory Technician",
        "Phlebotomist", "Optometrist", "Dietitian", "Nutritionist", "Orthoptist", "Audiologist",
        "Recreational Therapist", "Chiropractor", "Sonographer", "Perfusionist"
    },
    "pharmacy_roles": {
        "Pharmacist", "Clinical Pharmacist", "Pharmacy Technician", "Pharmaceutical Researcher",
        "Pharmacovigilance Associate", "Regulatory Affairs Specialist", "Formulation Scientist",
        "Pharmaceutical Sales Representative", "Medicinal Chemist"
    },
    "administrative_roles": {
        "Medical Biller", "Medical Coder", "Health Information Technician", "Medical Receptionist",
        "Medical Transcriptionist", "Healthcare Administrator", "Practice Manager", "Medical Office Assistant",
        "Health Services Manager", "Patient Services Coordinator", "Hospital Administrator"
    },
    "public_health_roles": {
        "Public Health Officer", "Epidemiologist", "Biostatistician", "Health Educator",
        "Community Health Worker", "Environmental Health Specialist", "Public Health Analyst",
        "Health Policy Analyst", "Global Health Specialist", "Public Health Nurse", "Disease Surveillance Officer"
    },
    "mental_health_roles": {
        "Clinical Psychologist", "Counselor", "Therapist", "Psychiatrist", "Psychiatric Nurse",
        "Substance Abuse Counselor", "Mental Health Social Worker", "Marriage and Family Therapist",
        "Behavioral Health Specialist", "Addiction Specialist", "Rehabilitation Counselor"
    }
}

educational_roles = {
    "school_education_roles": {
        "Primary School Teacher", "Elementary School Teacher", "Middle School Teacher", " Teacher",
        "High School Teacher", "Subject Teacher", "Special Education Teacher",
        "Substitute Teacher", "Classroom Assistant", "Homeroom Teacher"
    },
    "higher_education_roles": {
        "Lecturer", "Assistant Professor", "Associate Professor", "Professor",
        "Adjunct Faculty", "Research Scholar", "Postdoctoral Fellow",
        "Dean", "Academic Advisor"
    },
    "education_administration_roles": {
        "Principal", "Vice Principal", "School Administrator", "Head of Department",
        "Academic Coordinator", "Registrar", "Dean of Students", "Director of Admissions",
        "Education Policy Analyst"
    },
    "vocational_training_roles": {
        "Vocational Instructor", "Technical Trainer", "Industrial Training Instructor",
        "ITI Trainer", "Apprenticeship Coordinator", "Trade School Instructor",
        "Skill Development Trainer", "Workshop Facilitator"
    },
    "online_education_roles": {
        "Online Tutor", "eLearning Specialist", "Instructional Designer",
        "MOOC Facilitator", "Content Developer - Education", "Virtual Classroom Instructor",
        "LMS Administrator", "Remote Teaching Assistant"
    },
    "curriculum_development_roles": {
        "Curriculum Developer", "Instructional Coordinator", "Syllabus Designer",
        "Education Content Specialist", "Assessment Developer", "Standards Alignment Consultant"
    },
    "student_support_roles": {
        "School Counselor", "Career Counselor", "Academic Advisor",
        "Student Success Coach", "Guidance Counselor", "Mentor",
        "Remedial Tutor", "Behavioral Interventionist"
    },
    "special_education_roles": {
        "Special Educator", "Learning Disabilities Specialist", "Autism Support Specialist",
        "IEP Coordinator", "Speech-Language Pathologist (SLP)", "Occupational Therapist - Schools"
    },
    "educational_technology_roles": {
        "EdTech Specialist", "Technology Integration Coach", "Digital Learning Consultant",
        "Educational App Developer", "LMS Specialist", "Education Technology Trainer"
    },
    "library_roles": {
        "School Librarian", "Academic Librarian", "Library Assistant",
        "Library Media Specialist", "Archivist", "Information Resource Specialist"
    }
}


tech_domains = {k: k.replace("_roles", "") for k in tech_roles}
role_to_category = {}
category_to_dict_name = {}

# Add tech roles
for category, roles in tech_roles.items():
    domain = category.replace("_roles", "")
    category_to_dict_name[domain] = "tech"
    for role in roles:
        role_to_category[role] = domain

for category, roles in business_roles.items():
    domain = category.replace("_roles", "")
    category_to_dict_name[domain] = "business"
    for role in roles:
        role_to_category[role] = domain


for category, roles in medical_roles.items():
    domain = category.replace("_roles", "")
    category_to_dict_name[domain] = "medical"
    for role in roles:
        role_to_category[role] = domain

for category, roles in educational_roles.items():
    domain = category.replace("_roles", "")
    category_to_dict_name[domain] = "educational"
    for role in roles:
        role_to_category[role] = domain


DOMAIN_SIMILARITY_MATRIX = {
    "backend": {"backend": 1.0, "devops": 0.6, "cloud": 0.5, "data": 0.4, "ai_ml": 0.3},
    "frontend": {"frontend": 1.0, "fullstack": 0.7, "product": 0.4},
    "fullstack": {"fullstack": 1.0, "frontend": 0.7, "backend": 0.7},
    "data": {"data": 1.0, "ai_ml": 0.7, "cloud": 0.4, "backend": 0.4, "database": 0.6},
    "ai_ml": {"ai_ml": 1.0, "data": 0.7, "cloud": 0.3},
    "cybersecurity": {"cybersecurity": 1.0, "network": 0.6, "cloud": 0.5},
    "cloud": {"cloud": 1.0, "backend": 0.5, "devops": 0.8, "ai_ml": 0.3},
    "devops": {"devops": 1.0, "cloud": 0.8, "backend": 0.6},
    "qa": {"qa": 1.0},
    "product": {"product": 1.0, "project_management": 0.6, "frontend": 0.4},
    "project_management": {"project_management": 1.0, "product": 0.6},
    "network": {"network": 1.0, "cybersecurity": 0.6},
    "database": {"database": 1.0, "data": 0.6},
    "support": {"support": 1.0},
    "management": {"management": 1.0},
    "finance": {"finance": 1.0},
    "marketing": {"marketing": 1.0},
    "sales": {"sales": 1.0},
    "hr": {"hr": 1.0},
    "legal": {"legal": 1.0},
    "consulting": {"consulting": 1.0, "management": 0.5, "finance": 0.4},


    #BUSINESS

"marketing": { "marketing": 1.0, "sales": 0.7, "product": 0.6, "strategy": 0.5, "customer_success": 0.6, "operations": 0.4, "training": 0.3 },
"sales": { "sales": 1.0, "marketing": 0.7, "customer_success": 0.7, "product": 0.5, "strategy": 0.4, "finance": 0.3, "operations": 0.4 },
"finance": { "finance": 1.0, "strategy": 0.6, "operations": 0.5, "legal": 0.4, "hr": 0.3, "admin": 0.2 },
"hr": { "hr": 1.0, "training": 0.7, "admin": 0.5, "operations": 0.4, "strategy": 0.3 },
"operations": { "operations": 1.0, "finance": 0.5, "hr": 0.4, "sales": 0.4, "admin": 0.4, "customer_success": 0.3 },
"customer_success": { "customer_success": 1.0, "sales": 0.7, "marketing": 0.6, "operations": 0.3 },
"legal": { "legal": 1.0, "finance": 0.4, "operations": 0.3, "admin": 0.3 }, "admin": { "admin": 1.0, "hr": 0.5, "legal": 0.3, "operations": 0.4 },
"strategy": { "strategy": 1.0, "finance": 0.6, "marketing": 0.5, "sales": 0.4, "product": 0.6, "hr": 0.3 },
"training": { "training": 1.0, "hr": 0.7, "admin": 0.4, "operations": 0.3 },
"product": { "product": 1.0, "marketing": 0.6, "sales": 0.5, "strategy": 0.6 },

#MEDICAL
"clinical": { "clinical": 1.0, "nursing": 0.8, "allied_health": 0.7, "pharmacy": 0.6, "administrative": 0.4, "public_health": 0.5, "mental_health": 0.6 },
"nursing": { "clinical": 0.8, "nursing": 1.0, "allied_health": 0.7, "pharmacy": 0.5, "administrative": 0.4, "public_health": 0.6, "mental_health": 0.7 },
"allied_health": { "clinical": 0.7, "nursing": 0.7, "allied_health": 1.0, "pharmacy": 0.5, "administrative": 0.5, "public_health": 0.6, "mental_health": 0.6 },
 "pharmacy": { "clinical": 0.6, "nursing": 0.5, "allied_health": 0.5, "pharmacy": 1.0, "administrative": 0.5, "public_health": 0.5, "mental_health": 0.4 },
 "administrative": { "clinical": 0.4, "nursing": 0.4, "allied_health": 0.5, "pharmacy": 0.5, "administrative": 1.0, "public_health": 0.6, "mental_health": 0.4 },
"public_health": { "clinical": 0.5, "nursing": 0.6, "allied_health": 0.6, "pharmacy": 0.5, "administrative": 0.6, "public_health": 1.0, "mental_health": 0.6 },
 "mental_health": { "clinical": 0.6, "nursing": 0.7, "allied_health": 0.6, "pharmacy": 0.4, "administrative": 0.4, "public_health": 0.6, "mental_health": 1.0 },

#EDUCATIONAL

"school_education": { "school_education": 1.0, "higher_education": 0.6, "student_support": 0.7, "special_education": 0.7, "curriculum_development": 0.5, "education_administration": 0.6 },
"higher_education": { "school_education": 0.6, "higher_education": 1.0, "education_administration": 0.7, "curriculum_development": 0.6, "online_education": 0.6, "student_support": 0.5 },
"education_administration": { "education_administration": 1.0, "school_education": 0.6, "higher_education": 0.7, "curriculum_development": 0.5, "student_support": 0.4 },
"vocational_training": { "vocational_training": 1.0, "technical_training": 0.8, "online_education": 0.6, "curriculum_development": 0.5 },
"online_education": { "online_education": 1.0, "higher_education": 0.6, "vocational_training": 0.6, "educational_technology": 0.8, "curriculum_development": 0.5 },
"curriculum_development": { "curriculum_development": 1.0, "school_education": 0.5, "higher_education": 0.6, "online_education": 0.5, "education_administration": 0.5 },
"student_support": { "student_support": 1.0, "school_education": 0.7, "higher_education": 0.5, "special_education": 0.6, "education_administration": 0.4 },
"special_education": { "special_education": 1.0, "student_support": 0.6, "school_education": 0.7 },
"educational_technology": { "educational_technology": 1.0, "online_education": 0.8, "higher_education": 0.5, "curriculum_development": 0.5 },
"library": { "library": 1.0, "school_education": 0.4, "higher_education": 0.5, "education_administration": 0.4 }


}



domain_similarity = {
    (d1, d2): sim for d1, m in DOMAIN_SIMILARITY_MATRIX.items() for d2, sim in m.items()
}



import re
from difflib import get_close_matches

# Basic normalization: lowercase and remove all non-alphanumeric characters
def normalize_text(text: str) -> str:
    return re.sub(r"[^\w]", "", text.lower())

# Build a set of all known roles
all_roles = set(role_to_category.keys())

# Mapping from normalized role strings to their original format
norm_to_role = {normalize_text(r): r for r in all_roles}

# Fuzzy match a given role to the closest known role using normalized text
def normalize_role(role: str) -> str:
    norm = normalize_text(role)
    match = get_close_matches(norm, norm_to_role.keys(), n=1, cutoff=0.6)
    return norm_to_role[match[0]] if match else role

# Extract keywords from role by splitting normalized string (removes special characters)
def extract_keywords(role: str) -> set:
    return set(normalize_text(role).split())

# Compute similarity between two job roles
def get_role_similarity(role1: str, role2: str) -> float:
    # Normalize both roles to the closest known job titles
    role1 = normalize_role(role1)
    role2 = normalize_role(role2)

    # Exact match
    if role1 == role2:
        return 1.0

    # Get categories for each role (e.g., "AI/ML", "Data", "DevOps")
    cat1 = role_to_category.get(role1)
    cat2 = role_to_category.get(role2)

    # If either role is not categorized, return 0 (no similarity)
    if not cat1 or not cat2:
        return 0.0

    # Get domain dictionary group names (e.g., "ai_ml_roles", "data_roles")
    dict1 = category_to_dict_name.get(cat1)
    dict2 = category_to_dict_name.get(cat2)

    # If roles are in different domains (e.g., Data vs DevOps), return 0
    if dict1 != dict2:
        return 0.0

    # If roles belong to the same category (e.g., both "Data"), compute keyword overlap
    if cat1 == cat2:
        kw1, kw2 = extract_keywords(role1), extract_keywords(role2)
        overlap = len(kw1 & kw2)                         # common keywords
        total = max(len(kw1), len(kw2))                  # normalization factor
        return round(0.5 + 0.3 * (overlap / total if total else 0), 2)

    # If roles belong to different categories in the same domain, use domain similarity matrix
    return domain_similarity.get((cat1, cat2), domain_similarity.get((cat2, cat1), 0.0))


if __name__ == "__main__":
    print(get_role_similarity("AI Data Analyst", "DevOps Engineer"))
    print(get_role_similarity("Data Scientist", "AI Data Analyst"))
    print(get_role_similarity("Dataa scientist", "Data Base Admin"))
    print(get_role_similarity("NodeejS Developer", "NodeJS Developer"))
    print(get_role_similarity("Data Scientist", "Data Analyst"))
    print(get_role_similarity("React Developer", "Angular Developer"))
    print(get_role_similarity("DevOps Engineer", "CI/CD Engineer"))
    print(get_role_similarity("Monitoring Engineer", "Platform Engineer"))
    print(get_role_similarity("Site Reliability Engineeer", "Platform Engineer"))
    print(get_role_similarity("Doctor","Nurse"))
    print(get_role_similarity("Professor","Dean"))
