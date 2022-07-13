from cross_validation import crossvalidation

class evaluation:
    def __init__(model):
        self.model = model
    def evaluate():
        val = crossvalidation()
        avg_metrics, found_ents = val.medacy_eval()
        val.print_metrics(avg_metrics, found_ents)

if __name__ == '__main__':
    eval = evaluation()
    eval.evaluate()
