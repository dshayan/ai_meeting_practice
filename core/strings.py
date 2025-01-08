# Main Chat Page Strings
TITLE_WITH_CUSTOMER = "Meeting with {}"
TITLE_DEFAULT = "Meet your customer"
CHAT_INPUT_PLACEHOLDER = "Make your pitch ..."
FREEZE_COMMAND = "freeze and report"

# Sidebar Strings
SIDEBAR_HEADER = "Pitch Perfect"
SIDEBAR_SUBHEADER = "AI Conversation Practice"
NEW_MEETING_BUTTON = "Meet Customers →"
PREVIOUS_MEETINGS_HEADER = "Previous meetings"
NO_SAVED_MEETINGS = "No saved meetings yet."
SELECT_CUSTOMER_PROMPT = "Select a customer"
START_MEETING_BUTTON = "Start Meeting"

# Create Profile Page Strings
CREATE_PROFILE_TITLE = "Create customer profile"
PROFILE_DESCRIPTION_PLACEHOLDER = "Describe your customer ..."
SAVE_PROFILE_HEADER = "Save profile"
PROFILE_NAME_LABEL = "Profile name"
SAVE_PROFILE_BUTTON = "Save profile"

# View Profiles Page Strings
VIEW_PROFILES_TITLE = "Profiles"
NO_PROFILES_FOUND = "No customer profiles found."
VIEW_PROFILE_BUTTON_TEXT = "View"
VIEW_PROFILE_COLUMN_HEADER = "Action"
PROFILE_TABLE_HEADERS = {
    "name": "Name",
    "role": "Role",
    "last_modified": "Last Modified"
}
CREATE_NEW_PROFILE_BUTTON = "Create New Profile"
PROFILE_EXPANDER_TITLE = "Profile: {}"
EDIT_PROFILE_LABEL = "Edit Profile"
PROFILE_SAVE_SUCCESS_MESSAGE = "Profile saved successfully!"

# View Reports Page Strings
VIEW_REPORTS_TITLE = "Reports"
NO_REPORTS_FOUND = "No meeting reports found."
MEETINGS_DIR_ERROR = "Meetings directory not found: {}"
REPORT_TABLE_HEADERS = {
    "customer": "Customer",
    "last_modified": "Last Modified",
    "action": "Action"
}
VIEW_REPORT_BUTTON_TEXT = "View"
REPORT_EXPANDER_TITLE = "Report: {}"

# Button Labels
CLOSE_BUTTON = "Close"
EDIT_BUTTON = "Edit"
SAVE_BUTTON = "Save"
CANCEL_BUTTON = "Cancel"

# Error Messages
CUSTOMERS_DIR_ERROR = "Customers directory not found: {}"
PROMPT_FILE_ERROR = "Prompt file not found: {}"
MEETING_FILE_ERROR = "Error reading meeting file: {}"
MEETINGS_LIST_ERROR = "Error listing meetings: {}"
MEETING_LOAD_ERROR = "Meeting file not found: {}"
MEETING_SAVE_ERROR = "Error saving meeting: {}"
EVALUATION_SAVE_ERROR = "Error saving evaluation: {}"
API_CALL_ERROR = "Error in API call: {}"
PROFILE_NAME_REQUIRED = "Please enter a profile name"
NO_COMPLETE_PROFILE = "No complete profile found. Please continue the conversation until a full profile is generated."
PROFILE_CREATION_PROMPT_ERROR = "Customer creation prompt not found: {}"
PROFILE_SAVE_ERROR = "Error saving profile: {}"
PROFILE_SAVE_SUCCESS = "Profile '{}' saved successfully!"
PROFILE_EDIT_ERROR = "Error saving profile: {}"

# File Templates
EVALUATION_HEADER = "--- Meeting Evaluation {} ---\n\n"
EVALUATION_SECTION = "\n--- Evaluation #{} ---\n"
MEETING_FILENAME = "meeting_with_{}_{}{}"
EVALUATION_FILENAME = "response_evaluation_{}_{}.txt"
REPORT_FILENAME = "meeting_evaluation_{}_{}{}"