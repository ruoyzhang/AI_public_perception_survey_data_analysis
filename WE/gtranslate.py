from selenium import webdriver
import time

class selenium_gtranslate():

	"""
	using google translate to translate texts into English without using its paid API 
	"""

	def __init__(self, headless = True):
		"""
		init method

		headless: boolean, if True(default), the class runs in headless mode
		"""

		# setting up the driver as a class method and keep it in headless mode
		options = webdriver.FirefoxOptions()

		# headless?
		if headless:
			options.headless = headless

		# set driver
		self.driver = webdriver.Firefox(firefox_options = options)

	def get_gtranslate(self):
		"""
		open 'translate.google.com'
		"""

		url = 'https://translate.google.com/'
		print('navigating to google translate')
		self.driver.get(url)

	def translate_text(self, text):
		"""
		method used to translate a single piece of text
		we rely on the auto language detection of Google translate
		"""

		# send the required text to text box
		text_box = self.driver.find_element_by_xpath("//textarea[@id = 'source']")
		text_box.send_keys(text)

		# wait for a second
		time.sleep(1)

		# retrive the translated text
		translated = self.driver.find_element_by_xpath("//div[@class = 'result-shield-container tlid-copy-target']")

		# clear the text box field
		text_box.clear()

		return(translated.text)

	def translate_in_bulk(self, texts):
		"""
		method for translating a list of texts into English

		texts: a list of texts, order matters
		"""

		# get to the gtranslate page
		self.get_gtranslate()


		# placeholder for translated text
		translated = []

		print('now translating ...')

		# recording time lapsed
		begin = time.time()

		# loop through the list
		for i, text in enumerate(texts):
			translated.append(self.translate_text(text))
			now = time.time()
			print('text no.{} translation complete'.format(i+1))
			print('total time lapsed so far: {:02} seconds'.format(now - begin))
			print('estimated time remaining: {:02} seconds'.format((now - begin)/(i+1)*(len(texts) - i + 1)))

		return(translated)