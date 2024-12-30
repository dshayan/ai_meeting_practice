# Momentum - AI Conversation Practice

An AI-powered platform for practicing conversations with realistic personas. Perfect for sales, interviews, negotiations, or any professional interaction.

## Features

- Practice conversations with customizable AI profiles
- Get real-time feedback on your performance
- Track your progress over time with saved conversations
- Detailed evaluation reports with actionable insights

## Setup

1. Install requirements: `pip install -r requirements.txt`
2. Create `.env` file with your OpenAI API key
3. Run: `streamlit run chat.py`

## Usage

1. Select or create a conversation profile
2. Start your conversation
3. Type "freeze and report" to end the conversation and get your evaluation
4. Review saved conversations in the meetings folder

## Creating Custom Profiles

Add new profiles in the `prompts/customers` directory as `.txt` files with:
- Background information
- Communication style
- Key concerns
- Decision-making factors
- Personality traits