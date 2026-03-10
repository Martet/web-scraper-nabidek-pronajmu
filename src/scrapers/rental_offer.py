from dataclasses import dataclass


@dataclass
class RentalOffer:
    """Nabídka pronájmu bytu"""

    link: str
    """URL adresa na nabídku"""

    title: str
    """Popis nabídky (nejčastěji počet pokojů, výměra)"""

    location: str
    """Lokace bytu (městská část, ulice)"""

    price: int | str
    """Cena pronájmu za měsíc bez poplatků a energií"""

    image_url: str
    """Náhledový obrázek nabídky"""

    scraper: 'ScraperBase'
    """Odkaz na instanci srapera, ze kterého tato nabídka pochází"""

    def to_json(self):
        """Převede nabídku na JSON-serializovatelnou reprezentaci"""
        return {
            "link": self.link,
            "title": self.title,
            "location": self.location,
            "price": self.price,
            "image_url": self.image_url,
        }
    
    @staticmethod
    def from_json(json_dict: dict):
        """Vytvoří nabídku z JSON reprezentace

        Args:
            json_dict (dict): JSON reprezentace nabídky
            scraper (ScraperBase): Scraper, ze kterého nabídka pochází

        Returns:
            RentalOffer: Nabídka vytvořená z JSON reprezentace
        """
        return RentalOffer(
            link=json_dict["link"],
            title=json_dict["title"],
            location=json_dict["location"],
            price=json_dict["price"],
            image_url=json_dict["image_url"],
            scraper=None
        )
