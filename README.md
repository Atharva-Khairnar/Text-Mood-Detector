# Text Mood Detector

A web-based application that analyzes text to detect and display emotions. It uses advanced natural language processing techniques to identify various emotions including happiness, sadness, surprise, fear, and disgust.

## Features

- 🎨 Modern and user-friendly web interface
- 😊 Detects multiple emotions: Happy, Sad, Surprised, Scared, and Disgusted
- 🔍 Advanced sentiment analysis with:
  - Punctuation-based analysis (exclamation marks, question marks, etc.)
  - Pattern recognition (repeated letters, all caps)
  - Context-aware analysis (phrases like "not happy" or "but")
- 📊 Confidence scores for emotion detection
- 🎭 Emoji-based visual feedback
- 🎨 Color-coded emotion display

## Emotions Detected

- 😊 Happy
- 😢 Sad
- 🤔 Neutral
- 😲 Surprised
- 😨 Scared
- 🤢 Disgusted

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/text-mood-detector.git
   ```

2. Install the required dependencies:
   ```bash
   pip install flask transformers torch numpy
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://127.0.0.1:5001`

## Usage

1. Enter your text in the input field
2. Click the "Analyze" button
3. The application will display:
   - The detected emotion
   - A confidence score
   - A corresponding emoji
   - A color-coded display

## Technology Stack

- Backend: Python (Flask)
- Frontend: HTML, CSS, JavaScript
- Natural Language Processing: Custom sentiment analysis
- Machine Learning: Pattern recognition and context analysis

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Thanks to the Flask team for the excellent web framework
- Special thanks to the Transformers library for enabling advanced text processing
