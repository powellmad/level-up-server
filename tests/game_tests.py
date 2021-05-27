import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType
from levelupapi.models.game import Game


class GameTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        # Initiate request and capture response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Store the auth token
        self.token = json_response["token"]

        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        # response.status_code == status.HTTP_201_CREATED

        # Assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # SEED DATABASE WITH ONE GAME TYPE
        # This is needed because the API does not expose a /gametypes
        # endpoint for creating game types
        gametype = GameType()
        gametype.label = "Board game"
        gametype.save()

        self.game = Game()
        self.game.gametype_id = 1
        self.game.title = "Monopoly"
        self.game.instructions = ""
        self.game.max_players = 6
        self.game.gamer = 1
        
        self.game.save()


    def test_create_game(self):
        """
        Ensure we can create a new game.
        """
        # DEFINE GAME PROPERTIES
        url = "/games"
        data = {
            "gameTypeId": 1,
            "title": "Clue",
            "maxPlayers": 6,
            "instructions": ""
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["title"], "Clue")
        self.assertEqual(json_response["instructions"], "")
        self.assertEqual(json_response["max_players"], 6)

    def test_get_game(self):

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/games/{self.game.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["title"], "Monopoly")
        self.assertEqual(json_response["instructions"], "")
        self.assertEqual(json_response["max_players"], 6)

    def test_change_game(self):

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameTypeId": 1,
            "title": "Sorry",
            "maxPlayers": 4,
            "instructions": ""
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/games/{self.game.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/games/{self.game.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["title"], "Sorry")
        self.assertEqual(json_response["max_players"], 4)

    def test_delete_game(self):
        """
        Ensure we can delete an existing game.
        """

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/games/{self.game.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/games/{self.game.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)