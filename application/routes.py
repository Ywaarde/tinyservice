from .url import Shorten, ReturnURL, ReturnStats

def initialize_routes(api):
    """Add endpoints"""
    api.add_resource(Shorten, "/shorten")
    api.add_resource(ReturnURL, "/<shortcode>")
    api.add_resource(ReturnStats, "/<shortcode>/stats")