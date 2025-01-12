# Home Page Strings
HOME_PAGE_WELCOME = """
An AI-powered platform for realistic conversation practice, ideal for sales, interviews, negotiations, and professional interactions.

Choose an option from the sidebar to begin:

* **➕ Create**: Create a new customer profile through guided conversation
* **👀 Profiles**: View and manage your saved customer profiles
* **🎯 Strategy**: View and create meeting strategies
* **💬 Meet**: Practice conversations with AI-powered customer personas
* **📅 History**: Review your past meetings
* **📊 Reports**: View detailed evaluations and feedback from your meetings
"""

# Sidebar Strings
SIDEBAR_HEADER = "Pitch Perfect"
SIDEBAR_SUBHEADER = "AI Conversation Practice"
NEW_MEETING_BUTTON = "Meet Customers"
PREVIOUS_MEETINGS_HEADER = "Previous meetings"
NO_SAVED_MEETINGS = "No saved meetings yet."
SELECT_CUSTOMER_PROMPT = "Select a customer"
START_MEETING_BUTTON = "Start Meeting"

# Create Profile Page (➕) Strings
CREATE_PROFILE_TITLE = "Create customer profile"
PROFILE_DESCRIPTION_PLACEHOLDER = "Describe your customer ..."
SAVE_PROFILE_HEADER = "Save profile"
PROFILE_NAME_LABEL = "Profile name"
SAVE_PROFILE_BUTTON = "Save profile"
PROFILE_CREATION_PROMPT_ERROR = "Customer creation prompt not found: {}"
PROFILE_SAVE_ERROR = "Error saving profile: {}"
PROFILE_SAVE_SUCCESS = "Profile '{}' saved successfully!"
PROFILE_NAME_REQUIRED = "Please enter a profile name"
NO_COMPLETE_PROFILE = "No complete profile found. Please continue the conversation until a full profile is generated."

# View Profiles Page (👀) Strings
VIEW_PROFILES_TITLE = "Customer profiles"
NO_PROFILES_FOUND = "No customer profiles found."
VIEW_PROFILE_BUTTON_TEXT = "View"
VIEW_PROFILE_COLUMN_HEADER = "Action"
PROFILE_TABLE_HEADERS = {
    "name": "Name",
    "role": "Role",
    "last_modified": "Last Modified",
    "action": "Action"
}
CREATE_NEW_PROFILE_BUTTON = "Create New Profile"
PROFILE_EXPANDER_TITLE = "Profile: {}"
EDIT_PROFILE_LABEL = "Edit Profile"
PROFILE_SAVE_SUCCESS_MESSAGE = "Profile saved successfully!"
PROFILE_EDIT_ERROR = "Error saving profile: {}"

# Strategy Page (🎯) Strings
STRATEGY_PAGE_TITLE = "Meeting strategy"
NO_STRATEGIES_FOUND = "No customer profiles found."
STRATEGY_TABLE_HEADERS = {
    "name": "Name",
    "role": "Role",
    "action": "Action"
}
STRATEGY_VIEW_BUTTON = "View"
STRATEGY_CREATE_BUTTON = "Create"
STRATEGY_EXPANDER_TITLE = "Strategy for {}"
STRATEGY_MEET_BUTTON = "Meet"
STRATEGY_CREATION_SUCCESS = "Strategy created for {}"
STRATEGY_SAVE_ERROR = "Error saving strategy: {}"
STRATEGY_GENERATION_ERROR = "Error generating strategy: {}"
STRATEGY_PROMPT_ERROR = "Strategy generation prompt not found: {}"

# Meet Page (💬) Strings
TITLE_WITH_CUSTOMER = "Meeting with {}"
TITLE_DEFAULT = "Meet your customer"
CHAT_INPUT_PLACEHOLDER = "Make your pitch ..."
FREEZE_COMMAND = "freeze and report"
CHAT_INITIAL_VENDOR_PITCH = "Initial vendor pitch:\n\n"
CHAT_CUSTOMER_PREVIOUS_MESSAGE = "Customer's previous message: {}\n\n"
CHAT_VENDOR_RESPONSE = "Vendor's response: {}"
CHAT_CUSTOMER_CONTEXT = "Customer Context:\n{}\n\nVendor Messages to Evaluate:"
CHAT_REPORT_SAVED = "\nReport saved to: {}"
CHAT_MEETING_SAVED = "Meeting saved to: {}"
CHAT_EVALUATIONS_SAVED = "Evaluations saved to: {}"

# History Page (📅) Strings
VIEW_HISTORY_TITLE = "Meeting history"
NO_MEETINGS_FOUND = "No previous meetings found."
MEETING_TABLE_HEADERS = {
    "customer": "Customer",
    "date": "Date",
    "action": "Action"
}
MEETING_EXPANDER_TITLE = "Meeting with {}"

# Reports Page (📊) Strings
VIEW_REPORTS_TITLE = "Meeting reports"
NO_REPORTS_FOUND = "No meeting reports found."
REPORT_TABLE_HEADERS = {
    "customer": "Customer",
    "last_modified": "Last Modified",
    "action": "Action"
}
VIEW_REPORT_BUTTON_TEXT = "View"
REPORT_EXPANDER_TITLE = "Report: {}"

# Common Button Labels
CLOSE_BUTTON = "Close"
EDIT_BUTTON = "Edit"
SAVE_BUTTON = "Save"
CANCEL_BUTTON = "Cancel"

# File Templates
EVALUATION_HEADER = "--- Meeting Evaluation {} ---\n\n"
EVALUATION_SECTION = "\n--- Evaluation #{} ---\n"
MEETING_FILENAME = "meeting_with_{}_{}{}"
EVALUATION_FILENAME = "response_evaluation_{}_{}.txt"
REPORT_FILENAME = "meeting_evaluation_{}_{}{}"

# Error Messages
CUSTOMERS_DIR_ERROR = "Customers directory not found: {}"
PROMPT_FILE_ERROR = "Prompt file not found: {}"
MEETING_FILE_ERROR = "Error reading meeting file: {}"
MEETINGS_LIST_ERROR = "Error listing meetings: {}"
MEETING_LOAD_ERROR = "Meeting file not found: {}"
MEETING_SAVE_ERROR = "Error saving meeting: {}"
EVALUATION_SAVE_ERROR = "Error saving evaluation: {}"
API_CALL_ERROR = "Error in API call: {}"
MEETINGS_DIR_ERROR = "Meetings directory not found: {}"