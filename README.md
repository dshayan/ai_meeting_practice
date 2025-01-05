# AI Conversation Practice

An AI-powered platform for practicing conversations with realistic personas using Claude AI. Perfect for sales, interviews, negotiations, or any professional interaction.

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

## File Structure

- `meetings_data/` - Saved conversations and evaluations
  - `meeting_with_*.json` - Complete conversation records
  - `response_evaluation_*.txt` - Detailed response evaluations
  - `meeting_evaluation_*.txt` - Meeting evaluation reports
- `prompts/` - System prompts and evaluation templates
  - `customer_creation_model.txt` - Profile creation conversation guide
  - `response_evaluation_model.txt` - Response evaluation criteria
  - `meeting_evaluation_model.txt` - Final report generation template
- `customers/` - Customer profile definitions
  - `*.txt` - Individual customer profile files
- `core/` - Core application components
  - `config.py` - Configuration and environment settings
  - `strings.py` - Application string constants
- `pages/` - Streamlit application pages
  - `create_profile.py` - Customer profile creation interface
- `chat.py` - Main chat interface
- `requirements.txt` - Python package dependencies
- `.env` - Environment variables and API keys

## Creating Custom Profiles

1. UI Method: Use "Create customer profile" in sidebar for guided profile creation
2. Manual Method: Add `.txt` files to `customers` directory with customer details

## Setup

1. Install requirements: `pip install -r requirements.txt`
2. Create `.env` file with your Anthropic API key in the format:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```
3. Run: `streamlit run chat.py`