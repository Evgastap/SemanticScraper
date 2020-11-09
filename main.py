import requests
from bs4 import BeautifulSoup
from xml.etree import ElementTree
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement


def prettify(elem):
	"""
    Return a pretty-printed XML string for the Element.
    """
	rough_string = ElementTree.tostring(elem, 'utf-8')
	reparsed = minidom.parseString(rough_string)
	return reparsed.toprettyxml(indent="  ")


def main():
	# define url and make request
	url = 'https://www.imdb.com/list/ls093785287/'
	page = requests.get(url)

	# scape the page and get all the separate movie divs
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find_all(class_='lister-item mode-detail')

	# set up xml
	imdb = Element('imdb')

	for result in results:
		# PARSE HTML
		# get the HTML for the displayed attributes on page
		header = result.find("h3", class_="lister-item-header")
		p_elements = result.find_all("p", class_="text-muted text-small")  # there are multiple p's with that class
		subheader = p_elements[0]
		cast = p_elements[1]

		# get title, movie ID and year from header
		title_elem = header.find("a")
		title = header.find("a").text
		movie_id = title_elem.attrs['href']  # movie ID from the href
		year = header.find("span", class_="lister-item-year").text

		# get genres from subheader
		genres = subheader.find("span", class_="genre").text

		# get director and stars from the cast under description
		cast_elements = cast.find_all("a")
		director = cast_elements[0].text
		director_id = cast_elements[0].attrs['href']
		cast_dict = {}

		# PUT DATA IN XML
		# movie data
		xml_movie = SubElement(imdb, "movie", {"id": movie_id})
		xml_year = SubElement(xml_movie, "year")
		xml_year.text = year
		xml_title = SubElement(xml_movie, "title")
		xml_title.text = title
		xml_genres = SubElement(xml_movie, "genres")
		xml_genres.text = genres

		# director data
		xml_director = SubElement(xml_movie, "director", {"id": director_id})
		xml_director_name = SubElement(xml_director, "name")
		xml_director_name.text = director

		# actor data
		for actor in cast_elements[1:]:
			actor_name = actor.text
			actor_id = actor.attrs['href']
			cast_dict[actor_name] = actor_id

			xml_actor = SubElement(xml_movie, "actor", {"id": actor_id})
			xml_actor_name = SubElement(xml_actor, "name")
			xml_actor_name.text = actor_name

	# write data to XML
	mydata = ElementTree.tostring(imdb)
	myfile = open("export.xml", "w")
	myfile.write(str(mydata))


if __name__ == "__main__":
	main()
