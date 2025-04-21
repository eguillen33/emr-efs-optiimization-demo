# TODO - test all of these
setup-efs:
	python3 setup/setup_efs.py

run-bootstrap:
	python3 bootstrap/fetch_deps.py

run-job:
	spark-submit spark-jobs/etl_job.py

deploy-infra:
	cd infrastructure && terraform apply -auto-approve

destroy-infra:
	cd infrastructure && terraform destroy -auto-approve
