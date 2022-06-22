from medacy.tools.calculators.inter_dataset_agreement import measure_dataset
from medacy.tools.calculators.inter_dataset_agreement import format_results
from medacy.data.dataset import Dataset


gold_dataset = Dataset("Data/Input")
system_dataset = Dataset("Data/Output")

result = measure_dataset(gold_dataset, system_dataset)
output = format_results(result)
print(result)
