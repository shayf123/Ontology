import requests
import lxml.html
import rdflib

problems = ['Directed by', '\n', 'Produced by', '[a]', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]',
                '[9]', ' (p.g.a.)', 'Executive Producer', ': ', ' ', ', ', '', 'Running time', 'Starring']

def get_producers(doc):
    producers = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Produced by')]//@title"):
        producers.append(t)

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Produced by')]//text()"):
         t = t.strip()
         if t not in problems:
             skip = False
             for producer in producers:
                 if t in producer:
                     skip = True
                     break
             if(not skip):
                producers.append(t)

    producers.sort()
    return producers

def get_directors(doc):
    directors = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Directed by')]//@title"):
        directors.append(t)

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Directed by')]//text()"):
        t = t.strip()
        if t not in problems:
            skip = False
            for director in directors:
                if t in director:
                    skip = True
                    break
            if not skip:
                directors.append(t)

    directors.sort()
    return directors

def get_running_time(doc):
    runningtime = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Running time')]//text()"):
        if t not in problems:
            runningtime.append(t.strip())

    return runningtime

def get_starring(doc):
    starring = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Starring')]//@title"):
        starring.append(t)

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Starring')]//text()"):
        t = t.strip()
        if t not in problems:
            skip = False
            for star in starring:
                if t in star:
                    skip = True
                    break
            if not skip:
                starring.append(t)

    starring.sort()
    return starring

def get_release_date(doc):
    release_dates = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Release date')]//span[@class = 'bday dtstart published updated']//text()"):
        release_dates.append(t)

    #TODO: CHECK IF TO SORT, CHECK MORE EXAMPLES OF MISSING DATES
    return release_dates

def get_based_on(doc):
    based_on = []

    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Based on')]"):
        based_on.append("Yes")
        return based_on

    based_on.append("No")
    return based_on




def create():
    start_link = "http://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

    ontology = rdflib.Graph()

    r = requests.get(start_link)
    doc = lxml.html.fromstring(r.content)

    for t in doc.xpath("//table[@class = 'wikitable sortable']//tr[position() > 1 and td[position()=2]//text() > 2009]//td[position() = 1]//a"):
        film_link = "http://en.wikipedia.org" + t.xpath('.//@href')[0]

        film_name = t.xpath('.//@title')[0]

        r = requests.get(film_link)
        doc = lxml.html.fromstring(r.content)

        film_entity = rdflib.URIRef("http://example.org/" + film_name.replace(' ', '_'))

        producers = get_producers(doc)
        producer_relation = rdflib.URIRef("http://example.org/produced_by")
        for producer in producers:
            producer_entity = rdflib.URIRef("http://example.org/" + producer.replace(' ', '_'))
            ontology.add((film_entity, producer_relation, producer_entity))

        directors = get_directors(doc)
        director_relation = rdflib.URIRef("http://example.org/directed_by")
        for director in directors:
            director_entity = rdflib.URIRef("http://example.org/" + director.replace(' ', '_'))
            ontology.add((film_entity, director_relation, director_entity))

        running_time = get_running_time(doc)
        running_time_relation = rdflib.URIRef("http://example.org/running_time")
        for rt in running_time:
            rt_entity = rdflib.URIRef("http://example.org/" + rt.replace(' ', '_'))
            ontology.add((film_entity, running_time_relation, rt_entity))

        stars = get_starring(doc)
        starring_relation = rdflib.URIRef("http://example.org/starring")
        for star in stars:
            star_entity = rdflib.URIRef("http://example.org/" + star.replace(' ', '_'))
            ontology.add((film_entity, starring_relation, star_entity))

        release_dates = get_release_date(doc)
        release_dates_relation = rdflib.URIRef("http://example.org/release_dates")
        for release_date in release_dates:
            release_date_entity = rdflib.URIRef("http://example.org/" + release_date.replace(' ', '_'))
            ontology.add((film_entity, release_dates_relation, release_date_entity))

        based_on = get_based_on(doc)
        based_on_relation = rdflib.URIRef("http://example.org/based_on")
        for based_on_elem in based_on:
            based_on_entity = rdflib.URIRef("http://example.org/" + based_on_elem.replace(' ', '_'))
            ontology.add((film_entity, based_on_relation, based_on_entity))


    ontology.serialize("ontology.nt", format="nt")


create()
