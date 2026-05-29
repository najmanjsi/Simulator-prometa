### SLIM - Simulacija Ljubljanske nepremičnosti (angl. Simulation of Ljubljana's IMmobility)

<br>

<!-- 
> <br>
>
> #### Uvoz podatkov iz OpenStreetMap
>
> Opcije:
> - OSM WebWizard (SUMOv program)
>   - najhitreje in najbolj preprosto - izbereš območje, izbereš vrste cest, vrste vozil, število izbranih vozil in SUMO izdela simulacijo
>   - dobra opcija za izdelavo omrežja (če niso potrebne bolj specifične omejitve), pomanjkljivost je otežena ponavljivost (vedno je potrebno naklikati vse opcije)
>   - za izdelavo simulacije je dokaj neuporabno (morda le za sam začetek, da vidiš, kako simulacija sploh izgleda)
> - **Overpass Turbo (priporočjivo)**
>   - nekoliko počasneje in težje - potrebno se je seznaniti s formatom *query*jev in z oznakami OSM, da lahko pridobiš željene podatke
>   - še boljša opcija za izdelavo omrežja zaradi veliko večjega nadzora nad samo izdelavo - OPTurbo generira XML datoteko, ki jo lahko nato s SUMO orodjem `netconvert` spremeniš v omrežje. `netconvert` ima veliko parametrov, ki lahko olajšajo kasnejše čiščenje omrežja
>   - zelo enostavno ponavljivo, saj le prilepiš želen *query*. Poleg grafičnega vmesnika ima tudi API, torej en preprost Python program zadostuje za izvoz
> - OpenStreetMap Export
>   - ni priporočljivo, saj izvozi vse na označenem območju, kar pomeni, da zaradi omejitev ni možno izvoziti več kot nekaj km$^2$
> - Geofabrik
>   - prav tako izvozi vse v želeni državi/mestu, a nima omejitev glede velikosti
>
> <br>
-->


#### SUMO - Simulacija mestne premičnosti (angl. Simulation of Urban MObility)

- `netconvert`
- `netedit`
- `sumo` in `sumo-gui`
- `TraCI`
- skripte: `randomTrips`, `duarouter`, `routeSampler`, `mapDetectors`

<br>


#### Števci prometa

- niso javno dostopni podatki, hrani jih MOL (Mestna občina Ljubljana)
- več podatkovnih zbirk
    - starejša: 2013-2019, skupaj v eni CSV datoteki, že nekoliko izboljšana
    - novejše: 2019-2025, letne CSV datoteke, še vedno v originalnem formatu
- problemi podatkovnih zbirk
    - nekateri *ID*ji števcev (identifikacijske številke oblike 1xxx-xxx) so se tekom let spremenili
    - nekateri števci so bili premaknjeni, drugi odstranjeni, spet tretji na novo postavljeni
    - nekateri števci imajo večmesečne luknje v podatkih

<br>


#### Uvoz podatkov iz OpenStreetMap

Opcije:
- OSM WebWizard (SUMOv program)
    - najhitreje in najbolj preprosto - izbereš območje, izbereš vrste cest, vrste vozil, število izbranih vozil in SUMO izdela simulacijo
    - dobra opcija za izdelavo omrežja (če niso potrebne bolj specifične omejitve), pomanjkljivost je otežena ponavljivost (vedno je potrebno naklikati vse opcije)
    - za izdelavo simulacije je dokaj neuporabno (morda le za sam začetek, da vidiš, kako simulacija sploh izgleda)
- **Overpass Turbo (priporočjivo)**
    - nekoliko počasneje in težje - potrebno se je seznaniti s formatom *query*jev in z oznakami OSM, da lahko pridobiš željene podatke
    - še boljša opcija za izdelavo omrežja zaradi veliko večjega nadzora nad samo izdelavo - OPTurbo generira XML datoteko, ki jo lahko nato s SUMO orodjem `netconvert` spremeniš v omrežje. `netconvert` ima veliko parametrov, ki lahko olajšajo kasnejše čiščenje omrežja
    - zelo enostavno ponavljivo, saj le prilepiš želen *query*. Poleg grafičnega vmesnika ima tudi API, torej ena preprosta Python skripta zadostuje za izvoz
