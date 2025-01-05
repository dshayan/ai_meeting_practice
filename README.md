# AI Conversation Practice

An AI-powered platform for practicing conversations with realistic personas using Claude AI. Perfect for sales, interviews, negotiations, or any professional interaction.

## Features

- Practice conversations with AI-powered customer personas
- Create custom customer profiles through guided conversation
- Real-time response evaluation from the customer's perspective
- Detailed meeting reports with scoring across multiple criteria
- Automatic saving of conversations and evaluations
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
- `core/` - Core application components
  - `config.py` - Configuration and environment settings
  - `strings.py` - Application string constants

## Creating Custom Profiles

You can create new customer profiles in two ways:

1. Using the UI (Recommended):
   - Click "Create customer profile" in the sidebar
   - Engage in a guided conversation about your customer
   - The AI will ask relevant questions to build a complete profile
   - Save the profile when complete

2. Manually:
   Add new profiles in the `customers` directory as `.txt` files with:
   - Background information
   - Communication style
   - Key concerns
   - Decision-making factors
   - Personality traits
   - Success metrics
   - Red flags

## Setup

1. Install requirements: `pip install -r requirements.txt`
2. Create `.env` file with your Anthropic API key in the format:
   ```
   ANTHROPIC_API_KEY=your_key_here
   ```
3. Run: `streamlit run chat.py`