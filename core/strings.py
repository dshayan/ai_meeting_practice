# Application Title
SIDEBAR_HEADER = "Pitch Perfect"
SIDEBAR_SUBHEADER = "AI conversation practice"

# Home Page Strings
HOME_PAGE_WELCOME = """
An AI-powered platform for realistic conversation practice, powered by Claude 3.5 Sonnet. Perfect for sales professionals, negotiators, and anyone looking to improve their communication skills.

Choose an option from the sidebar to begin:

* **🔥 Projects**: Create and manage project specifications through guided conversation
* **👀 Profiles**: Create and manage detailed customer personas
* **🎯 Strategy**: Generate data-driven meeting strategies based on customer profiles
* **💬 Meet**: Practice conversations with AI personas and receive real-time feedback
* **📅 History**: Review past conversations and track your progress
* **📊 Reports**: Analyze detailed meeting evaluations and performance metrics
* **⚙️ Settings**: View and edit system prompts that control AI behavior
"""

# Project page
VIEW_PROJECTS_TITLE = "View projects"
CREATE_PROJECT_TITLE = "Create new project"
PROJECT_DESCRIPTION_PLACEHOLDER = "Tell me about your project..."
PROJECT_TABLE_HEADERS = {
    "name": "Project name",
    "objective": "Primary objective",
    "last_modified": "Last modified",
    "action": "Action"
}
PROJECT_CREATION_PROMPT_ERROR = "Error reading project creation prompt from {}"
PROJECT_SAVE_ERROR = "Error saving project: {}"
PROJECTS_DIR_ERROR = "Projects directory not found: {}"
NO_PROJECTS_FOUND = "No projects found. Create your first project!"
CREATE_NEW_PROJECT_BUTTON = "Create new project"
SAVE_PROJECT_HEADER = "Save project"
PROJECT_NAME_LABEL = "Project name"
SAVE_PROJECT_BUTTON = "Save project"
PROJECT_NAME_REQUIRED = "Please enter a project name"
NO_COMPLETE_PROJECT = "No complete project specification found"
PROJECT_SAVE_SUCCESS = "Project '{}' saved successfully!"
PROJECT_EXPANDER_TITLE = "Project: {}"

# Project page - edit/view strings
EDIT_PROJECT_LABEL = "Edit project"
PROJECT_SAVE_SUCCESS_MESSAGE = "Project saved successfully!"
PROJECT_EDIT_ERROR = "Error saving project: {}"
VIEW_PROJECT_BUTTON_TEXT = "View"

# Create Profile Page
CREATE_PROFILE_TITLE = "Create customer profile"
PROFILE_DESCRIPTION_PLACEHOLDER = "Describe your customer..."
SAVE_PROFILE_HEADER = "Save profile"
PROFILE_NAME_LABEL = "Profile name"
SAVE_PROFILE_BUTTON = "Save profile"
PROFILE_CREATION_PROMPT_ERROR = "Customer creation prompt not found: {}"
PROFILE_SAVE_ERROR = "Error saving profile: {}"
PROFILE_SAVE_SUCCESS = "Profile '{}' saved successfully!"
PROFILE_NAME_REQUIRED = "Please enter a profile name"
NO_COMPLETE_PROFILE = "No complete profile found. Please continue the conversation until a full profile is generated"
CANCEL_CREATION_BUTTON = "Cancel creation"

# View Profiles Page
VIEW_PROFILES_TITLE = "Customer profiles"
NO_PROFILES_FOUND = "No customer profiles found"
VIEW_PROFILE_BUTTON_TEXT = "View"
VIEW_PROFILE_COLUMN_HEADER = "Action"
PROFILE_TABLE_HEADERS = {
    "name": "Name",
    "role": "Role",
    "last_modified": "Last modified",
    "action": "Action"
}
CREATE_NEW_PROFILE_BUTTON = "Create new profile"
PROFILE_EXPANDER_TITLE = "Profile: {}"
EDIT_PROFILE_LABEL = "Edit profile"
PROFILE_SAVE_SUCCESS_MESSAGE = "Profile saved successfully!"
PROFILE_EDIT_ERROR = "Error saving profile: {}"

# Strategy Page
STRATEGY_PAGE_TITLE = "Meeting strategy"
NO_STRATEGIES_FOUND = "No customer profiles found"
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

# Meet Page
TITLE_WITH_CUSTOMER = "Meeting with {}"
TITLE_DEFAULT = "Meet your customer"
CHAT_INPUT_PLACEHOLDER = "Make your pitch..."
FREEZE_COMMAND = "freeze and report"
CHAT_INITIAL_VENDOR_PITCH = "Initial vendor pitch:\n\n"
CHAT_CUSTOMER_PREVIOUS_MESSAGE = "Customer's previous message: {}\n\n"
CHAT_VENDOR_RESPONSE = "Vendor's response: {}"
CHAT_CUSTOMER_CONTEXT = "Customer Context:\n{}\n\nVendor Messages to Evaluate:"
CHAT_REPORT_SAVED = "\nReport saved to: {}"
CHAT_MEETING_SAVED = "Meeting saved to: {}"
CHAT_EVALUATIONS_SAVED = "Evaluations saved to: {}"
NEW_MEETING_BUTTON = "Meet customers"

# History Page
VIEW_HISTORY_TITLE = "Meeting history"
NO_MEETINGS_FOUND = "No previous meetings found"
MEETING_TABLE_HEADERS = {
    "customer": "Customer",
    "date": "Date",
    "action": "Action"
}
MEETING_EXPANDER_TITLE = "Meeting with {}"

# Reports Page
VIEW_REPORTS_TITLE = "Meeting reports"
NO_REPORTS_FOUND = "No meeting reports found"
REPORT_TABLE_HEADERS = {
    "customer": "Customer",
    "last_modified": "Last modified",
    "action": "Action"
}
VIEW_REPORT_BUTTON_TEXT = "View"
REPORT_EXPANDER_TITLE = "Report: {}"

# Settings Page
SETTINGS_PAGE_TITLE = "System prompts settings"
NO_PROMPTS_FOUND = "No prompts found in the prompts directory"
PROMPTS_DIR_ERROR = "Prompts directory not found: {}"
PROMPTS_TABLE_HEADERS = {
    "name": "Name",
    "last_modified": "Last modified",
    "action": "Action"
}
VIEW_PROMPT_BUTTON = "View"
PROMPT_EXPANDER_TITLE = "Prompt: {}"
EDIT_PROMPT_LABEL = "Edit prompt"
PROMPT_SAVE_SUCCESS = "Prompt saved successfully!"
PROMPT_SAVE_ERROR = "Error saving prompt: {}"

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