import requests
import lxml.html
import rdflib


problems = ['Directed by', '\n', 'Produced by', '[a]', '[1]', '[2]', '[3]', '[4]', '[5]', '[6]', '[7]', '[8]',
                '[9]', ' (p.g.a.)', 'Executive Producer', ': ', ' ', ', ', '', 'Running time', 'Starring']

people_link_problems = ['#cite_note-1', '#cite_note-2', '#cite_note-Elliot-1', '#cite_note-comingsoon-1', '#cite_note-Fletcher-2']

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


def check_octavia_spencer(films_list, films_names, starring_list):
    for i in range(len(films_list)):
        if "The Shape of Water" == films_names[i]:
            stars = starring_list[i]
            for star in stars:
                if "Octavia Spencer" == star:
                    print("Yes")
                    print("---------")
                    print(films_list[i])
                    print(films_names[i])
                    print(starring_list[i])
                    return
    print("No")


def check_meryl_streep(films_list, starring_list):
    count_meryl_strip = 0
    for i in range(len(films_list)):
        stars = starring_list[i]
        for star in stars:
            if "Meryl Streep" == star:
                print(films_list[i])
                count_meryl_strip += 1
    print("Number of films is " + str(count_meryl_strip))


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


def get_people(people_set, doc):
    for t in doc.xpath("//table[@class = 'infobox vevent']//tr[contains(.//text(),'Directed by') or " +
                       "contains(.//text(),'Produced by') or contains(.//text(),'Starring')]//a//@href"):
        if t not in people_link_problems:
            people_set.add("https://en.wikipedia.org" + t)


def get_birthday(doc):
    bd = []
    for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard']//tr[contains(.//text(),'Born')]//span[@class = 'bday']//text()"):
        bd.append(t)

    return bd


def create():
    start_link = "https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films"

    ontology = rdflib.Graph()

    r = requests.get(start_link)
    doc = lxml.html.fromstring(r.content)


    films_entities = []
    films_list = []
    films_names = []
    producers_list = []
    directors_list = []
    running_time_list = []
    starring_list = []
    based_on_list = []
    release_date_list = []
    people_set = set()


    for t in doc.xpath("//table[@class = 'wikitable sortable']//tr[position() > 1 and td[position()=2]//text() > 2009]//td[position() = 1]//a//@href"):
        films_list.append("https://en.wikipedia.org" + t)

    for t in doc.xpath("//table[@class = 'wikitable sortable']//tr[position() > 1 and td[position()=2]//text() > 2009]//td[position() = 1]//a//@title"):
        films_names.append(t)


    for link in films_list:
        r = requests.get(link)
        doc = lxml.html.fromstring(r.content)


        print(link)
        producers_list.append(get_producers(doc))
        print(producers_list[-1])
        #directors_list.append(get_directors(doc))
        #running_time_list.append(get_running_time(doc))
        #starring_list.append(get_starring(doc))
        #release_date_list.append(get_release_date(doc))
        #based_on_list.append(get_based_on(doc))
        #print(based_on_list[-1])
        #get_people(people_set, doc)

    #people_list = list(people_set)
    #bdays = []
    #occupations = []
    # for people_link in people_list:
    #     r = requests.get(people_link)
    #     doc = lxml.html.fromstring(r.content)

        #bdays.append(get_birthday(doc))
        # occupations.append(get_occupation(doc))
        #
        # print(people_link)
        # print(occupations[-1])

    #     occ = []
    #     for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard']//tr[contains(.//text(),'Occupation')]//li//text()"):
    #         if t not in problems:
    #             occ.append(t)
    #
    #
    #     for t in doc.xpath("//table[@class = 'infobox biography vcard' or @class = 'infobox vcard']//tr[contains(.//text(),'Occupation')]//td[@class = 'infobox-data role' or @class='infobox-data']//text()"):
    #         if t not in problems:
    #             occ.append(t)
    #
    #
    #     occupations.append(sorted(list(set(occ))))
    #     #print(occupations[-1])

    # for i in range(len(films_list)):
    #     print(str(i) + " " + films_list[i])
    #     print(directors_list[i])
    #     print(producers_list[i])
    #     print(running_time_list[i])
    #     print(starring_list[i])
    #     print(release_date_list[i])
    #     print("--------------")

    # for i in range(len(people_list)):
    #     print(str(i) + " " + people_list[i])
    #     print(bdays[i])

    # print("------------------------")
    # check_meryl_streep(films_list, starring_list)
    # print("------------------------")
    # check_octavia_spencer(films_list, films_names, starring_list)


create()
