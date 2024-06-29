# Полезные материалы

- методичка по git - https://git-scm.com/docs

---

# Как работать с проектом

1) Всегда забирайте изменения с репозитория и сливайте master ветку с своей

```shell
# находять в своей ветке
git merge master
```

2) Работайте только в своей ветке и не пуште изменения в master

3) Комментируйте код, или пишите в чат об изменениях

4) Не меняйте README.md и части, которые к вам не относятся (если что-то из этого надо - напищите в чат)

---

# Развертка и запуск проекта на локальной машине

## 1) Получаем все изменения с репозитория 

```shell
git remote add origin git@github.com:Asurasuu/neoinst.git

git pull origin master # (или git fetch, но тут смотреть придется по ситуации)
```

## 2) Запуск приложения с docker

```shell
docker build  -t python_app_neoinst .

docker run -p 8080:8080 -d python_app_neoinst:latest
```