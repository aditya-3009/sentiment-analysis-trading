# Evaluation protocol

A model identifier alone is not evidence of project performance. Before publishing benchmark claims, evaluate on a labelled dataset separate from any training data.

## Recommended protocol

1. Select a documented financial sentiment dataset (for example, Financial PhraseBank) and record its source, licence, version, and label mapping.
2. Remove duplicates and inspect class balance.
3. Create a fixed train/validation/test split with a recorded random seed. If using pretrained FinBERT without fine-tuning, reserve the test split for final evaluation.
4. Map labels consistently to `positive`, `negative`, and `neutral`.
5. Report accuracy, macro precision, macro recall, macro F1, and a confusion matrix.
6. Include per-class precision/recall/F1 because class imbalance can hide poor minority-class performance.
7. Record hardware, package versions, model identifier, batch size, and inference latency methodology.

## Important distinction

The API confidence score is the model's output score, not a calibrated probability. It is not the probability that a stock will rise or fall.

## Future extensions

- Batch prediction endpoint.
- Reproducible evaluation CLI and reports.
- Confidence calibration and error analysis.
- Time-aware evaluation to reduce temporal leakage.
- Comparison against a TF-IDF + classical ML baseline.
