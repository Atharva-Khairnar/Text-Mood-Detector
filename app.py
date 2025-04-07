from flask import Flask, render_template, request
import torch
from transformers import pipeline
import numpy as np
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    
    # List of positive and negative words and expressions
    positive_words = [
        'happy', 'good', 'great', 'awesome', 'love', 'best', 'amazing', 'fantastic', 'excellent', 
        'wonderful', 'joyful', 'excited', 'pleased', 'delighted', 'satisfied',
        'yay', 'yay!', 'yay!!', 'yay!!!', 'yay!!!!', 'yay!!!!!',
        'cool', 'awesome', 'amazing', 'fantastic', 'wonderful',
        'super', 'excellent', 'terrific', 'marvelous', 'splendid',
        'brilliant', 'outstanding', 'impressive', 'fantastic', 'terrific',
        'great', 'good', 'nice', 'wonderful', 'amazing',
        'superb', 'excellent', 'fantastic', 'terrific', 'marvelous',
        'splendid', 'brilliant', 'outstanding', 'impressive', 'fantastic'
    ]
    
    negative_words = [
        'sad', 'bad', 'terrible', 'awful', 'hate', 'worst', 'angry', 'frustrated', 'disappointed', 
        'upset', 'annoyed', 'unhappy', 'depressed', 'miserable',
        'terrible', 'awful', 'horrible', 'dreadful', 'atrocious',
        'abysmal', 'lousy', 'rotten', 'crummy', 'mediocre',
        'poor', 'bad', 'subpar', 'inferior', 'second-rate',
        'unhappy', 'miserable', 'depressed', 'melancholy', 'sorrowful',
        'gloomy', 'pessimistic', 'hopeless', 'despairing', 'disheartened'
    ]
    
    # Add surprise/shock words
    surprise_words = [
        'wow', 'whoa', 'amazing', 'incredible', 'unbelievable',
        'surprised', 'shocked', 'astonished', 'astounded',
        'mind-blowing', 'jaw-dropping', 'incredulous',
        'amazed', 'flabbergasted', 'stunned'
    ]
    
    # Add fear words
    fear_words = [
        'scared', 'afraid', 'terrified', 'fearful', 'petrified',
        'horrified', 'panicked', 'anxious', 'nervous', 'worried',
        'frightened', 'terrifying', 'horrible', 'dreadful',
        'nightmarish', 'menacing', 'threatening', 'dangerous'
    ]
    
    # Add disgust words
    disgust_words = [
        'gross', 'disgusting', 'yucky', 'nasty', 'vile',
        'repulsive', 'revolting', 'horrid', 'filthy', 'dirty',
        'slimy', 'icky', 'smelly', 'stinky', 'putrid',
        'rancid', 'rotten', 'foul', 'offensive', 'abhorrent',
        'repugnant', 'contaminated', 'tainted', 'poisonous',
        'noxious', 'noxious', 'repellent', 'offensive', 'repulsive',
        'ew', 'eww', 'ewww', 'ewwww', 'ewwwww'
    ]
    
    # Convert text to lowercase for comparison
    text_lower = text.lower()
    
    # Count positive and negative words
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    surprise_count = sum(1 for word in surprise_words if word in text_lower)
    fear_count = sum(1 for word in fear_words if word in text_lower)
    disgust_count = sum(1 for word in disgust_words if word in text_lower)
    
    # Check for 'ew' with repeated 'w's
    ew_count = len(re.findall(r'eww+', text_lower))
    disgust_count += ew_count
    
    # Calculate total words for better confidence
    total_words = len(text_lower.split())
    if total_words == 0:
        total_words = 1  # Avoid division by zero
    
    # Initialize base confidence
    if positive_count > negative_count:
        emotion = 'Happy'
        emoji = '😊'
        color = '#4CAF50'
        confidence = min(100, round((positive_count / total_words) * 100, 2))
    elif negative_count > positive_count:
        emotion = 'Sad'
        emoji = '😢'
        color = '#f44336'
        confidence = min(100, round((negative_count / total_words) * 100, 2))
    else:
        emotion = 'Neutral'
        emoji = '😐'
        color = '#9e9e9e'
        confidence = 0
    
    # Check for surprise/shock
    if surprise_count > 0:
        if surprise_count > 2:
            emotion = 'Surprised'
            emoji = '😲'
            color = '#FFA500'
            confidence = min(100, round((surprise_count / total_words) * 100, 2))
        else:
            confidence = min(100, confidence + (surprise_count * 10))
    
    # Check for fear
    if fear_count > 0:
        if fear_count > 2:
            emotion = 'Scared'
            emoji = '😨'
            color = '#FF69B4'
            confidence = min(100, round((fear_count / total_words) * 100, 2))
        else:
            confidence = min(100, confidence + (fear_count * 10))
    
    # Check for disgust
    if disgust_count > 0:
        if disgust_count > 2 or ew_count > 0:
            emotion = 'Disgusted'
            emoji = '🤢'
            color = '#8B0000'
            confidence = min(100, round((disgust_count / total_words) * 100, 2))
        else:
            confidence = min(100, confidence + (disgust_count * 10))
    
    # Add punctuation-based analysis
    # Count exclamation marks
    exclamation_count = text.count('!')
    if exclamation_count > 0:
        if emotion == 'Happy':
            confidence = min(100, confidence + (exclamation_count * 5))
        elif emotion == 'Surprised' or emotion == 'Scared' or emotion == 'Disgusted':
            confidence = min(100, confidence + (exclamation_count * 8))
        else:
            confidence = min(100, confidence + (exclamation_count * 3))
    
    # Check for question marks
    question_count = text.count('?')
    if question_count > 0:
        confidence = max(0, confidence - (question_count * 5))
    
    # Check for multiple punctuation marks
    multiple_punctuation = re.findall(r'[!?.]{2,}', text)
    if multiple_punctuation:
        if emotion == 'Happy':
            confidence = min(100, confidence + (len(multiple_punctuation) * 10))
        elif emotion == 'Surprised' or emotion == 'Scared' or emotion == 'Disgusted':
            confidence = min(100, confidence + (len(multiple_punctuation) * 12))
        else:
            confidence = min(100, confidence + (len(multiple_punctuation) * 7))
    
    # Add pattern-based analysis
    # Check for all caps (indicating emphasis)
    if any(word.isupper() for word in text.split()):
        if emotion == 'Happy':
            confidence = min(100, confidence + 15)
        elif emotion == 'Surprised' or emotion == 'Scared' or emotion == 'Disgusted':
            confidence = min(100, confidence + 20)
        else:
            confidence = min(100, confidence + 10)
    
    # Check for repeated letters (like 'happyyyy')
    repeated_letters = re.findall(r'(.)\1{2,}', text)
    if repeated_letters:
        if emotion == 'Happy':
            confidence = min(100, confidence + (len(repeated_letters) * 8))
        elif emotion == 'Surprised' or emotion == 'Scared' or emotion == 'Disgusted':
            confidence = min(100, confidence + (len(repeated_letters) * 12))
        else:
            confidence = min(100, confidence + (len(repeated_letters) * 5))
    
    # Add minimum confidence threshold
    if confidence < 20:
        emotion = 'Neutral'
        emoji = '😐'
        color = '#9e9e9e'
        confidence = 0
    
    return {
        'emotion': emotion,
        'confidence': confidence,
        'emoji': emoji,
        'color': color
    }

if __name__ == '__main__':
    print("Starting Text Mood Detector...")
    app.run(debug=True, port=5001, host='127.0.0.1')
