kubectl apply -f deployment/db-configmap.yaml - Set up environment variables for the pods
kubectl apply -f deployment/db-secret.yaml - Set up secrets for the pods
kubectl apply -f deployment/postgres.yaml - Set up a Postgres database running PostGIS
kubectl apply -f deployment/udaconnect-api.yaml - Set up the service and deployment for the API
kubectl apply -f deployment/udaconnect-app.yaml - Set up the service and deployment for the web app
sh scripts/run_db_command.sh <POD_NAME> - Seed your database against the postgres pod. (kubectl get pods will give you the POD_NAME)


While the Kubernetes service for postgres is running 
(you can use kubectl get services to check), 
you can expose the service to connect locally:
kubectl port-forward svc/postgres 5432:5432
This will enable you to connect to the database at localhost. 
You should then be able to connect to postgresql://localhost:5432/geoconnections. 
This is assuming you use the built-in values in the deployment config map

We can access a running Docker container using kubectl exec -it <pod_id> sh. 
From there, we can curl an endpoint to debug network issues.
The starter project uses Python Flask. 
Flask doesn't work well with asyncio 
out-of-the-box. Consider using multiprocessing
to create threads for asynchronous behavior in a standard Flask application.

multiprocessing