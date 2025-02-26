#!/bin/bash

lint_it() {
	python -m pip install --upgrade pip
        pip install pylint
	pylint app
}

$*

