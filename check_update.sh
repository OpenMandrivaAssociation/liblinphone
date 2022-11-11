#!/bin/sh
# We have to filter out time based releases -- 5.1.67 > 2010.03.04
git ls-remote --tags https://gitlab.linphone.org/BC/public/liblinphone 2>/dev/null|awk '{ print $2; }' |sed -e 's,refs/tags/,,;s,_,.,g;s,-,.,g;s,^v\.,,;s,^v,,' |grep -E '^[0-9.]+$' |grep -v '[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]' |sort -V |tail -n1
