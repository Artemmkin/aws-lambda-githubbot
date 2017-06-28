PROJECT = githubotik
VIRTUAL_ENV = env
FUNCTION_NAME = githubotik # change it to the name of an aws lambda function you create.
													 # This is used to update it using this Makefile

# default commands
install: virtual
build: clean_package build_package_tmp copy_python remove_unused zip

virtual:
	@echo "Setup and activate virtualenv"
	if [ ! -d ${VIRTUAL_ENV} ]; then \
		pip install virtualenv; \
		virtualenv ${VIRTUAL_ENV}; \
		source ${VIRTUAL_ENV}/bin/activate; \
		pip install -r requirements.txt; \
		deactivate; \
	fi
	@echo ""

clean_package:
	rm -rf ./package/*

build_package_tmp:
	mkdir -p ./package/tmp/lib
	cp -a ./${PROJECT}/. ./package/tmp/

copy_python:
	if [ -d ${VIRTUAL_ENV}/lib ]; then \
		cp -a ${VIRTUAL_ENV}/lib/python2.7/site-packages/. ./package/tmp; \
	fi

remove_unused:
	rm -rf ./package/tmp/wheel*
	rm -rf ./package/tmp/easy_install*
	rm -rf ./package/tmp/setuptools*

zip:
	cd ./package/tmp && zip -r ../${PROJECT}.zip .

update_lambda:
	aws lambda update-function-code \
		--function-name ${FUNCTION_NAME} \
		--zip-file fileb://package/${PROJECT}.zip
