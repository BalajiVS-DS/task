import re
import json


equivalent_degrees = {
    "B.Tech": ["Bachelor of Technology", "B.E.", "Bachelor of Engineering"],
    "M.Tech": ["Master of Technology", "M.E.", "Master of Engineering"],
    "B.Sc.": ["Bachelor of Science"],
    "M.Sc.": ["Master of Science"],
    "B.Com.": ["Bachelor of Commerce"],
    "M.Com.": ["Master of Commerce"],
    "B.A.": ["Bachelor of Arts"],
    "M.A.": ["Master of Arts"],
    "BBA": ["Bachelor of Business Administration"],
    "MBA": ["Master of Business Administration", "PGDM"],
    "BCA": ["Bachelor of Computer Applications"],
    "MCA": ["Master of Computer Applications"],
    "LL.B.": ["Bachelor of Laws"],
    "LL.M.": ["Master of Laws"],
    "MBBS": ["Bachelor of Medicine, Bachelor of Surgery"],
    "MD": ["Doctor of Medicine"],
    "BDS": ["Bachelor of Dental Surgery"],
    "B.Pharm": ["Bachelor of Pharmacy"],
    "M.Pharm": ["Master of Pharmacy"],
    "B.Arch": ["Bachelor of Architecture"],
    "M.Arch": ["Master of Architecture"],
    "B.Ed.": ["Bachelor of Education"],
    "M.Ed.": ["Master of Education"],
    "Ph.D.": ["Doctor of Philosophy"]
}

all_degrees = [deg for group in equivalent_degrees.values() for deg in group]
all_degrees += list(equivalent_degrees.keys())


specialization_similarity_groups = [
    ({"Computer Science", "Information Technology", "Software Engineering", "Computer Applications"}, 90),
    ({"Artificial Intelligence", "Machine Learning", "Data Science"}, 90),
    ({"Electrical Engineering", "Electronics Engineering", "Electronics and Communication Engineering"}, 80),
    ({"Mechanical Engineering", "Automobile Engineering", "Mechatronics"}, 85),
    ({"Civil Engineering", "Architecture"}, 75),
    ({"Biotechnology", "Genetic Engineering", "Bioinformatics","Biomedical", "Industrial Biotechnology"}, 85),
    ({"Finance", "Accounting", "Commerce","Business"}, 85),
    ({"Marketing", "Sales"}, 80),
    ({"Physics", "Applied Physics"}, 90),
    ({"Mathematics", "Statistics"}, 85),
    ({"Law", "Legal Studies"}, 90),
    ({"Political Science", "Public Administration"}, 75),
    ({"History", "Geography","Archaeology"}, 70),
    ({"Philosophy", "Ethics"}, 85),
    ({"Education", "Educational Technology"}, 80),
    ({"Environmental Science", "Ecology"}, 85),
    ({"Chemical Engineering", "Process Engineering", "Petrochemical Engineering", "Biochemical Engineering"}, 85),
    ({"Aerospace Engineering", "Aerodynamics", "Avionics", "Propulsion Systems"}, 85),
    ({"Textile Engineering", "Apparel Production", "Textile Chemistry"}, 85),
    ({"Agricultural Engineering", "Food Processing", "Irrigation Systems"}, 85),
    ({"Mining Engineering", "Petroleum Engineering", "Reservoir Engineering", "Drilling Engineering"}, 85),
    ({"Marine Engineering", "Ship Design", "Marine Propulsion"}, 85),
    ({"Pharmaceutical Engineering", "Drug Development", "Manufacturing Processes", "Regulatory Affairs"}, 85),
    ({"Nuclear Engineering", "Reactor Design", "Radiation Protection", "Nuclear Fuel Cycle"}, 85),
]


def extract_degree_and_specialization(text):
    text = text.strip().lower()
    found_degree = None
    found_specialization = None

    for degree in sorted(all_degrees, key=len, reverse=True):
        if degree.lower() in text:
            found_degree = degree
            break

    match = re.search(r'(in|of)\s+([A-Za-z\s&]+)', text)
    if match:
        found_specialization = match.group(2).strip()

    return found_degree, found_specialization


def get_degree_score(required_degrees, candidate_degree, equivalent_degrees):
    normalized_required = [deg.strip().lower() for deg in required_degrees]
    if any(req in {"ug", "undergraduate", "any degree"} for req in normalized_required):
        return 100

    for req_degree in required_degrees:
        for base, equivalents in equivalent_degrees.items():
            if req_degree == base or req_degree in equivalents:
                if candidate_degree == base or candidate_degree in equivalents:
                    return 100
    return 0

def get_specialization_score_grouped(required_specializations, candidate_specialization, similarity_groups):
    candidate_specialization = candidate_specialization.strip().lower()
    best_score = 0

    for req_spec in required_specializations:
        req_spec = req_spec.strip().lower()
        if candidate_specialization == req_spec:
            return 100

        for group, score in similarity_groups:
            group_lower = {s.lower() for s in group}
            if candidate_specialization in group_lower and req_spec in group_lower:
                best_score = max(best_score, score)

    return best_score

def get_total_education_score(requirement_data, candidate_data, equivalent_degrees, similarity_groups):
    candidate_text = candidate_data.get("educational_qualification", "")
    candidate_degree, candidate_specialization = extract_degree_and_specialization(candidate_text)

    if not candidate_degree or not candidate_specialization:
        return {
            "degree_score": 0,
            "specialization_score": 0,
            "total_education_score": 0,
            "note": "Could not extract degree/specialization"
        }

    degree_score = get_degree_score(
        requirement_data["educational_qualification_required"]["degree_required"],
        candidate_degree,
        equivalent_degrees
    )

    specialization_score = get_specialization_score_grouped(
        requirement_data["educational_qualification_required"]["specialization_branch_list"],
        candidate_specialization,
        similarity_groups
    )

    total_score = int(0.5 * degree_score + 0.5 * specialization_score)

    return {
        "degree_score": degree_score,
        "specialization_score": specialization_score,
        "total_education_score": total_score
    }

data_requirements = {
    "educational_qualification_required": {
        "degree_required": ["UG"],
        "specialization_branch_list": ["Computer Science", "Mechanical Engineering", "ECE"]
    }
}

data_candidate = {
    "educational_qualification": "B.Tech in Automobile Engineering"
}


result = get_total_education_score(data_requirements, data_candidate, equivalent_degrees, specialization_similarity_groups)
print(" Education Match Result:", json.dumps(result, indent=2))
