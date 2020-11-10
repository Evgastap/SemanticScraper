import requests
import multiprocessing
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


def get_person_info(person_id):
	"""
	For now, gets the birth date of the person
	:param person_id: personal ID used to navigate to the IMDB page
	:return: birthday in format yyyy-mm-dd
	"""
	url = "https://www.imdb.com" + person_id
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	result = soup.find("div", id="name-born-info")
	if result is not None:
		try:
			return result.find("time").attrs['datetime']
		except AttributeError:
			return None
	else:
		return None


def main():
	# define url and make request
	url = 'https://www.imdb.com/list/ls093785287/'
	page = requests.get(url)

	# scape the page and get all the separate movie divs
	soup = BeautifulSoup(page.content, 'html.parser')
	results = soup.find_all(class_='lister-item mode-detail')

	# set up xml
	imdb = Element('imdb')

	i = 0
	for result in results:
		print("iteration %s" % i)
		i += 1
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
		try:
			# get only the year number in brackets, sometimes there are other vals
			year = year[year.index("(") + 1:year.index(")")]
		except ValueError:
			print(year)  # sometimes "year" is just an empty string...

		# get genres from subheader
		genres = subheader.find("span", class_="genre").text
		genres_array = genres.strip().replace("\n", "").split(", ")  # removes trailing whitespace and line break

		# get director and stars from the cast under description
		cast_elements = cast.find_all("a")
		director = cast_elements[0].text
		director_id = cast_elements[0].attrs['href']
		director_dob = get_person_info(director_id)

		# PUT DATA IN XML
		# default movie data
		xml_movie = SubElement(imdb, "movie", {"id": movie_id})
		xml_year = SubElement(xml_movie, "year")
		xml_year.text = year
		xml_title = SubElement(xml_movie, "title")
		xml_title.text = title

		# genre data
		xml_genres = SubElement(xml_movie, "genres")
		for genre in genres_array:
			xml_genre = SubElement(xml_genres, "genre")
			xml_genre.text = genre

		# director data
		xml_director = SubElement(xml_movie, "director", {"id": director_id})
		xml_director_name = SubElement(xml_director, "name")
		xml_director_name.text = director
		xml_director_dob = SubElement(xml_director, "dob")
		xml_director_dob.text = director_dob

		# actor data
		cast_dict = {}
		for actor in cast_elements[1:]:
			actor_name = actor.text
			actor_id = actor.attrs['href']
			actor_dob = get_person_info(actor_id)
			cast_dict[actor_name] = actor_id

			xml_actor = SubElement(xml_movie, "actor", {"id": actor_id})
			xml_actor_name = SubElement(xml_actor, "name")
			xml_actor_dob = SubElement(xml_actor, "dob")
			xml_actor_dob.text = actor_dob
			xml_actor_name.text = actor_name

	# write data to XML
	myfile = open("export.xml", "w")
	myfile.write(prettify(imdb))


if __name__ == "__main__":
	main()
