# glcardgame
Two Player Card Game

##### Steps start the application 
After cloning the repository : 

   There are a couple of things you need to set up before you can start your application.
   1. Create docker volume for our application's db for local environment
   
        `docker volume create --name=cgpgdata`
   2. Build and Run
   
        `docker-compose up --build`
           
##### ENVs are not supposed to be pushed
 - I have pushed local envs just for reference
 

#### Architecture of Application

Dockerized Application

  Services - django(backend) and postgres(database)
  
  Rest APIs built using
  
    Django Rest framework
  Database
  
    Postgres
 - Database Structure - db_structure.png
 
 
 The main game playing APIs are:
 1. "http://localhost:8000/games/"
    
    Body : 
    
    `{
	"username1": "testplayer3",
	"username2": "testplayer4"
    }`
    
 
   Success Response:
    
     `{
    "id": 2,
    "status": "NR",
    "date_created": "2020-02-05T02:26:55.294316Z",
    "date_modified": "2020-02-05T02:26:55.294338Z",
    "player1": 4,
    "player2": 5,
    "next_move_by": 4,
    "won_by": null
    }`
    
    
 2. "http://localhost:8000/draw_card/"
 
    Body:
    
    `{
	"player":4,
	"game":2
    }`
    
    
   Success Response:
   
    `{
    "id": 85,
    "sequence_player1": [
        [
            "8",
            "DIAMOND"
        ],
        [
            "5",
            "DIAMOND"
        ],
        [
            "3",
            "CLUB"
        ],
        [
            "8",
            "CLUB"
        ],
        [
            "9",
            "CLUB"
        ]
    ],
    "sequence_player2": [
        [
            "12",
            "HEART"
        ],
        [
            "6",
            "CLUB"
        ],
        [
            "4",
            "SPADE"
        ],
        [
            "7",
            "HEART"
        ],
        [
            "7",
            "CLUB"
        ]
    ],
    "card_rank": "8",
    "card_suit": "DIAMOND",
    "game_status": "NR",
    "date_created": "2020-02-05T03:23:44.225484Z",
    "date_modified": "2020-02-05T03:23:44.225519Z",
    "player": 4,
    "game": 2,
    "card": 135
}`
    