from selenium import webdriver
import time
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

		# implicit wait foe 1 second
		time.sleep(1)

		# we instruct the function to wait until the translated text is loaded properly
		delay = 10
		try:
			WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, "//div[@class = 'result-shield-container tlid-copy-target']")))
		except TimeoutException:
			print('translation result not yet loaded after {}s, now executing an implicit 5s wait'.format(delay))
			self.driver.implicitly_wait(5)

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
			try:
				translated.append(self.translate_text(text))
			except StaleElementReferenceException as e:
				print('... stale element ...!')
				translated.append('')
			now = time.time()
			to_print = "text no.{} complete,total time lapsed: {:02} seconds, estimated time remaining: {:02} seconds".format(i+1, now - begin, (now - begin)/(i+1)*(len(texts) - i + 1))
			to_print = '\r' + to_print
			print(to_print, end = '')

		return(translated)