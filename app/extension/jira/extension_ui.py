import random

from selenium.webdriver.common.by import By
from selenium_ui.jira.pages.selectors import SearchLocators

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
            #page.wait_until_visible((By.CSS_SELECTOR, "div[class='project']"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()

def view_issue_qtest_plugin_enabled(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_key = datasets['custom_issue_key']

    @print_timing("selenium_view_issue_qtest_plugin_enabled")
    def measure():

        @print_timing("selenium_view_issue_qtest_plugin_enabled:view_issue_qtest_test_execution")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/browse/{issue_key}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_available_to_switch((By.CSS_SELECTOR, "#qtest-test-run-link-panel iframe"))
            page.wait_until_any_ec_presented(selectors=[(By.XPATH, "(//div[@class='aui-group']/div[contains(text(),'There is no test run associated with this issue.')]) | (//div[@class='iframe-bar-chart-stack']/div)")])
            page.return_to_parent_frame()

        sub_measure()
    measure()

def search_jql_qtest_plugin_enabled(webdriver, datasets):
    page = BasePage(webdriver)
    #jql = "Project in (JPTS, JPTK) and summary ~ '*qTestManagerIssue*' ORDER BY Key DESC, updated DESC"
    jql = "summary ~ 'ManagerIssue*' ORDER BY Key DESC, updated DESC"

    @print_timing("selenium_search_jql_qtest_plugin_enabled")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/issues/?jql={jql}")
        page.wait_until_any_ec_presented(selectors=[SearchLocators.search_issue_table,
                                                          SearchLocators.search_issue_content,
                                                          SearchLocators.search_no_issue_found])
        # switch to qTest Widget iframe
        page.wait_until_available_to_switch((By.CSS_SELECTOR, "#qtest-test-run-link-panel iframe"))
        page.wait_until_any_ec_presented(selectors=[(By.XPATH, "(//div[@class='aui-group']/div[contains(text(),'There is no test run associated with this issue.')]) | (//div[@class='iframe-bar-chart-stack']/div)")])
        page.return_to_parent_frame()

    measure()

def view_qtest_widget_qtest_plugin_enabled(webdriver, datasets):
    page = BasePage(webdriver)

    @print_timing("selenium_view_qtest_widget_plugin_enabled")
    def measure():
        page.go_to_url(f"{JIRA_SETTINGS.server_url}/projects/SLTP?selectedItem=com.qas.qtest.plugins.jira-plugin:qtest-panel")
        page.wait_until_visible((By.CSS_SELECTOR, "#sidebar-page-container iframe"))

        # switch to qTest Widget iframe
        page.wait_until_available_to_switch((By.CSS_SELECTOR, "#sidebar-page-container iframe"))
        page.wait_until_visible((By.XPATH, "//form[@id='select-project']//button"))
        page.wait_until_visible((By.XPATH, "//div/h3[text()='Resolved Defects: By Test Run Status']/../..//a[text()='View Defects']"))
        page.return_to_parent_frame()

    measure()

