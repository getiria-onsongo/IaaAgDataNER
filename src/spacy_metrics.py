"""
File with functions to extract and average json outputs of spacy evaluate
function. Ended up not using this now, but saving for possible later use.


Functions
----------
extract_metrics(self, prefix="metrics_fold", suffix=".json") -> dict
    creates a dict with important metrics from spacy json
average_metrics(metrics : dict) -> dict
    averages metrics
"""

def extract_metrics(prefix="metrics_fold", suffix=".json") -> dict:
      """
      Extracts a dictonary of metrics from spacy json file of metrics.

      Parameters
      ----------
      prefix : string
          start of name for each json file, going up to fold number
      suffix : string
          end of name for each json file, starting after fold number

      Returns dictonary of metrics.
      """
      metrics = defaultdict(list)
      for i in range(0, self.k_folds):
          file_name = prefix + str(i) + suffix
          json_dict = json_2_dict(file_name)
          for tag in self.tags:
              if tag in json_dict["ents_per_type"].keys():
                  data = json_dict["ents_per_type"][tag]
                  metrics[tag].append(data)
      return metrics

  def average_metrics(metrics : dict) -> dict:
      """
      Averages across folds metrics for each label as well as overall.

      Parameters
      ----------
      metrics : dict
          dictonary of metrics extracted from spacy json

      Returns dictonary of averages.
      """
      avg_metrics = {}
      p_all = []
      r_all = []
      f_all = []
      for k,v in metrics.items():
          p_temp = []
          r_temp = []
          f_temp = []
          for i in v:
              p_all.append(i.get("p"))
              r_all.append(i.get("r"))
              f_all.append(i.get("f"))

              p_temp.append(i.get("p"))
              r_temp.append(i.get("r"))
              f_temp.append(i.get("f"))
              avg_metrics[k] = [sum(p_temp)/len(p_temp), sum(r_temp)/len(r_temp), sum(f_temp)/len(f_temp)]
          avg_metrics["ALL"] = [sum(p_all)/len(p_all), sum(r_all)/len(r_all), sum(f_all)/len(f_all)]
      return avg_metrics
