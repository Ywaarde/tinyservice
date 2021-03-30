from application import db

from datetime import datetime

class UrlModel(db.Model):
    """Create url object, stats are set to default"""
    __tablename__ = 'tiny-service-url-objects'
    shortcode = db.Column(db.String(6), primary_key=True)
    url = db.Column(db.String(100), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    lastRedirect = db.Column(db.DateTime, nullable=False, default=datetime.now)
    redirectCount = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Url: {self.url}, shortcode: {self.shortcode}"