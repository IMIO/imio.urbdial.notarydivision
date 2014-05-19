*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

*** Test Cases ***

Test edit form fields
    Go to  ${PLONE_URL}/notarydivisions/++add++NotaryDivision
    Page should contain  Ajouter Division notariale

    Page should not contain  Exclude from navigation

    Page should contain  Référence
    Page should contain textfield  form-widgets-reference

    Page should contain  Requérant(s)
    Page should contain  Nom
    Page should contain  Prénom

    Page should contain  Affectation actuelle du bien


*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit
