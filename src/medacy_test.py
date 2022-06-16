
from medacy.model.model import Model

model = Model.load_external('medacy_model_clinical_notes')
annotation = model.predict("The patient was prescribed 1 capsule of Advil for 5 days.")
print(annotation)