- OpenStreetMap Export
    - ni priporočljivo, saj izvozi vse na označenem območju, kar pomeni, da zaradi omejitev ni možno izvoziti več kot nekaj km$^2$
- Geofabrik
    - prav tako izvozi vse v želeni državi/mestu, a nima omejitev glede velikosti

<br>


#### Od števcev do simulacije

- datoteke
    - dataseti MOL
        - `minute_full.csv`
        - `minute_full_station_merged.csv`
    - `lokacije_stevcev.txt`
        - koordinate števcev (v datotekah MOL so samo opisne lokacije za odsek ceste) v in opombe
<br>

- Python skripte
    - `bounding_box_counters.py`
        - *input*: pravokotno območje (angl. bounding box) v obliki `(lon1, lon2, lat1, lat2)`
        - *output*: CSV s `counter_id,lat,lon,direction`
    - `location2edge_mapping.py`
        - *input*: CSV s `counter_id,lat,lon,direction`
        - *output*: CSV s `counter_id,edge_id,offset`, kjer je offset pozicija števca na *edge*u
    - `sumo_files_generator.py`
        - glavna datoteka, ki ustvari datoteko `edgecounts.xml`, potrebno za `routeSampler.py`, da ustvari primerne poti
        - lahko ustvari tudi datoteko `inductionloops.add.xml` (**TODO**), ki definira lokacije simuliranih števcev v omrežju
        - *input*: seznam števcev, PKL datoteka s podatki za števce, CSV s `counter_id,edge_id,offset`, datum, začetni in končni čas
        - *ouput*: XML datoteka, primerna za simulacijo, ki ima podatke o številu vozil porazdeljene po 15 minutnih (900s) intervalih
<br>

- **ustvarjanje simulacije**
    - potrebujemo sledeče datoteke
        - `map.osm`
            - vsebuje naj vsaj glavne ceste oz. vsaj tiste, na katerih se nahajajo števci
        - `countercoordinates.csv`
            - vsebuje naj čim bolj natančne koordinate števcev
        - `countingdata.csv`
    - ustvarjanje omrežja
        - `netconvert --osm-files map.osm --no-turnarounds -o network.net.xml`
            - to je najbolj preprosta verzija, obstaja še veliko drugih opcij, ki jih lahko na tej točnki nastavimo
                - `tls`
                - `geometry`
                - ...
    - podatki na števcih $\to$ podatki na povezavah
        - uporabimo `bounding_box_counters.py`, `location2edge_mapping.py` in `sumo_files_generator.py`, da ustvarimo `edgecounts.xml` datoteko za določen interval
    - ustvarjanje poti po omrežju
        - `python randomTrips.py -n network.net.xml --fringe-factor 50 -o trips.xml`
            - `--fringe-factor` določa, koliko "potovanj" (angl. trips, ima le začetek in konec) bo imelo začetek ali konec na robu omrežja
        - `duarouter -n network.net.xml -t trips.xml -o routes_init.rou.xml`
            - `duarouter` iz potovanj zgradi najkrajše (mogoče najhitrejše?) poti (napram potovanjem imajo poti poleg začetka in konca še vse vmesne povezave)
        - `python routeSampler.py -r routes_init.rou.xml --edgedata-files edgecounts.xml -o routes.rou.xml`
            - izmed prej ustvarjenih poti izbere tiste, ki pripomorejo k pretoku, defiranem s podatki števcev

<br>


<!--
```mermaid
---
config:
    theme: redux
    look: handDrawn
    fontFamily: papyrus
---
graph LR
    A{{   \n\n\n  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎    }} --- C{{   \n\n\n  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎    }}
    B{{   \n\n\n  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎    }} --- D{{   \n\n\n  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎    }}
    E{{   \n\n\n  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎    }}
    
```
-->
