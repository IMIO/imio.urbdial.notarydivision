*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

*** Test Cases ***

Test plone searchbox is disabled
    Go to  ${PLONE_URL}
    Page Should Not Contain Button  searchGadget
    Page Should Not Contain Button  searchButton


Test plone root default portlets are disabled
    Go to  ${PLONE_URL}/@@manage-portlets
    Page should contain  Manage portlets for
    Page Should Not Contain Button  navigation-show
    Page Should Not Contain Button  navigation-hide


Test site view redirect to notarydivisions folder view
    Go to  ${PLONE_URL}
    Location should be  ${PLONE_URL}/notarydivisions


Test redirect to login form page for anonymous
    Logout
    Go to  ${PLONE_URL}
    Page Should Contain Button  Log in


*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  Log in
