run: certs/cert.pem certs/key.pem
	docker-compose up

down:
	docker-compose down
	rm -rf certs


certs/%.pem:
	mkdir -p certs
	mkcert -install || true
	mkcert -cert-file certs/cert.pem -key-file certs/key.pem blog.localhost
	echo "Certificates generated"
