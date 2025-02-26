#!/bin/bash

lint_it() {
	docker run -it --rm fastapi-sample "python -m pip install --upgrade pip && pip install pylint && pylint app"
}

$*

