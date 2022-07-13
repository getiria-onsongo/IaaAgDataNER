from cross_validation import CrossValidation

val = CrossValidation()
avg_metrics, found_ents, counts = val.medacy_eval()
val.print_metrics(avg_metrics, found_ents, counts)
