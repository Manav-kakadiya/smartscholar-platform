from transformers import pipeline
import re

# Load sentiment analysis model (lightweight)
try:
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
except:
    print("⚠️ Transformers model not loaded. Install with: pip install transformers torch")
    sentiment_analyzer = None

def analyze_assignment(text: str) -> dict:
    """Analyze assignment text and provide feedback"""
    
    if not text or len(text.strip()) < 50:
        return {
            "word_count": len(text.split()),
            "feedback": "Text too short to analyze. Please provide more content.",
            "score": 0,
            "suggestions": ["Add more detailed explanation", "Expand your arguments"]
        }
    
    # Basic metrics
    word_count = len(text.split())
    sentence_count = len([s for s in text.split('.') if s.strip()])
    avg_sentence_length = word_count / max(sentence_count, 1)
    
    # Grammar checks (simple)
    grammar_issues = []
    
    # Check for common errors
    if ' i ' in text.lower() and not any(x in text for x in ['I am', 'I have', 'I will']):
        grammar_issues.append("Use 'I' (capital) instead of 'i'")
    
    if text.count('  ') > 0:
        grammar_issues.append("Multiple spaces detected")
    
    if not text[0].isupper():
        grammar_issues.append("Text should start with capital letter")
    
    # Sentiment analysis
    sentiment_score = 0.5  # neutral default
    if sentiment_analyzer:
        try:
            sentiment = sentiment_analyzer(text[:512])[0]  # Limit to 512 chars
            sentiment_score = sentiment['score'] if sentiment['label'] == 'POSITIVE' else 1 - sentiment['score']
        except:
            pass
    
    # Calculate score
    score = 50  # Base score
    
    # Word count scoring
    if word_count >= 300:
        score += 20
    elif word_count >= 200:
        score += 15
    elif word_count >= 100:
        score += 10
    
    # Sentence structure
    if 10 <= avg_sentence_length <= 25:
        score += 15
    else:
        score += 5
    
    # Grammar
    if len(grammar_issues) == 0:
        score += 15
    elif len(grammar_issues) <= 2:
        score += 10
    
    score = min(100, score)
    
    # Generate feedback
    feedback_parts = []
    
    if word_count < 150:
        feedback_parts.append("Consider expanding your response with more details.")
    elif word_count > 500:
        feedback_parts.append("Good length! Your response is comprehensive.")
    
    if avg_sentence_length < 10:
        feedback_parts.append("Try using more complex sentences to improve flow.")
    elif avg_sentence_length > 30:
        feedback_parts.append("Some sentences are quite long. Consider breaking them up.")
    
    if len(grammar_issues) > 0:
        feedback_parts.append(f"Grammar suggestions: {', '.join(grammar_issues[:3])}")
    else:
        feedback_parts.append("Grammar looks good!")
    
    feedback = " ".join(feedback_parts) if feedback_parts else "Good work overall!"
    
    # Suggestions
    suggestions = []
    if score < 70:
        suggestions.append("Add more supporting evidence")
        suggestions.append("Improve sentence structure")
    if len(grammar_issues) > 0:
        suggestions.extend(grammar_issues[:2])
    
    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "grammar_issues": len(grammar_issues),
        "score": score,
        "feedback": feedback,
        "suggestions": suggestions,
        "sentiment_score": round(sentiment_score, 2)
    }

# Test function
if __name__ == "__main__":
    sample_text = """
    The concept of machine learning has revolutionized the way we approach problem-solving 
    in computer science. Machine learning algorithms can learn from data and make predictions 
    without being explicitly programmed. This has applications in many fields including 
    healthcare, finance, and education.
    """
    
    result = analyze_assignment(sample_text)
    print("Assignment Analysis:")
    print(f"Score: {result['score']}/100")
    print(f"Word Count: {result['word_count']}")
    print(f"Feedback: {result['feedback']}")
    print(f"Suggestions: {result['suggestions']}")