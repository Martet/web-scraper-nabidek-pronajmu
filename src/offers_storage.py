import json

from scrapers.rental_offer import RentalOffer


class OffersStorage:
    """Úložiště dříve nalezených nabídek"""

    def __init__(self, path: str):
        self.path = path
        """Cesta k uloženým odkazům"""

        self.first_time = False
        """Neproběhl pokus o uložení nabídek (soubor neexistuje)"""

        self._offers: list[RentalOffer] = []
        """Seznam URL odkazů na všechny nalezené nabídky"""

        try:
            with open(self.path) as file:
                self._offers = [RentalOffer.from_json(offer) for offer in json.load(file)]
        except FileNotFoundError:
            self.first_time = True


    def contains(self, offer: RentalOffer) -> bool:
        """Objevila se nabídka již dříve?

        Args:
            offer (RentalOffer): Nabídka

        Returns:
            bool: Jde o starou nabídku
        """
        return offer in self._offers


    def save_offers(self, offers: list[RentalOffer]):
        """Uložit nabídky jako nalezené

        Args:
            offers (list[RentalOffer]): Nalezené nabídky
        """
        self._offers = offers + self._offers
        
        with open(self.path, 'w') as file_object:
            json.dump([offer.to_json() for offer in self._offers], file_object)

        self.first_time = False


    def get_offers(self, limit: int = 25, offset: int = 0) -> list[RentalOffer]:
        """Získat nabídky z úložiště

        Args:
            limit (int): Maximální počet nabídek
            offset (int): Posun od začátku seznamu

        Returns:
            list[RentalOffer]: Nabídky z úložiště
        """
        return list(self._offers)[offset:offset + limit]
