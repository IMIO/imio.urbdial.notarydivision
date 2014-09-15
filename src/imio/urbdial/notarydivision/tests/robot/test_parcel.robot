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
    Delete parcel  1
    Confirm Action
    Location should be  http://localhost:55001/plone/notarydivisions/test_notarydivision/#fieldset-estate

Test created parcel specific rights display
    Go to  ${PLONE_URL}/notarydivisions/test_notarydivision
    Click link  fieldset-estate
    Edit parcel  1
    Select Checkbox  form-widgets-undivided-0
    Input Text  id=form-widgets-specific_rights  Im singing in the rain
    Click button  form-buttons-save
    Click link  droits des parties
    Current Frame Contains  Im singing in the rain

*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit

Edit parcel
    [Arguments]  ${parcel_number}
    Click element  xpath= //fieldset[@id='created_estate']//tbody//tr[${parcel_number}]//img[@title='Modifier']

Delete parcel
    [Arguments]  ${parcel_number}
    Click element  xpath= //fieldset[@id='created_estate']//tbody//tr[${parcel_number}]//form[@name='deleteUidForm']//img
