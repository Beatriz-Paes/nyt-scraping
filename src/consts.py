def get_section_and_type(key):
    values = {
        # sections
        "ANY": "any",
        "ARTS": "Arts",
        "BOOKS": "Books",
        "BUSINESS": "Business",
        "FASHION": "Fashion",
        "HEALTH": "Health",
        "MAGAZINE": "Magazine",
        "T_MAGAZINE": "T Magazine",
        "MOVIES": "Movies",
        "NEW_YORK": "New York",
        "OPINION": "Opinion",
        "SCIENCE": "Science",
        "REAL_ESTATE": "Real Estate",
        "SPORTS": "Sports",
        "STYLE": "Style",
        "TRAVEL": "Travel",
        "U_S": "U.S.",
        "WORLD": "World",
        # notice type
        "ARTICLE": "article",
        "AUDIO": "audio",
        "IMAGE_SLIDESHOW": "imageslideshow",
        "RECIPE": "recipe",
        "INTERACTIVE_GRAPHICS": "interactivegraphics",
        "VIDEO": "video",
        "WIRECUTTERARTICLE": "wirecutterarticle",
    }
    return values.get(key)
