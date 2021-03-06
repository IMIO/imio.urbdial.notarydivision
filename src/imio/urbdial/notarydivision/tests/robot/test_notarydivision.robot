*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

*** Test Cases ***

Test created parcelling specific rights display
    Go to  ${PLONE_URL}/notarydivisions/test_notarydivision/edit#fieldsetlegend-estate
    Select Checkbox  form-widgets-undivided-0
    Input Text  id=form-widgets-specific_rights  Im singing in the rain
    Click button  form-buttons-save
    Click link  fieldset-estate
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
