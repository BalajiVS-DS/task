def evaluate_candidate(field_scores):
    weights = {
        "degree": 25,
        "specialization": 15,
        "experience": 30,
        "notice_period": 15,
        "job_role": 10,
        "job_location": 5
    }

    pass_marks = {
        "degree": 40,
        "specialization": 40,
        "experience": 50,
        "notice_period": 50,
        "job_role": 50,
        "job_location": 40
    }

    field_validity = {}
    weighted_sum = 0
    total_weight = 0
    min_required_sum = 0

    for field, score in field_scores.items():
        weight = weights.get(field, 0)
        pass_mark = pass_marks.get(field, 50)

        # Boolean validity check
        valid = score >= pass_mark
        field_validity[field] = valid

        # Weighted actual score
        weighted_sum += score * weight

        # Weighted required minimum score
        min_required_sum += pass_mark * weight
        total_weight += weight

    overall_score = weighted_sum / total_weight if total_weight > 0 else 0
    minimum_required_score = min_required_sum / total_weight if total_weight > 0 else 0
    is_eligible = overall_score >= minimum_required_score

    return {
        "field_validity": field_validity,
        "overall_score": round(overall_score, 2),
        "minimum_required_score": round(minimum_required_score, 2),
        "is_eligible": is_eligible
    }


field_scores = {
    "degree": 100,
    "specialization": 90,
    "experience": 40,
    "notice_period": 20,
    "job_role": 60,
    "job_location": 70
}

result = evaluate_candidate(field_scores)
print(result)
