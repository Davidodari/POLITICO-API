# List DT will hold list of parties and offices represented as dicts
parties = []
offices = []


class PartiesModel:
    def __init__(self, party=None, party_id=None):
        # Initialise DT inside model
        self.parties = parties
        self.party = party
        self.party_id = party_id

    def create_political_party(self):
        """A function that facilitates creation of a political party and appending to a data structure
           @:return the created party name with success message
        """
        # Extract data from party dict
        created_party = {
            # Id increments on length of list
            "id": len(parties) + 1,
            "name": self.party['name'],
            "hqAddress": self.party['hqAddress'],
            "logoUrl": self.party['logoUrl']
        }
        # Added to list
        parties.append(created_party)
        # Return assigned id response when party successfully created
        return created_party['id']

    def get_all_political_parties(self):
        # Get List Of Parties
        return self.parties

    def get_specific_political_party(self, party_id):
        # Get party by passed in id and return party otherwise default to message response
        if party_id is not None:
            for party in parties:
                if party['id'] == party_id:
                    return party['name']
        return 'Doesnt Exist In Model'


class OfficesModel:
    def __init__(self, office=None):
        self.offices = offices
        self.office = office

    def create_government_office(self):
        """A function that facilitates creation of a government office and appending to a data structure
           @:return the created office id with success message
        """
        # Extract data from party dict
        # Created Office as dict
        created_office = {
            # Id increments on length of list
            "id": len(parties) + 1,
            "type": self.office['type'],
            "name": self.office['name'],

        }
        # Added to list
        offices.append(created_office)
        # Return assigned id response when office successfully created
        return created_office['id']

    def get_all_government_offices(self):
        return self.offices
