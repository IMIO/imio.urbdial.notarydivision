for po in $(find . -path '*/notarydivision/locales/*/LC_MESSAGES/*.po'); do
        msgfmt -o ${po/%po/mo} $po;
    done
