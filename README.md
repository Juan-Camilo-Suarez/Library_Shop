# Library_Shop

### Установка и запуск проекта
1. Создать виртуальное окружение:\
```python -m venv venv```
2. Активировать виртуальное окружение:\
```venv\Scripts\activate.bat``` - для Windows \
```source venv/bin/activate``` - для Linux и MacOS
3. Установить зависимости:\
```pip install -r requirements.txt```
4. Установите PostgreSQL and Redis
```docker-compose up -d ```
5. Применить миграции к базе данных:\
```python manage.py migrate```
6. Запуск сервера:\
```python src/app/manage.py runserver```
7. Загрузить fixture на бд:\
```python src/manage.py loaddata fixtures/initial_data.json ```

# Diagram
![image](https://github.com/Juan-Camilo-Suarez/Library_Shop/assets/71409094/7db36adb-9aa4-4573-8e34-d71ecc8398a8)
