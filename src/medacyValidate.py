from medacy.tools.calculators.inter_dataset_agreement import measure_dataset
from medacy.tools.calculators.inter_dataset_agreement import format_results
from medacy.data.dataset import Dataset
import argparse
import json
import pprint
from medacy.data.annotations import Annotations
from medacy.data.data_file import DataFile


gold_dataset = Dataset("Data/DavisLJ11Test")
system_dataset = Dataset("Data/DavisLJ11Train")


# for file in system_dataset:
#     print(file.file_name, str(file.txt_path), str(file.ann_path))

# entities = json.dumps(gold_dataset.get_labels(as_list=True))
# counts = gold_dataset.compute_counts()
# print(f"Entities: {entities}")
# pprint.pprint(counts)


result = measure_dataset(gold_dataset, system_dataset, 'lenient')
output = format_results(result)
print(result)
