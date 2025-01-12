# Common CSS styles for all pages
COMMON_TABLE_CSS = """
    <style>
        /* Base table styles */
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 48px;
            vertical-align: middle;
        }
        
        /* Table header styles */
        .table-header {
            min-height: 64px;
            font-weight: bold;
            padding: 8px 0;
        }
        
        /* Table cell styles */
        .table-cell {
            display: flex;
            align-items: center;
            min-height: 48px;
            padding: 8px 0;
            white-space: nowrap;
        }
        
        /* Table button styles */
        .table-button {
            min-width: 64px;
            padding: 4px 8px;
            white-space: nowrap;
        }
    </style>
"""

# Table layout configurations
TABLE_LAYOUTS = {
    'profiles': [3, 5, 2, 2],  # Name, Role, Last Modified, Action
    'strategy': [3, 5, 2],     # Name, Role, Action
    'meet': [3, 5, 2, 2],      # Name, Role, Last Modified, Action
    'history': [4, 4, 2],      # Customer, Date, Action
    'reports': [4, 4, 2]       # Customer, Last Modified, Action
}