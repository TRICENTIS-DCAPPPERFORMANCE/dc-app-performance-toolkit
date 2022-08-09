import random
import selectors

from selenium.webdriver.common.by import By
from selenium_ui.jira.pages.pages import Search
from selenium_ui.jira.pages.pages import Issue

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.set_credentials(username=username, password=password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()

def view_issue_qtest_scenario_plugin_enabled(webdriver, datasets):
    issue_page = Issue(webdriver, issue_key=datasets['custom_issue_key'])

    @print_timing("selenium_view_issue_qtest_scenario_plugin_enabled")
    def measure():
        issue_page.go_to()
        issue_page.wait_for_page_loaded()

        # switch to qTest Scenario iframe
        issue_page.wait_until_available_to_switch((By.XPATH, "//div[@id='ap-com.qasymphony.qtestscenario.version2__gherkin-web-panel']//iframe"))
        issue_page.wait_until_any_ec_presented(selectors=[(By.XPATH, "//div[@id='settings-container']/label[contains(text(),'Repository')]|//div[@id='editor-container']//span[contains(text(),'Repository')]")])
        issue_page.return_to_parent_frame()

    measure()

def search_jql_qtest_scenario_plugin_enabled(webdriver, datasets):
    
    jql = JIRA_SETTINGS.custom_dataset_query
    search_page = Search(webdriver, jql)

    @print_timing("selenium_search_jql_qtest_scenario_plugin_enabled")
    def measure():
        search_page.go_to()
        search_page.wait_for_page_loaded()

        # switch to qTest Widget iframe
        search_page.wait_until_available_to_switch((By.XPATH, "//div[@id='ap-com.qasymphony.qtestscenario.version2__gherkin-web-panel']//iframe"))
        search_page.wait_until_any_ec_presented(selectors=[(By.XPATH, "//div[@id='settings-container']/label[contains(text(),'Repository')]|//div[@id='editor-container']//span[contains(text(),'Repository')]")])
        search_page.return_to_parent_frame()
    measure()

def update_issue_qtest_scenario_plugin_enabled(webdriver, datasets):
    issue_page = Issue(webdriver, issue_id=datasets['custom_issue_id'])

    @print_timing("selenium_update_issue_qtest_scenario_plugin_enabled")
    def measure():

        @print_timing("selenium_update_issue_qtest_scenario_plugin_enabled:open_edit_issue_form")
        def sub_measure():
            issue_page.go_to_edit_issue()  # open editor
        sub_measure()

        issue_page.fill_summary_edit()  # edit summary

        @print_timing("selenium_update_issue_qtest_scenario_plugin_enabled:save_edit_issue_form")
        def sub_measure():
            issue_page.edit_issue_submit()  # submit edit issue
            issue_page.wait_for_issue_title()
        sub_measure()
    measure()

