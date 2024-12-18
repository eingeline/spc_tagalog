from transformers import AutoTokenizer, AutoModelForMaskedLM
from rouge_score import rouge_scorer
from bert_score import score as bert_score

modelname = "jcblaise/roberta-tagalog-base"
tokenizer = AutoTokenizer.from_pretrained(modelname)
model = AutoModelForMaskedLM.from_pretrained(modelname)

max_length = 128

# Input will be user input
input_text = input("Enter prompt: ").strip()

# Reference text
reference_text = "Ang Italy ang bansang may pinakamaraming naitalang kaso ng coronavirus sa labas ng Asia."


if len(tokenizer.encode(reference_text)) > max_length:
    reference_text = tokenizer.decode(tokenizer.encode(reference_text)[:max_length], skip_special_tokens=True)

if input_text and reference_text:
    print("\n\n")
    print(f"Candidate input length: {len(tokenizer.encode(input_text))}, Content: {input_text}")
    print(f"Reference input length: {len(tokenizer.encode(reference_text))}, Content: {reference_text}")

    # ROUGE Score calculation
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(reference_text, input_text)

    # BERTScore calculation
    P, R, F1 = bert_score(
        [input_text],
        [reference_text],
        lang="tl",  # For English. Use 'multilingual' for mixed-language or set to 'tl' for Tagalog if supported.
        verbose=True
    )

    # Print bert and rouge score
    print("\n")
    print(f"BERTScore Precision: {P[0]:.4f}")
    print(f"BERTScore Recall: {R[0]:.4f}")
    print(f"BERTScore F1 Score: {F1[0]:.4f}")


    print(f"ROUGE-1 F1 score: {rouge_scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-2 F1 score: {rouge_scores['rouge2'].fmeasure:.4f}")
    print(f"ROUGE-L F1 score: {rouge_scores['rougeL'].fmeasure:.4f}")

else:
    print("\n\n")
    print("Cannot compute BERTScore or ROUGE scores due to empty input.")
