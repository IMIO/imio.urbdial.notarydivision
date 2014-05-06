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


*** Keywords ***

Suite Setup
    Open test browser
    Enable autologin as  test-user
