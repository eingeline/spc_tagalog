from transformers import pipeline, AutoTokenizer, AutoModelForMaskedLM
from rouge_score import rouge_scorer

modelname = "jcblaise/roberta-tagalog-base"
tokenizer = AutoTokenizer.from_pretrained(modelname)
model = AutoModelForMaskedLM.from_pretrained(modelname)

exit = True
n = 0

max_length = 128

# Input will be user input
input_text = input("Enter prompt: ")

# Adjust these parameters to fine-tune the generation
top_k = 50
score_threshold = 0.1

while exit:
    # input_masked is the one fed in the pipeline as the input is kept updated every after masked fill
    input_masked = (input_text + " <mask>")[-max_length:]

    # Fill-mask model
    ml = pipeline("fill-mask", model=model, tokenizer=tokenizer)
    results = ml(input_masked, top_k=top_k)

    # Remove punctuation from predictions
    filtered_results = []
    for result in results:
        if result['score'] >= score_threshold:
            if not any(char.isalpha() for char in result['token_str']):  # Check if only punctuation
                continue
            filtered_results.append(result)

    if filtered_results:
        input_result = filtered_results[0]["token_str"]
        input_text += input_result
        print(input_text)

        n += 1
        if input_result == ".":
            exit = False
    else:
        print("No valid predictions found.")
        break

'''
# test data
reference_text = "Si Jose Rizal ang tinaguriang pambansyang bayani."

# rouge metric
scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
scores = scorer.score(reference_text, input_text)

# to ensure reference text is within limits
if len(tokenizer.encode(reference_text)) > max_length:
    reference_text = tokenizer.decode(tokenizer.encode(reference_text)[:max_length])

# to check for empty inputs
if input_text.strip() and reference_text.strip():
    print("\n\n")
    print(f"Candidate input length: {len(tokenizer.encode(input_text))}, Content: {input_text}")
    print(f"Reference input length: {len(tokenizer.encode(reference_text))}, Content: {reference_text}")

    print("\n")
    print(f"ROUGE-1 F1 score: {scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-L F1 score: {scores['rougeL'].fmeasure:.4f}")

else:
    print("\n\n")
    print("Cannot compute ROUGE score due to empty input.")
'''