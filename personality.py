def calculate_personality(answers):
    traits = {
        "Openness": 0,
        "Conscientiousness": 0,
        "Extraversion": 0,
        "Agreeableness": 0,
        "Neuroticism": 0
    }

    traits["Openness"] = sum(answers[0:2])
    traits["Conscientiousness"] = sum(answers[2:4])
    traits["Extraversion"] = sum(answers[4:6])
    traits["Agreeableness"] = sum(answers[6:8])
    traits["Neuroticism"] = sum(answers[8:10])

    return traits