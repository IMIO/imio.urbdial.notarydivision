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

Test parcel specific rights display
    Go to  ${PLONE_URL}/notarydivisions/test_notarydivision
    Click link  fieldset-estate
    Edit initial parcel  1
    Select Checkbox  form-widgets-undivided_a-0
    Input Text  id=form-widgets-specific_rights_a  Im just a gigolo
    Click button  form-buttons-save
    Click link  droits des parties
    Current Frame Contains  Im just a gigolo

*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit

Edit initial parcel
    [Arguments]  ${parcel_number}
    Edit parcel  ${parcel_number}  initial

Edit parcel
    [Arguments]  ${parcel_number}  ${parcel_type}
    Click element  xpath= //fieldset[@id='${parcel_type}_estate']//tbody//tr[${parcel_number}]//img[@title='Modifier']

Delete initial parcel
    [Arguments]  ${parcel_number}
    Delete parcel  ${parcel_number}  initial

Delete parcel
    [Arguments]  ${parcel_number}  ${parcel_type}
    Click element  xpath= //fieldset[@id='${parcel_type}_estate']//tbody//tr[${parcel_number}]//form[@name='deleteUidForm']//img
