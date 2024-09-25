# Amadeus Hotel Booking

![](screenshots/amadeus-hotel-booking-django-2.png)
![](screenshots/amadeus-hotel-booking-django.png)

With the Hotel Booking API you are able to integrate booking capabilities directly in your application. In this prototype we demonstrate the end-to-end booking process with the following flow: 

- Find all available hotels in a given city or location using [Hotel List API](https://developers.amadeus.com/self-service/category/hotel/api-doc/hotel-search/api-reference)
- Find the available prices with room details, descriptions and more using [Hotel Search API](https://developers.amadeus.com/self-service/category/hotel/api-doc/hotel-search/api-reference)
- Complete the booking using the [Hotel Booking](https://developers.amadeus.com/self-service/category/hotel/api-doc/hotel-booking/api-reference)

You also check out the [demo](https://hotel-booking-engine.azurewebsites.net/) as well.

## How to run the project via Docker (recommended)

First you need to add your environment variales in an `.env` file, such as 

```sh
AMADEUS_CLIENT_ID=YOUR_API_KEY
AMADEUS_CLIENT_SECRET=YOUR_API_SECRET
```

Build the image from the Dockerfile. The following command will 

```sh
docker build -t hotel-booking .
```

Then start the app
```sh
docker run --env-file .env -p 8000:8000 hotel-booking
```


At this point you can open a browser and go to `https://0.0.0.0:8000`.


## How to run the project locally

Clone the repository.

```sh
git clone https://github.com/amadeus4dev/hotel-booking.git
cd hotel-booking
```

Next create a virtual environment and install the dependencies.

```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

For authentication add your API key/secret to your environmental variables.

```sh
export AMADEUS_CLIENT_ID=YOUR_API_KEY
export AMADEUS_CLIENT_SECRET=YOUR_API_SECRET
```

You can easily switch between `test` and `production` environments by setting:

```
export AMADEUS_HOSTNAME="test" # an empty value will also set the environment to test
```

or

```
export AMADEUS_HOSTNAME="production"
```

> Each environment has different API keys. Do not forget to update them!

Finally, run the Django server.

```sh
python amadeus_demo_api/manage.py runserver
```

Finally, open a browser and go to `https://127.0.0.1:8000`

## License

This library is released under the [MIT License](LICENSE).

## Help

You can find us on [StackOverflow](https://stackoverflow.com/questions/tagged/amadeus) or join our developer community on
[Discord](https://discord.gg/cVrFBqx).
