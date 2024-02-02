import json

import requests
from bs4 import BeautifulSoup

article_list = []


def iterate_thru_tags_propriety(response_url, tag, propriety):
    soup = BeautifulSoup(response_url.content, 'html.parser')
    meta_tag = soup.find(tag, property=propriety)
    if meta_tag:
        return meta_tag.get('content')
    else:
        return ""


def iterate_thru_tags_name(response_url, tag, propriety):
    soup = BeautifulSoup(response_url.content, 'html.parser')
    meta_tag = soup.find(tag, attrs={'name': propriety})
    if meta_tag:
        return meta_tag.get('content')
    else:
        return ""


def iterate_thru_tags_type(response_url, tag, propriety):
    soup = BeautifulSoup(response_url.content, 'html.parser')
    script_tag = soup.find(tag, type=propriety)
    if script_tag:
        content = script_tag.string
        try:
            json_ld = json.loads(content)
            return json_ld
        except json.JSONDecodeError:
            print("Error decoding JSON content.")


def crawl_article_bzi(url):
    article_info = {}
    response = requests.get(url)

    article = {}
    nr = 1
    article_info["articleName"] = iterate_thru_tags_propriety(response, "meta", "og:title")
    article_info['articleBody'] = iterate_thru_tags_propriety(response, "meta", "og:description")
    article_info['articleUrl'] = iterate_thru_tags_propriety(response, "meta", "og:url")
    article_info['articleDatePublished'] = \
        iterate_thru_tags_propriety(response, "meta", "article:published_time").split("T")[0]
    article_info['multimedia_content'] = {}
    article_info['multimedia_content'][f"image_{nr}"] = {}

    article_info['multimedia_content'][f"image_{nr}"]["imageUrl"] = iterate_thru_tags_propriety(response, "meta", "og"
                                                                                                                  ":image")
    article_info['multimedia_content'][f"image_{nr}"]["imageId"] = article_info['multimedia_content'][f"image_{nr}"]["imageUrl"]
    article_info['multimedia_content'][f"image_{nr}"]["width"] = iterate_thru_tags_propriety(response, "meta", "og"
                                                                                                               ":image:width")
    article_info['multimedia_content'][f"image_{nr}"]["height"] = iterate_thru_tags_propriety(response, "meta", "og"
                                                                                                                ":image:height")
    article_info['organization'] = {}
    article_info['author'] = {}
    if iterate_thru_tags_name(response, "meta", "twitter:data1") == "":
        article_info['author']["authorName"] = iterate_thru_tags_name(response, "meta", "twitter:creator")
    else:
        article_info['author']["authorName"] = iterate_thru_tags_name(response, "meta", "twitter:data1")

    article_info['author']["authorNationality"] = \
        iterate_thru_tags_propriety(response, "meta", "og:locale")
    article_info['organization']["organizationName"] = iterate_thru_tags_name(response, "meta", "twitter:creator")
    article_info['generatedAtTime'] = iterate_thru_tags_propriety(response, "meta", "article:published_time")
    take_information_jsonld = iterate_thru_tags_type(response, "script", 'application/ld+json')
    print("print information",take_information_jsonld)
    organization_id = None
    organization_name = None
    word_count = None
    keywords = None
    image_url = None
    image_object = None
    image_caption = None
    # organization_name = take_information_jsonld["@graph"][0]["name"]
    # organization_id = take_information_jsonld["@graph"][0]["url"]
    # image_url = take_information_jsonld["@graph"][0]["image"]["url"]
    # image_caption = take_information_jsonld["@graph"][0]["image"]["caption"]
    # print("Image URL:", image_url)
    # print("Image Caption:", image_caption)
    # print("Organization:", organization_name)
    # print("Organization ID:", organization_id)
    for item in take_information_jsonld.get('@graph', []):
        authors = item.get('author', [])
        for author in authors:
                if '@type' in author and author['@type'] == 'Organization':
                    print(author)
                    organization_name = author.get('name')
                    organization_id = author.get('@id')
                    print("Organization:", organization_name)
                article_info['organization']["organizationName"] = organization_name
        if '@type' in item and item['@type'] == 'NewsArticle':
            if organization_id is None:
                organization_id = item["publisher"]["@id"]
                article_info['organization']["organizationId"] = organization_id
                print("Organization ID:", organization_id)
            word_count = item.get('wordCount', None)  # Set to None initially
            word_count = word_count if word_count is not None else "Word count not available"
            article_info['wordCount'] = word_count
            print("Word Count:", word_count)

            keywords = item.get('keywords', [])  # Set to empty list initially
            print("Keywords:", ', '.join(keywords))
            article_info['keywords'] = keywords
            image_object = item.get('image')  # Set to empty dictionary initially
            # if image_object is list:
            #     image_id = image_object[0].get('@id', "Image URL not available")
            #     image_url = image_object[0].get('url', "Image URL not available")
            #     image_width = image_object[0].get('width', "Image URL not available")
            #     image_height = image_object[0].get('height', "Image URL not available")
            #     image_description = image_object[0].get('caption', "Image caption not available")
            #     print("Image URL:", image_url)
            #     print("Image Caption:", image_caption)
            # elif image_object is dict:





    # media_files = []
    #
    # for img in soup.find_all('img'):
    #     media_files.append(img['src'])
    #
    # for video in soup.find_all('video'):
    #     media_files.append(video['src'])
    #
    # article['media_files'] = media_files

    return article_info
