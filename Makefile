migrate:
	docker run --rm -v ${PWD}/sql:/flyway/sql -v ${PWD}/flyway.conf:/flyway/conf flyway/flyway migrate