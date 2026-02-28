jupyter nbcovert Training.ipynb --to python
jupyter nbconvert Training.ipynb --to python
clear
export IMAGE_URI=us-central1-docker.pkg.dev/project-230934ed-7015-46b8-afc/customer-churn-af/customer_churn:v1
echo $IMAGE_URI
docker
docker images
clear
docker build -f Dockerfile -t ${IMAGE_URI} ./
docker build -f Dockerfile -t ${IMAGE_URI} ./
ls requirements*
docker build -f Dockerfile -t ${IMAGE_URI} ./
clear
docker images
gcloud init
clear
gcloud auth configure-docker \us-central1-docker.pkg.dev
docker push ${IMAGE_URI}
docker push ${IMAGE_URI}
jupyter nbconvert Training.ipynb --to python
export IMAGE_URI=us-central1-docker.pkg.dev/project-230934ed-7015-46b8-afc/customer-churn-af/customer_churn:v2
echo $IMAGE_URI
docker images
docker
docker build -f Dockerfile -t ${IMAGE_URI} ./
echo $IMAGE_URI
docker images
echo $IMAGE_URI
gcloud auth configure-docker \us-central1-docker.pkg.dev
docker push ${IMAGE_URI}
clear
git add .
git commit -m "Deployed and tested"
git push -u origin main
git push origin main
git branch
git checkout main
git checkout -b main
git checkout main
git push
git push --set-upstream origin main
git push --set-upstream origin main
git push --set-upstream origin main
git push --set-upstream origin main
git push --set-upstream origin main
git remote -v
git push --set-upstream origin main
git push --set-upstream origin main
git branch
git push
git config --global user.email "23kaif05@gmail.com"
git config --global user.name "Kaif Ahmad"
git init
git remote add https://github.com/kaif2305/GCP-Customer-Churn.git
git remote add origin https://github.com/kaif2305/GCP-Customer-Churn.git
git pull origin main
