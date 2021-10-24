# Heart attack possibility
Итоговый проект курса "Машинное обучение в бизнесе"

Стек:
- ML: sklearn, pandas, numpy
- API: flask
- Данные: с kaggle - https://www.kaggle.com/nareshbhat/health-care-data-set-on-heart-attack-possibility

Задача: Предсказать есть ли риск сердечного заболевания у человека (поле target). Бинарная классификация

Используемые признаки:

- age - возраст (integer)
- sex - пол (integer)
- cp - тип боли в груди (4 варианта ответа) (integer)
- trestbps - артериальное давление в состоянии покоя (integer)
- chol - уровень холестерина мг/дл (integer)
- fbs - уровень сахара в крови натощак > 120 мг / дл (integer)
- restecg - результаты электрокардиографии в покое (значения 0,1,2) (integer)
- thalach - достигнутая максимальная частота пульса (integer)
- exang - стенокардия, вызванная физической нагрузкой (integer)
- oldpeak - депрессия ST, вызванная упражнениями по сравнению с отдыхом (float)
- slope - наклон сегмента ST при пиковой нагрузке (integer)
- ca - количество крупных сосудов (0-3), окрашенных флурозопией (integer)
- thal - 0 = нормально; 1 = исправленный дефект; 2 = обратимый дефект (integer)
- target - 1 - высокий шанс сердечного приступа; 0 - низкий шанс сердечного приступа (integer)

Модель: RandomForestClassifier

## Порядок действий для запуска API

### Клонируем репозиторий и создаем образ
```
$ git clone https://github.com/mayo889/ML_model_flask_docker.git
$ cd ML_model_flask_docker
$ docker build -t  ml_model .
```

### Запускаем контейнер

Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель. (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)
```
$ docker run -d -p 8180:8180 -p 8181:8181 -v <your_local_path_to_pretrained_models>:/app/app/models ml_model
```

### Переходим на localhost:8181
