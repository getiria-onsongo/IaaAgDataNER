from medacy.tools.calculators.inter_dataset_agreement import measure_dataset
from medacy.tools.calculators.inter_dataset_agreement import format_results
from medacy.data.dataset import Dataset
import json

gold_dataset = Dataset("Data/converted/DavisLJ11")
spacy_dataset = Dataset("Data/predictions/DavisLJ11SpacyAnn")
pos_dataset = Dataset("Data/predictions/DavisLJ11PosAnn")

print("Spacy results")
print("____________________________")
result = measure_dataset(gold_dataset, spacy_dataset, 'lenient')
output = format_results(result)
print(output)

print("\nPOS results")
print("____________________________")
result = measure_dataset(gold_dataset, pos_dataset, 'lenient')
output = format_results(result)
print(output)
