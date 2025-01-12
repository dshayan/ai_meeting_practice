# Common CSS styles for all pages
COMMON_TABLE_CSS = """
    <style>
        /* Base table styles */
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 38px;
            vertical-align: middle;
        }
        
        /* Table header styles */
        .table-header {
            font-weight: bold;
            padding: 8px 0;
        }
        
        /* Table cell styles */
        .table-cell {
            display: flex;
            align-items: center;
            min-height: 38px;
            padding: 8px 0;
            white-space: nowrap;
        }
        
        /* Table row hover effect */
        .table-row:hover {
            background-color: #f8f9fa;
        }
        
        /* Table button styles */
        .table-button {
            width: 100%;
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