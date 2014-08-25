*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

*** Test Cases ***

Test parcel delete redirects on estate tab
    Go to  ${PLONE_URL}/notarydivisions/test_notarydivision
    Click link  fieldset-estate
    Delete initial parcel  1
    Confirm Action
    Location should be  http://localhost:55001/plone/notarydivisions/test_notarydivision/#fieldset-estate

*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit

Delete initial parcel
    [Arguments]  ${parcel_number}
    Delete parcel  ${parcel_number}  initial

Delete parcel
    [Arguments]  ${parcel_number}  ${parcel_type}
    Click element  xpath= //fieldset[@id='${parcel_type}_estate']//tbody//tr[${parcel_number}]//form[@name='deleteUidForm']//img
