''' This configuration file should be edited based on the website that you would like to scrape. 
    These variables will be used in the general_web_scraping and data_handling code.'''

# Setting the URL variable to the string "https://www.myprotein.com", the website you would like scraped
URL = "https://www.myprotein.com"

# This is the xpath of the button that closes the signup pop up window.
SIGN_UP_CLOSE_BUTTON_XPATH = "//button[@class='emailReengagement_close_button']"

# Setting the iframe_id variable to the id attribute of the iframe containing the accept cookies button.
IFRAME_ID = None

# This is the xpath of the button that accepts cookies.
ACCEPT_COOKIES_BUTTON_XPATH = "//button[@class='cookie_modal_button']"

# This is the xpath of the link that will open the list of the desired objects.
DESIRED_CATEGORY_XPATH = '//*[@id="mainContent"]/div[2]/a[1]'

# This is the xpath of the container that has all the desired objects.
CONTAINER_XPATH = '//*[@id="mainContent"]/div[3]/ul'

# This is the xpath of the list of all the objects.
OBJECT_LIST_RELATIVE_XPATH = './li[contains(@class, "productListProducts_product")]'

# Setting the number of pages you would like to get the objects of scraped. (page=1 means that it will
# only scrape 1 page and so on)
PAGES = 2

# This is the xpath of the button that will take you to the next page.
NEXT_BUTTON_XPATH = '//button[contains(@class, "NavigationButtonNext")]'

# A dictionary that contains the properties that you want to scrape, their xpath, and the attribute to
# extract.
DICT_PROPERTIES = {
    'Name': ('//h1[@class="productName_title"]', 'text'), 
    'Starting_Price': ('//p[@data-product-price="price"]', 'text'), 
    'Flavour_Selected': ('//select[@id="athena-product-variation-dropdown-5"]//option[@selected]', 'text'), 
    'Stars': ('//span[@class="athenaProductReviews_aggregateRatingValue"]', 'text'), 
    'Product_Image':('//img[@class="athenaProductImageCarousel_image"]', 'src'), 
    'Unique_ID':('//input[@name="prodId"]', 'value') 
    }

# This is the name of the bucket that the data will be stored in.
BUCKET_NAME = 'aicoredatacollectionbucket'