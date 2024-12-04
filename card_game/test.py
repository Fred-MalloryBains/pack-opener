from app import app, db , models
from app.models import Cards 


with app.app_context():
    cards = Cards(
        artist_name = 'fred',
        
        popularity = 30,
        image_url = 'hgaeiieohq3ihiqg',
        genre = "jazz",
        uri = "gjfhiahgiap",
    )

    db.session.add(cards)
    db.session.commit()