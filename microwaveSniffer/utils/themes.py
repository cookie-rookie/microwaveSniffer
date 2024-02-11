# themes.py

light_theme = {
    "main_background": "background-color: #FFFFFF;",
    "button_style": """
        QPushButton {
            background-color: #E0E0E0;
            color: black;
        }
        QPushButton:hover {
            background-color: #CCCCCC;
        }
    """,
    "label_style": "color: black;",
    # Define other widget styles for light theme
}

dark_theme = {
    "main_background": "background-color: #333333;",
    "button_style": """
        QPushButton {
            background-color: #555555;
            color: white;
        }
        QPushButton:hover {
            background-color: #777777;
        }
    """,
    "label_style": "color: white;",
    # Define other widget styles for dark theme
}
