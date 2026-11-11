# Architecture

## Inference path
1. A client submits financial text to FastAPI `POST /analyze`.
2. Pydantic validates the request.
3. A lazy loader initializes ProsusAI FinBERT on the first inference request.
4. FinBERT returns positive, negative, and neutral class scores.
5. The API returns the predicted class, confidence, class scores, and model identifier.

## Batch path
CSV news -> raw_text_data -> preprocessing -> preprocessed_text -> FinBERT scoring -> sentiment_scores -> experimental trading_signals.

PostgreSQL credentials are loaded from environment variables and must not be committed.

## Evaluation guardrails
Sentiment is a text classification result, not a price forecast. Backtests should use chronological splits, avoid look-ahead leakage, and account for trading fees and slippage.
