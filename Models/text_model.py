# models/text_model.py
from transformers import pipeline

class TextModel:
    def __init__(self):
        self.model_name = "BART Summarizer"
        self.category = "Text (NLP - Summarization)"
        self.description = "Summarizes long text into concise summaries."
        
        self.model = pipeline(
            "summarization",  # changed task
            model="facebook/bart-large-cnn"  # changed model
        )

    def run(self, text: str):
        try:
            result = self.model(text)
            return result
        except Exception as e:
            return f"Error: {str(e)}"
