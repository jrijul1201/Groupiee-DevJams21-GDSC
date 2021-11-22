# Groupiee-DevJams21-GDSC
### Link for website
https://groupiee-mrow.herokuapp.com/ <br>
Note: Some parts of the website are running on test apis(namely the chat API)

# About Groupiee

Indeed, while traveling is something we all love to daydream about and even plan for weeks or even months in the making, the nitty-gritty parts of travel leave not much to be desired. If it were up to us, we would skip all the miserable and troublesome parts of travel altogether after all, who would want to go through all the hassle if you can skip right to the good part, right?

The solution, we present is a platform that matches you with people of the same interests and location and helps you plan an entire trip with them. We present ‘Groupiee’, we aim to make travel hassle-free and fun, here at Groupiee we use your location and help you find a social travel buddy that travels with you, shares the expense, plan your itinerary vibes with you, and makes your trip easier and help you connect with other user and form a feeling of community by our Direct Messaging feature.

# Features 
1.Find a travel buddy that will be based on your location.


2.Book Itenaries -Your one-stop solution


3.Create a community with fellow travelers with the Direct Message feature.

# How to set up
Clone the repository
```
git clone git@github.com:shunphoenix55/Groupiee-DevJams21-GDSC.git
```

Set up a virtual environment (if desired)
```
# Navigate to the directory
cd Groupiee-DevJams21-GDSC
# Create the virtual environment
python3 -m venv groupiee-venv
# Activate the virtual environment
source groupiee-venv/bin/activate
```
(Note: virtual environment setup may be different for non-Linux based systems)

# Install dependencies
## Python
```
python3 -m pip install -r requirements.txt
```
### How to run
Run the app.py file either from your preferred IDE or using
```
python3 ./app.py
```
### Frontend
- [Materializecss](https://materializecss.com/)

### APIs
- [TalkJS chat API](https://talkjs.com/)
- [nominatim geocoding api](https://nominatim.org/release-docs/latest/api/Search/)
- [Leaflet.js map renderer](https://leafletjs.com/)
- rapid api for listing the flights

# Admin Controls

## Verifying users
`/admin_verify_users`
This will bring up a list of users and their verification details
## Adding destinations manually
`/add_destination`
This will let you add destinations manually with a display picture
