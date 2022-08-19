<h1 align="center"> Realtor </h1>
## Foursquare_capstone_project
Repository created to store a simple recommendation system built with fousquare API data and Python.

## Project objective:
* Given a input containin restaurant of format {'price_level':[1.0],'rating':[4.3],'user_ratings_total':[107],'lat ':[-24.128515],'lon':[-46.689152]}, the algorithim recommends 5 other similar category restaurants.

## How it was developed:
* Data was scrapped from google places api, for São Paulo city in brazil.
Code for data collection can be found on: <br/>
[Data gathering](app/data/main/get_place_data.py)<br/><br/>

* Data was then preprocessed and stored in a mysql db,which is attached to the project.
Code for data collection can be found on: 
<br/>[main jupyter notebook](app/recomendation_system.ipynb)<br/><br/>

* Data was finally segmented using Kmeans, and then used to get the best 5 restaurants ranked by review rate
Code for this step can also be found on:
<br/>[main jupyter notebook](app/recomendation_system.ipynb)<br/><br/>

* Code for a full recommendation can be found on:
<br/>[recmmendation engine](app/make_recommendation.py)<br/><br/>

## How to run this project ?
* You need to have docker and docker compose installed.
* In the project's main folder run:
```
docker-compose up
}
```
all dependencies will be automaticaly installed
* You will also need a google places api token, its free for a number of request.
more detail can be found on::<br/>[google places api]([app/recomendation_system.ipynb](https://cloud.google.com/apis?utm_source=google&utm_medium=cpc&utm_campaign=latam-BR-all-pt-dr-SKWS-all-all-trial-p-dr-1011454-LUAC0015755&utm_content=text-ad-none-any-DEV_c-CRE_534667502763-ADGP_Hybrid%20%7C%20SKWS%20-%20PHR%20%7C%20Txt%20~%20API-Management_General-KWID_43700065166693636-kwd-152051905&utm_term=KW_api-ST_API&gclid=Cj0KCQjwxveXBhDDARIsAI0Q0x08Zr_LkklWwk5FC9niUs1sB59-flhKObMSl4IR4c8x51wC-HfCow0aAgCZEALw_wcB&gclsrc=aw.ds))<br/><br/>
* Then go to:<br/>[main jupyter notebook](app/recomendation_system.ipynb)<br/><br/>

