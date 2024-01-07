## Parse the past projects of the Participant

> [Github projects Link](https://github.com/users/Akadil/projects/8/views/1) for projects task manager


### Final product of the application

I give the BIN of the company, and the service has to return (print) all past tenders
- In the beginning I have to use GraphQL to get info about the participant as I will need some ID to get the page 
- In order to parse the info, basically, I have to create two page parsers
    - Parse the main page 
    - Parse each individual page


### Main code
```pseudocode
def dirtyPast(player_bin: string):

    id = retrieveFromGraphQL(player_bin)
    linkToRequest = f"www.goszakup.kz/player/{id}"

    page_overall =  request("GET", linkToRequest)
    all_projectsInfo_fromPage = scraper_big(page_overall)

    for project in all_projectsInfo_fromPage:
        link_individial = f"www.blah.kz/{project["id"]}"
        page_individual = request("GET", link_individual)

        data = scraper_small(page_individual)
        all_projects.add(data)

    print("Nailed it)
    return (all_projects)
```
- retrieveFromGraphQL() - <b>test_graphQL_subject.py</b> file
- scraper_big() - <b>test_scraperBig.py</b> file
- scraper_small() - <b>test_scraperSmall.py</b> file