import string, random

def create_shortcode():
    """Generate a shortcode."""
    return ''.join(random.choices(string.ascii_letters + string.digits + "_", k=6))

def is_valid_shortcode(input: str):
    """Check if a shortcode is valid."""
    if len(input) != 6:
        return False
    else:
        no_score = input.replace('_', '0')
        return no_score.isalnum()

def correct_url(input: str):
    """Check if a url has a 'http' prefix and add it if this is not the case."""
    if not input[:4] == 'http':
        return 'https://' + input
    else:
        return input