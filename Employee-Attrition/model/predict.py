import pickle
import pandas as pd 

#import the model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)

MODEL_VERSION = '1.0.0'

class_labels = model.classes_.tolist()

def predict_output(user_input: dict):

    input_df = pd.DataFrame(user_input)

    predicted_class = model.predict(input_df)[0]

    probabilities = model.predict_proba(input_df)[0]
    confidence = max(probabilities)

    class_probs = {
        str(label): round(float(p), 4)
        for label, p in zip(class_labels, probabilities)}

    return {
        "predicted_category": int(predicted_class),
        "confidence": round(float(confidence), 4),
        "class_probabilities": class_probs
    }
