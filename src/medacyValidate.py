from medacy.tools.calculators.inter_dataset_agreement import measure_dataset
from medacy.tools.calculators.inter_dataset_agreement import format_results
from medacy.data.dataset import Dataset
import argparse
import json

gold_dataset = Dataset("Data/converted/DavisLJ11converted")
system_dataset = Dataset("Data/predictions/DavisLJ11predicted")

result = measure_dataset(gold_dataset, system_dataset, 'lenient')
output = format_results(result)
print(output)
