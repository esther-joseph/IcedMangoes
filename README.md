# IcedMangoes
This is a creative storefront template to help starting artists who are new to starting a small business to help streamline their product and content in a more organized fashion using Python, Django, and MongoDB

Install using `pip install django djongo pillow` and the configuration is as follows here:

`
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'artist_store_db',
    }
}
`

SOLID principles are included in this project where:
- Single Responsibility: services.py handles logic; views render.
- Open/Closed: Can extend ArtworkService without changing core.
- Liskov Substitution: Could swap ArtworkService with subclass.
- Interface Segregation: (If we had interfaces, we’d split service logic.)
- Dependency Inversion: (Can inject service into views for better decoupling.)
