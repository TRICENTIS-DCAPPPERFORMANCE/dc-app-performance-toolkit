import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.bamboo.pages.pages import JobConfiguration, Login, PlanSummary, QtestBuildConfigurationPage, QtestPluginPage
from util.conf import BAMBOO_SETTINGS




def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
   # rnd_plan = random.choice(datasets["build_plans"])

    build_plan_id = 'SBP-STP'

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
            login_page.click_login_button()
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:view_plan_summary_page")
        def sub_measure():
            page.go_to_url(f"{BAMBOO_SETTINGS.server_url}/browse/{build_plan_id}")
            page.wait_until_visible((By.ID, "buildResultsTable"))  # Wait for summary field visible
            # Wait for you app-specific UI element by ID selector
           # page.wait_until_visible((By.ID, "ID_OF_YOUR_APP_SPECIFIC_UI_ELEMENT"))
        sub_measure()
    measure()

def view_plan_summary_qtest_plugin_page_enabled(webdriver, datasets):

    build_plan_id = 'SBP-STP'
    qtest_plugin_page = QtestPluginPage(webdriver, build_plan_id=build_plan_id)

    @print_timing("view_plan_summary_qtest_plugin_page_enabled")
    def measure():
        qtest_plugin_page.go_to_plan_qtest_page()
        qtest_plugin_page.wait_for_page_loaded()

    measure()
    
def view_job_configuration_qtest_plugin_enabled(webdriver, datasets):

    build_plan_id = 'SBP-STP'
    plan_job_configuration_page = QtestBuildConfigurationPage(webdriver, build_plan_id=build_plan_id)

    @print_timing("view_job_configuration_qtest_plugin_enabled")
    def measure():
        plan_job_configuration_page.go_to_plan_qtest_build_configuration_page()
        plan_job_configuration_page.wait_for_page_loaded()

    measure()
