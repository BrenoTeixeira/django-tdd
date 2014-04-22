from selenium import webdriver
from selenium.webdriver.common.keys import Keys


from django.test import LiveServerTestCase


class AdminTest(LiveServerTestCase):

    fixtures = ['ft/fixtures/admin.json']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def get_body_context(self):
        self.body = self.browser.find_element_by_tag_name('body')
        return self.body

    def test_admin_site(self):
        # user opens web browser, navigates to admin page
        self.browser.get(self.live_server_url + '/admin/')
        self.get_body_context()
        self.assertIn('Django administration', self.body.text)
        # user types in username and passwords and presses enter
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('123456')
        password_field.send_keys(Keys.RETURN)
        # login credentials are correct, and user is redirected to the main admin page
        self.get_body_context()
        self.assertIn('Site administration', self.body.text)
        # user clicks on the Users link
        user_link = self.browser.find_element_by_link_text('Users')
        user_link.click()
        # user verifies that user live@forever.com is present
        self.get_body_context()
        self.assertIn('brenotx@gmail.com', self.body.text)
        # user clicks on the add link
        add_user_link = self.browser.find_element_by_link_text('Add user')
        add_user_link.click()
        # user types in username and password
        username_field = self.browser.find_element_by_id('id_username')
        username_field.send_keys('new_user')
        password_field = self.browser.find_element_by_id('id_password1')
        password_field.send_keys('123456')
        password_confirmation_field = self.browser.find_element_by_id('id_password2')
        password_confirmation_field.send_keys('123456')
        password_confirmation_field.send_keys(Keys.RETURN)
        # user verifies successful message
        self.get_body_context()
        self.assertIn('The user "new_user" was added successfully', self.body.text)

    def test_create_contact_admin(self):
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('admin')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('123456')
        password_field.send_keys(Keys.RETURN)
        # user verifies that user_contacts is present
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('User_Contacts', body.text)
        # user clicks on the Person link
        person_link = self.browser.find_element_by_link_text('Persons')
        person_link.click()
        # user clicks on the Add person link
        add_person_link = self.browser.find_element_by_link_text('Add person')
        add_person_link.click()
        # user fills out the form
        self.browser.find_element_by_name('first_name').send_keys('Breno')
        self.browser.find_element_by_name('last_name').send_keys('Teixeira')
        self.browser.find_element_by_name('email').send_keys('brenotx@gmail.com')
        self.browser.find_element_by_name('address').send_keys('2227 Lexington Ave')
        self.browser.find_element_by_name('city').send_keys('San Francisco')
        self.browser.find_element_by_name('state').send_keys('CA')
        self.browser.find_element_by_name('country').send_keys('United States')
        # user clicks the save button
        self.browser.find_element_by_css_selector('input[value="Save"]').click()
        # the person has been added
        self.get_body_context()
        self.assertIn('Teixeira, Breno', self.body.text)
        # user returns the main admin screen
        home_link = self.browser.find_element_by_link_text('Home')
        home_link.click()
        # user clicks on the Phone link
        persons_links = self.browser.find_elements_by_link_text('Phones')
        persons_links[0].click()
        # user clicks on the Add phone link
        add_person_link = self.browser.find_element_by_link_text('Add phone')
        add_person_link.click()
        # user finds the person in the dropdown
        el = self.browser.find_element_by_name("person")
        for option in el.find_elements_by_tag_name('option'):
            if option.text == 'Teixeira, Breno':
                option.click()
        # user adds the phone numbers
        self.browser.find_element_by_name('number').send_keys("4158888888")
        # user clicks the save button
        self.browser.find_element_by_css_selector("input[value='Save']").click()
        # the Phone has been added
        self.get_body_context()
        self.assertIn('4158888888', self.body.text)
        # user logs out
        self.browser.find_element_by_link_text('Log out').click()
        self.get_body_context()
        self.assertIn('Thanks for spending some quality time with the Web site today.', self.body.text)