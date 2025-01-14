COMMON_TABLE_CSS = """
    <style>
        /* Base table styles */
        .stMarkdown p {
            margin-bottom: 0;
            line-height: 48px;
            vertical-align: middle;
            width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        /* Table header styles */
        .table-header {
            min-height: 48px;
            font-weight: bold;
            padding: 8px 0;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            width: 100%;
        }
        
        /* Table cell styles */
        .table-cell {
            display: block;  /* Changed from flex to block */
            min-height: 48px;
            padding: 8px 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
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
    'projects': [3, 5, 2, 2],  # Name, Objective, Last Modified, Action
    'strategy': [3, 5, 2],     # Name, Role, Action
    'meet': [3, 5, 2, 2],      # Name, Role, Last Modified, Action
    'history': [4, 4, 2],      # Customer, Date, Action
    'reports': [4, 4, 2],      # Customer, Last Modified, Action
    'settings': [4, 4, 2]      # Name, Last Modified, Action
}