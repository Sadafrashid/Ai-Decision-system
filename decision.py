def recommend_decision(traits, choice1, choice2):
    score1 = 0
    score2 = 0

    # Creative vs Stable logic
    if traits["Openness"] > 5:
        score1 += 2

    if traits["Conscientiousness"] > 5:
        score2 += 2

    if traits["Extraversion"] > 5:
        score1 += 1

    if traits["Neuroticism"] > 5:
        score2 += 1

    if score1 > score2:
        return choice1, "This option matches your creative and social personality."
    else:
        return choice2, "This option is more stable and suits your personality."