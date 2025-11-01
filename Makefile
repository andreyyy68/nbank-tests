start-app:
	bash infra/docker_compose/start-app.sh

run-tests:
	run-tests:
	pytest -m "api or ui" \
		--html=reports/report.html \
		--self-contained-html \
		--alluredir=reports/allure \
		-v -s --tb=long
