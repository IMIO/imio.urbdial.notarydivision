domain=urbdial.divnot
i18ndude rebuild-pot --pot $domain.pot --create $domain ../
i18ndude merge --pot $domain.pot --merge custom.pot
i18ndude sync --pot $domain.pot */LC_MESSAGES/$domain.po
