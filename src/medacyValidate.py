from inter_dataset_agreement import measure_dataset
from inter_dataset_agreement import format_results
from dataset import Dataset
import json


print("Fold 0")
print("____________________________")
result = measure_dataset(Dataset("fold_0_results/gold_bratt"), Dataset("fold_0_results/pred_bratt"), 'lenient')
output = format_results(result)
print(output)

print("\nFold 1")
print("____________________________")
result = measure_dataset(Dataset("fold_1_results/gold_bratt"), Dataset("fold_1_results/pred_bratt"), 'lenient')
output = format_results(result)
print(output)


print("\nFold 2")
print("____________________________")
result = measure_dataset(Dataset("fold_2_results/gold_bratt"), Dataset("fold_2_results/pred_bratt"), 'lenient')
output = format_results(result)
print(output)


print("\nFold 3")
print("____________________________")
result = measure_dataset(Dataset("fold_3_results/gold_bratt"), Dataset("fold_3_results/pred_bratt"), 'lenient')
output = format_results(result)
print(output)

print("\nFold 4")
print("____________________________")
result = measure_dataset(Dataset("fold_4_results/gold_bratt"), Dataset("fold_4_results/pred_bratt"), 'lenient')
output = format_results(result)
print(output)
