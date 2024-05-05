# K8S_falcoalert

Проект, в котором разворачивается локальный кластер K8S. 
В кластере работает утилита Falco. Она отслеживает все 
нестандартные системные вызовы ядра, не попадающие под 
список парвил. При срабатывании alerta происходит отправка 
сообщения в чат-бот Telegram.

Для работы Falco в конфигурационном  файле был прописан параметр 
```yaml
driver:
  kind: modern_ebpf
```
Это специальная система, создающая рядом с ядром песочницу, где могут 
запускаться приложения на уровне ядра без необходимости его 
перекомпиялции. Благодаря этому драйверу Falco видит все вызовы, 
происходящие в контейнерах кластера. 

## Создание кластера и запуск Falco
1. Установка необходимого софта (скрипт под Debian подобные Linux): 

    ```sudo ./devops_set.sh```
2. Запуск кластера K8S в minikube: ```minikube start```
3. Создание нового namespace: ```kubectl create namespace secured-ns```
4. Запускаем deployment: ```kubectl apply -f deployment.yaml -n secured-ns```
5. Клонируем репозиторий Falco: ```helm repo add falcosecurity https://falcosecurity.github.io/charts```
6. Обновляем репозиторий Helm: ```helm repo update```
7. Устанавливаем сначала Falcosidekick: ```helm install falcosidekick -f values-kick.yaml falcosecurity/falcosidekick -n secured-ns```
8. Устанавливаем Falco: ```helm install falco -f values-falco.yaml falcosecurity/falco -n secured-ns```
9. Запускаем бота через ``python3 main.py``

- На данном этапе кластер и бот находятся полностью в рабочем состоянии

## Триггер алерта Falco
Запустить срабатывание уведомления можно несколькими способами, подробнее можно посмотреть на git falco: https://github.com/falcosecurity/falcosidekick

- Вход в оболочку контейнера: ```kubectl exec -it ubuntu-*** -n secured-ns -- /bin/bash```
- Установка пакета nmap: ```apt update && apt install nmap -y```
- Сканирование портов: ```nmap 0.0.0.0```
- Поиск файлов id_rsa*: ```find --name id_rsa*```

## Полезные команды
1. Посмотреть список pods: ```kubectl get pods -n secured-ns``` 
2. Посмотреть список сервисов: ```kubectl get services -n secured-ns```
3. Скачать исходники Falco: ```helm pull falcosecurity/falco --untar```