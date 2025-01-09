# Pitch Perfect

An AI-powered platform for realistic conversation practice, ideal for sales, interviews, negotiations, and professional interactions.

## Features

- Create custom customer profiles through guided conversation
- Practice conversations with AI-powered customer personas
- Real-time response evaluation from the customer's perspective
- Detailed meeting reports with scoring across multiple criteria
- Review past meetings and performance history

## Usage

1. Create a new customer profile or select an existing one
2. Start your conversation with the AI customer
3. Each of your responses is automatically evaluated from the customer's perspective
4. Type "freeze and report" to end the conversation and get a final evaluation
5. Review past conversations and evaluations in the meetings_data folder

## Setup

1. Install requirements: `pip install -r requirements.txt`
2. Create `.env` file with your Anthropic API key in the format:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```
3. Run: `streamlit run pages/3_💬_Meet.py`