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

    def __eq__(self, other):
        """Nabídky jsou stejné, pokud mají stejný odkaz"""
        if not isinstance(other, RentalOffer):
            return False
        
        return self.link == other.link
