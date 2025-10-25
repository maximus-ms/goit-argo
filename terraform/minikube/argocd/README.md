
### 1.1. Підключення до k8s кластера

В цій роботі було вирішено використати `minikube` замість `AWS`. Це додасть більше практичного досвіду у роботі з різними іниструментами.

1. Отримуємо список доступних конфігурацій у `kubectl`
```bash
kubectl config get-clusters
```
2. Активуємо локальний minicube конфіг (імʼя конфігу беремо з виводу попередньої команди)
```bash
kubectl config use-context amd2-minikube
```
3. Перевіряємо наявність нодів
```bash
kubectl get nodes
```
Бачимо вивід команди:
```
NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   3h17m   v1.34.0
```
K2s кластер піднятий і підлючений до `kubectl`, все готово до подальшої роботи.


### 1.2. Запуск ArgoCD

В даному випадку terraform для запуску ArgoCD розміщено в тому ж гіт-репозиторії що й Helm деплої для нього.

[https://github.com/maximus-ms/goit-argo.git](https://github.com/maximus-ms/goit-argo.git)

Всі подальші команди виконуємо з директорії `./terraform/minikube/argocd`

#### 1.2.1. Ініціалізуємо `terraform` проєкт
```bash
terraform init
```
#### 1.2.2. Встановлюємо `ArgoCD` додаток через `helm`. При встановленні ігноруємо запуск апплікай, щоб уникнути помилок синхронізації.
```bash
terraform apply -var="init_argocd_only=true"
```
Можна подивитися на запущені поди в неймспейсі `infra-tools` (в цьому неймспейсі ми запустили `ArgoCD`)
```bash
kubectl get pods -n infra-tools
```
#### 1.2.3. Запускаємо додатки в `ArgoCD`
```bash
terraform apply
```
В якості підказок вкінці виконання команди отримаємо маленьку шпаргалку
```
...
Outputs:

argocd_login = "admin"
argocd_password = "kubectl -n infra-tools get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d ; echo"
argocd_port_forward = "kubectl port-forward svc/argocd-server -n infra-tools 8080:80"
```
#### 1.2.4. Прокидаємо порт 80 від `ArgoCD` на наш `localhost:8080`
```bash
kubectl port-forward svc/argocd-server -n infra-tools 8080:80
```
#### 1.2.5. Дізнаємося пароль адміна
```bash
kubectl -n infra-tools get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d ; echo
```
#### 1.2.6. Відкриваємо `ArgoCD` GUI в нашому браузері за адресою

[http://localhost:8080](http://localhost:8080)


## Git-репозиторій з Helm-деплоєм

Створено git-репозиторій `goit-argo`

[https://github.com/maximus-ms/goit-argo.git](https://github.com/maximus-ms/goit-argo.git)

В репозиторії додано апплікації `demo-nginx` та `mlflow`


### 2.1. Перевіримо порти цих апплікацій (використовуємо неймспейс `application`)
```bash
kubectl get service -n application
```
Отирмали вивід:
```bash
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
demo-nginx   ClusterIP   10.106.165.104   <none>        80/TCP    146m
mlflow       ClusterIP   10.110.0.167     <none>        80/TCP    137m
```
### 2.2. Прокинемо порти до наших застосунків і перевіримо їх роботу в браузері

**Nginx:**
```bash
kubectl port-forward -n application svc/demo-nginx 8800:80
```

**MLFlow:**
```bash
kubectl port-forward -n application svc/mlflow 8880:80
```
```bash
kubectl get service -A
```
