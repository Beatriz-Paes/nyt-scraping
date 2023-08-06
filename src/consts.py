def get_section_and_type(key):
    values = {
        # sections
        "Any": "any",
        "Arts": "Arts",
        "Books": "Books",
        "Business": "Business",
        "Fashion": "Fashion",
        "Health": "Health",
        "Magazine": "Magazine",
        "T Magazine": "T Magazine",
        "Movies": "Movies",
        "New York": "New York",
        "Opinion": "Opinion",
        "Science": "Science",
        "Real Estate": "Real Estate",
        "Sports": "Sports",
        "Style": "Style",
        "Travel": "Travel",
        "U.S.": "U.S.",
        "World": "World",
        # notice type
        "Article": "article",
        "Audio": "audio",
        "Image Slideshow": "imageslideshow",
        "Recipe": "recipe",
        "Interactive Graphics": "interactivegraphics",
        "Video": "video",
        "Wirecutterarticle": "wirecutterarticle",
    }
    return values.get(key)
