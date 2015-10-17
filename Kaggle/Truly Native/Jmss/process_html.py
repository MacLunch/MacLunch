# real output file
#in_file_dir = 'data/html/train/'
#out_file_dir = 'data/json/'

# 임시 output file
in_file_dir = 'data(test)/html/'
out_file_dir = 'data(test)/json/'

from bs4 import BeautifulSoup as bs
import os, sys, logging, string, glob
import cssutils as cu
import json

ferr = open("errors_in_scraping.log","w")

def parse_page(in_file, urlid):
    """ parameters:
            - in_file: file to read raw_data from
            - url_id: id of each page from file_name """
    page = open(in_file, 'r')
    soup = bs(page)
    total_headings, headings = parse_heading(soup, [1,2,3,4,5,6])
    doc = {
            "id": urlid,
            "text":parse_text(soup),
            "title":parse_title(soup),
            "links":parse_links(soup),
            "images":parse_images(soup),
            "headings":total_headings,
            "h1":headings[0],
            "h2":headings[1],
            "h3":headings[2],
            "h4":headings[3],
            "h5":headings[4],
            "h6":headings[5],
            "script_src":parse_script(soup)
           }

    return doc

def parse_text(soup):
    """ parameters:
            - soup: beautifulSoup4 parsed html page
        out:
            - textdata: a list of parsed text output by looping over html paragraph tags
        note:
            - could soup.get_text() instead but the output is more noisy """
    textdata = []

    for text in soup.find_all('p'):
        try:
            textdata.append(text.text.encode('ascii','ignore').strip())
        except Exception:
            continue

    return textdata


def parse_heading(soup, levels):
    hdata = []
    hlevel_data = [[],[],[],[],[],[]]
    
    for level in levels:
        for heading in soup.find_all('h' + str(level)):
            try:
                hdata.append(heading.text.encode('ascii', 'ignore').strip())
                hlevel_data[level-1].append(heading.text.encode('ascii', 'ignore').strip())
            except Exception:
                continue
    

#    temp = []
#    for level in levels:
#        temp.append(filter(None, hlevel_data[level-1]))
            
    return hdata, hlevel_data

def parse_script(soup):
    script_data = []
    
    for script in soup.find_all('script'):
        try:
            if 'javascript' in script.get('type'):
                script_data.append(script.get('src').encode('ascii', 'ignore'))
        except Exception:
            continue
    
    return script_data



def parse_title(soup):
    """ parameters:
            - soup: beautifulSoup4 parsed html page
        out:
            - title: parsed title """

    title = []

    try:
        title.append(soup.title.string.encode('ascii','ignore').strip())
    except Exception:
        return title

    return title

def parse_links(soup):
    """ parameters:
            - soup: beautifulSoup4 parsed html page
        out:
            - linkdata: a list of parsed links by looping over html link tags
        note:
            - some bad links in here, this could use more processing """

    linkdata = []

    for link in soup.find_all('a'):
        try:
            linkdata.append(str(link.get('href').encode('ascii','ignore')))
        except Exception:
            continue

    return linkdata


def parse_images(soup):
    """ parameters:
            - soup: beautifulSoup4 parsed html page
        out:
            - imagesdata: a list of parsed image names by looping over html img tags """
    imagesdata = []

    for image in soup.findAll("img"):
        try:
            imagesdata.append("%(src)s"%image)
        except Exception:
            continue

    return imagesdata

def to_json(python_object):                                             
    if isinstance(python_object, bytes):                                
        return {'__class__': 'bytes',
                '__value__': list(python_object)}                       
    raise TypeError(repr(python_object) + ' is not JSON serializable')

def gogo():
    """ parameters:
                - argv: sys args from the command line that consist of:
                            <label_file> <input_raw_dir> <output_directory>
                * input_raw_dir: directory to read raw input html files
                * output_directory: directory to save processed html files

        note:
                - this will loop over all raw_files and create processed ouput for
                  a give site_id IF input data for that id exists, otherwise it will
                  skip it """

    inFolder = in_file_dir
    outputDirectory = out_file_dir

    print( inFolder, outputDirectory)

    if not os.path.exists(inFolder):
        print (inFolder," does not exist")
        return

    if not os.path.exists(outputDirectory):
        os.makedirs(outputDirectory)

    cu.log.setLevel(logging.CRITICAL)
    json_array = []

    print ('abc')

    fIn = glob.glob( inFolder + '*/*raw*')

    print ('bbb')
    print (fIn)
    
    last_bucket_name = fIn[0].split('/')[-2]
    print ('last_bucket_name : ' + last_bucket_name)
    for idx, filename in enumerate(fIn):
        print (idx, filename)
        if idx % 10000 == 0:
            print ("Processed %d HTML files" % idx)

        filenameDetails = filename.split("/")
        urlId = filenameDetails[-1].split('_')[0]
        bucket_name = filenameDetails[-2]
        print (bucket_name)

        if bucket_name != last_bucket_name or filename==fIn[-1]:            
            print ('SAVING BUCKET %s' % last_bucket_name)
            out_file_name = outputDirectory + 'chunk' + last_bucket_name + '.json'
            out_file = os.path.join(out_file_name)
        
            with open(out_file, mode='w') as feedsjson:
                for entry in json_array:
                    json.dump(entry, feedsjson, default=to_json)
                    feedsjson.write('\n')

            feedsjson.close()
            json_array = []  
            last_bucket_name = bucket_name

        
            
        try:
            doc = parse_page(filename, urlId)
        except Exception as e:
            ferr.write("parse error with reason : "+str(e)+" on page "+urlId+"\n")
            continue

        json_array.append(doc)
        
        

           
    print ("Scraping completed .. There may be errors .. check log at errors_in_scraping.log")

gogo()
