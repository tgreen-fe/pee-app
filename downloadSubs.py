from asyncore import close_all
import requests
import json
from requests.structures import CaseInsensitiveDict
import linecache

def check_if_string_in_file(file_name, string_to_search):
    """ Check if any line in the file contains given string """
    # Open the file in read only mode
    with open(file_name, 'r', encoding="utf-8") as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if string_to_search in line:
                return True
    return False

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r', encoding="utf-8") as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def check_film_length(file_name):
    file = open(file_name, encoding="utf-8")
    content = file.readlines()[-1]
    lineNums = search_string_in_file(file_name, content)

    finalLineNum = lineNums[len(lineNums)-1][0]
    
    for x in range(10):
        if("-->" in linecache.getline(file_name, finalLineNum-x)):
            totalTimeLine = linecache.getline(file_name, finalLineNum-x)
            break
    
    totalTime = totalTimeLine.split(":")
    return(totalTime)

def film_download(filmTitle):
    urlSearch = "https://api.opensubtitles.com/api/v1/subtitles"

    querystring = {"query":str(filmTitle), "languages":"en"}

    headersSearch = {
        'Content-Type': "application/json",
        'Api-Key': "YOUR_OPENSUBTITLES_API_KEY",
        'User-Agent':
        "PeeApp v0.1",
        }

    searchResp = requests.request("GET", urlSearch, headers=headersSearch, params=querystring)
    searchJson = searchResp.json()

    try:
        i = 0
        for i in range(50):
            print("Is this the correct film: ", searchJson['data'][i]['attributes']['feature_details']['movie_name'], "?")
            correctFilm = input("Y/N\n")
            if correctFilm.lower() == "y":
                fileID = searchJson['data'][i]['attributes']['files'][0]['file_id']
                break

    except IndexError:
        print("Your search could not be found. Would you like to retry?")
        retryValue = input("(Y/N)\n")
        if retryValue.lower() == "y":
            fullSearch()
        else:
            raise SystemExit(0)

    
    #print(searchJson['data'][0]['attributes'])
    
    #fileID = searchJson['data'][0]['attributes']['files'][0]['file_id']
    #print(searchJson)
    #print(fileID)

    urlDownload = "https://api.opensubtitles.com/api/v1/download"

    headers = CaseInsensitiveDict()
    headers["Api-Key"] = "YOUR_OPENSUBTITLES_API_KEY"
    headers["Content-Type"] = "application/json"
    headers["User-Agent"] = "PeeApp v0.1"

    data = """{"file_id":""" + str(fileID) + """}"""


    resp = requests.post(urlDownload, headers=headers, data=data)
    respJson = resp.json()
    srtLink = respJson['link']

    r = requests.get(srtLink)

    

    open('subtitles.txt', 'wb').write(r.content.lower())

def search_script(scriptQuoteCaseSense):
    scriptQuote = scriptQuoteCaseSense.lower()
    if check_if_string_in_file("subtitles.txt", scriptQuote):
        matched_lines = search_string_in_file("subtitles.txt", scriptQuote)
        print('Total Matched lines : ', len(matched_lines))

        filmLength = check_film_length('subtitles.txt')

    
        file = open('subtitles.txt', encoding="utf-8")
        content = file.readlines()
        for elem in matched_lines:
            if("-->" in content[elem[0]-2]):
                curTime = str(content[elem[0]-2])
                currentTime = curTime.split(":")
                print('Line Number = ', elem[0], ' : Line = ', elem[1], " : Time = ", content[elem[0]-2], " : Percentage Complete = ", round((((int(currentTime[0])*60)+(int(currentTime[1])))/((int(filmLength[0])*60)+(int(filmLength[1]))))*100, 2), "% : Time Left = ", ((int(filmLength[0])*60)+(int(filmLength[1]))) - ((int(currentTime[0])*60)+(int(currentTime[1]))), " minutes")
            elif("-->" in content[elem[0]-3]):
                curTime = str(content[elem[0]-3])
                currentTime = curTime.split(":")
                print('Line Number = ', elem[0], ' : Line = ', elem[1], " : Time = ", content[elem[0]-3], " : Percentage Complete = ", round((((int(currentTime[0])*60)+(int(currentTime[1])))/((int(filmLength[0])*60)+(int(filmLength[1]))))*100, 2), "% : Time Left = ", ((int(filmLength[0])*60)+(int(filmLength[1]))) - ((int(currentTime[0])*60)+(int(currentTime[1]))), " minutes")
            else:
                curTime = str(content[elem[0]-4])
                currentTime = curTime.split(":")
                print('Line Number = ', elem[0], ' : Line = ', elem[1], " : Time = ", content[elem[0]-4], " : Percentage Complete = ", round((((int(currentTime[0])*60)+(int(currentTime[1])))/((int(filmLength[0])*60)+(int(filmLength[1]))))*100, 2), "% : Time Left = ", ((int(filmLength[0])*60)+(int(filmLength[1]))) - ((int(currentTime[0])*60)+(int(currentTime[1]))), " minutes")
    else:
        print("Please check the dialouge spelling or try a different phrase")
        newInput = input("")
        search_script(newInput)

def fullSearch():
    filmTitle = input("Enter Film or Television Show Title:")
    film_download(filmTitle)
    scriptQuoteCaseSense = input("Enter most recent line of dialogue:")
    search_script(scriptQuoteCaseSense)

fullSearch()

repeatSearch = input("Would you like to search another film or TV Show? Y/N:\n")
if repeatSearch.lower() == "y":
    fullSearch()
