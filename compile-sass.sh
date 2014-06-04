#!/bin/sh
cd $(dirname $0)
sass --scss --style=expanded "staff_toolbar/sass/staff_toolbar.scss" "staff_toolbar/static/staff_toolbar/staff_toolbar.css"
rm -Rf .sass-cache/
