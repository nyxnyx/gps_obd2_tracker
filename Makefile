dist:
	python3 setup.py sdist bdist_wheel

upload: dist
	python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*


.PHONY: clean
clean:
	$(RM) -rf build dist *.egg-info openapiv3/__pycache__