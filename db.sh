#!/bin/bash

rm courses.sqlite
initialize_courses_db development.ini
populate_db development.ini

