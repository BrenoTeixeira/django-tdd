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