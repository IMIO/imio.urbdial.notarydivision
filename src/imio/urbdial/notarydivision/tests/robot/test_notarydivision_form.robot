*** Settings ***

Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote


Suite Setup  Suite Setup
Suite Teardown  Close all browsers

*** Variables ***

*** Test Cases ***

Test datagrid fields
    Go to  ${PLONE_URL}/notarydivisions/++add++NotaryDivision
    Page should contain  Ajouter Division notariale

    Page should contain  Requérant(s)
    Page should contain  Nom
    Page should contain  Prénom

    Page should contain  Ensemble immobilier initial
    Page should contain  Commune
    Page should contain  Division
    Page should contain  Section
    Page should contain  Radical
    Page should contain  Bis
    Page should contain  Exposant
    Page should contain  Puissance
    Page should contain  Superficie
    Page should contain  Droits des parties


*** Keywords ***

Suite Setup
    Open test browser
    Log in as admin

Log in as admin
    Go to  ${PLONE_URL}/login
    Input text  id=__ac_name  test-user
    Input password  id=__ac_password  secret
    Click Button  submit
