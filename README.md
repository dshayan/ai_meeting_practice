# AI Conversation Practice

An AI-powered platform for practicing conversations with realistic personas using Claude AI. Perfect for sales, interviews, negotiations, or any professional interaction.

## Features

- Practice conversations with customizable AI customer profiles
- Detailed evaluation reports with scoring across multiple criteria
- Track your progress with automatically saved conversations

## Setup

1. Install requirements: `pip install -r requirements.txt`
2. Create `.env` file with your Anthropic API key
3. Run: `streamlit run chat.py`

## Usage

1. Select a customer profile
2. Start your conversation
3. Each response is automatically evaluated and saved
4. Type "freeze and report" to end the conversation and get a final evaluation
5. Review past conversations and evaluations in the meetings_data folder

## File Structure

- `meetings_data/` - Saved conversations and evaluations
  - `meeting_with_*.json` - Complete conversation records
  - `vendor_evaluation_*.txt` - Detailed response evaluations
  - `vendor_report_*.txt` - Final evaluation reports
- `prompts/` - System prompts and evaluation templates
- `customers/` - Customer profile definitions
- `core/` - Core application components
  - `config.py` - Configuration and environment settings
  - `strings.py` - Application string constants

## Creating Custom Profiles

Add new profiles in the `customers` directory as `.txt` files with:
- Background information
- Communication style
- Key concerns
- Decision-making factors
- Personality traits
- Success metrics
- Red flags