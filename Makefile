stop:
	docker-compose -f src/docker-compose.yaml stop

start:
	docker-compose -f src/docker-compose.yaml up  -d --no-deps --build 

test:
	docker-compose -f src/docker-compose.yaml up --build --exit-code-from test

build:
	docker build -t hamedsalim1999/hemnet-task-app:$(version) src 
	docker push hamedsalim1999/hemnet-task-app:$(version) 

configk8s:
	aws eks update-kubeconfig --region us-east-1 --name ascode-cluster

deployk8s:
	terraform -chdir=terraform plan 
	terraform -chdir=terraform apply 

distroyk8s:
	terraform -chdir=terraform destroy 

applyingress:
	helm install ingress -n ingress --create-namespace -f k8s/ingress-nginx/values-prod.yaml k8s/ingress-nginx
	
applyk8s:
	kubectl apply -f k8s/app/server-namespace.yaml
	kubectl apply -f k8s/app


