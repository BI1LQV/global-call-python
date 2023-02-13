#! bash
rimraf ./dist
python3 setup_browser.py sdist bdist_wheel
twine upload dist/*

rimraf ./dist
python3 setup.py sdist bdist_wheel
twine upload dist/*