def crawl_article_lrb(url):
    article_info = {}
    response = requests.get(url)

    article = {}
    nr = 1
    article_info["articleName"] = iterate_thru_tags_propriety(response, "meta", "og:title")
    article_info['articleBody'] = iterate_thru_tags_propriety(response, "meta", "og:description")
    article_info['articleUrl'] = iterate_thru_tags_propriety(response, "meta", "og:url")
    article_info['articleDatePublished'] = \
        iterate_thru_tags_propriety(response, "meta", "article:published_time").split("T")[0]
    article_info['multimedia_content'] = {}
    article_info['multimedia_content'][f"image_{nr}"] = {}

    article_info['multimedia_content'][f"image_{nr}"]["imageUrl"] = iterate_thru_tags_propriety(response, "meta", "og"
                                                                                                                  ":image")
    article_info['multimedia_content'][f"image_{nr}"]["imageId"] = article_info['multimedia_content'][f"image_{nr}"]["imageUrl"]
    article_info['multimedia_content'][f"image_{nr}"]["width"] = iterate_thru_tags_propriety(response, "meta", "og"
                                                                                                               ":image:width")
    article_info['multimedia_content'][f"image_{nr}"]["height"] = iterate_thru_tags_propriety(response, "meta", "og"
                                                                                                                ":image:height")
    article_info['organization'] = {}
    article_info['author'] = {}
    if iterate_thru_tags_name(response, "meta", "twitter:data1") == "":
        article_info['author']["authorName"] = iterate_thru_tags_name(response, "meta", "twitter:creator")
    else:
        article_info['author']["authorName"] = iterate_thru_tags_name(response, "meta", "twitter:data1")

    article_info['author']["authorNationality"] = \
        iterate_thru_tags_propriety(response, "meta", "og:locale")
    article_info['organization']["organizationName"] = iterate_thru_tags_name(response, "meta", "twitter:creator")
    article_info['generatedAtTime'] = iterate_thru_tags_propriety(response, "meta", "article:published_time")
    take_information_jsonld = iterate_thru_tags_type(response, "script", 'application/ld+json')
    print(take_information_jsonld)
    article_info['organization']["organizationName"] =take_information_jsonld["@graph"][0]["name"]
    author = take_information_jsonld["@graph"][1]["author"][0]
    author_id = take_information_jsonld["@graph"][1]["author"][0]["@id"]
    author_name = take_information_jsonld["@graph"][1]["author"][0]["name"]
    print(author, author_name, author_id)

    organization_id = None
    organization_name = None
    word_count = None
    keywords = None
    image_url = None
    image_object = None
    image_caption = None
    # organization_name = take_information_jsonld["@graph"][0]["name"]
    # organization_id = take_information_jsonld["@graph"][0]["url"]
    # image_url = take_information_jsonld["@graph"][0]["image"]["url"]
    # image_caption = take_information_jsonld["@graph"][0]["image"]["caption"]
    # print("Image URL:", image_url)
    # print("Image Caption:", image_caption)
    # print("Organization:", organization_name)
    # print("Organization ID:", organization_id)
    for item in take_information_jsonld.get('@graph', []):
        authors = item.get('author', [])
        for author in authors:
                if '@type' in author and author['@type'] == 'Organization':
                    print(author)
                    organization_name = author.get('name')
                    organization_id = author.get('@id')
                    print("Organization:", organization_name)
                article_info['organization']["organizationName"] = organization_name
        if '@type' in item and item['@type'] == 'NewsArticle':
            if organization_id is None:
                organization_id = item["publisher"]["@id"]
                article_info['organization']["organizationId"] = organization_id
                print("Organization ID:", organization_id)
            word_count = item.get('wordCount', None)  # Set to None initially
            word_count = word_count if word_count is not None else "Word count not available"
            article_info['wordCount'] = word_count
            print("Word Count:", word_count)

            keywords = item.get('keywords', [])  # Set to empty list initially
            print("Keywords:", ', '.join(keywords))
            article_info['keywords'] = keywords
            image_object = item.get('image')  # Set to empty dictionary initially
            # if image_object is list:
            #     image_id = image_object[0].get('@id', "Image URL not available")
            #     image_url = image_object[0].get('url', "Image URL not available")
            #     image_width = image_object[0].get('width', "Image URL not available")
            #     image_height = image_object[0].get('height', "Image URL not available")
            #     image_description = image_object[0].get('caption', "Image caption not available")
            #     print("Image URL:", image_url)
            #     print("Image Caption:", image_caption)
            # elif image_object is dict:





    # media_files = []
    #
    # for img in soup.find_all('img'):
    #     media_files.append(img['src'])
    #
    # for video in soup.find_all('video'):
    #     media_files.append(video['src'])
    #
    # article['media_files'] = media_files

    return article_info

url = "https://www.bzi.ro/un-schimb-de-replici-care-a-pornit-pe-pagina-de-instagram-a-laviniei-pirva-a-avut-o-in" \
      "-centrul-atentiei-pe-andreea-marin-de-la-ce-a-inceput-totul-4908113 "
url2 = "https://www.libertatea.ro/entertainment/site-ul-cancanro-prins-cu-mata-n-sac-la-furat-de-stiri-435777"
list_of_articles = [url, "https://www.bzi.ro/ce-relatie-are-horia-brenciu-cu-fiul-adoptiv-pot-spune-doar-ca-am-uitat-cat-de-dificil-a-fost-4908842",
                   "https://www.bzi.ro/florin-ristei-s-a-afisat-pe-internet-alaturi-de-o-alta-vedeta-fanii-si-prietenii-sai-l-au-felicitat-imediat-4908726","https://www.bzi.ro/el-este-soferul-care-a-accidentat-o-femeie-pe-trecerea-de-pietoni-din-targu-cucu-abia-luase-permisul-de-conducere-exclusiv-foto-video-4909383"]

for article in list_of_articles:
    article_data = crawl_article_bzi(article)
    number = list_of_articles.index(article)
    article_data = {f"article{number+1}": article_data}
    article_list.append(article_data)

print(article_list)
# article_data = crawl_article_lrb(url2)
