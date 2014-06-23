mkdir urbdial_notarydivision
mkdir urbdial_notarydivision/profiles
mkdir urbdial_notarydivision/profiles/default
cp -rf  ../profiles/default/workflows* urbdial_notarydivision/profiles/default/
archgenxml-2.7 workflows.zargo
manage generated.pot
rm -rf ../i18n
rm -rf ../profiles/default/workflows/
mv -f urbdial_notarydivision/profiles/default/workflows* ../profiles/default/
rm -rf urbdial_notarydivision
