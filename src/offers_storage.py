import datetime as dt
import csv
import time

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
                for offer in csv.reader(file):
                    try:
                        timestamp = dt.datetime.fromisoformat(offer[-1])
                    except:
                        timestamp = dt.datetime.min
                    if len(offer) < 5:
                        continue
                    self._offers.append(RentalOffer(
                        link=offer[0],
                        title=offer[1],
                        location=offer[2],
                        price=offer[3],
                        image_url=offer[4],
                        timestamp=timestamp
                    ))
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
        self._offers.extend(offers)
        
        with open(self.path, 'a', newline='') as file_object:
            writer = csv.writer(file_object)
            for offer in offers:
                fields = list(offer.__dict__.values())[:-1]
                fields[-1] = offer.timestamp.isoformat()
                writer.writerow(fields)

        self.first_time = False


    def get_offers(self, limit: int = 25, offset: int = 0) -> list[RentalOffer]:
        """Získat nabídky z úložiště

        Args:
            limit (int): Maximální počet nabídek
            offset (int): Posun od začátku seznamu

        Returns:
            list[RentalOffer]: Nabídky z úložiště
        """
        return self._offers[::-1][offset:offset + limit]


    def get_index(self, offer_link: str) -> int | None:
        """Získat index nabídky v úložišti podle odkazu

        Args:
            offer_link (str): Odkaz na nabídku

        Returns:
            int | None: Index nabídky v úložišti, nebo None pokud se nenachází
        """
        for i, offer in enumerate(self._offers[::-1]):
            if offer.link == offer_link:
                return i
        
        return None
