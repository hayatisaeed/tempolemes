# Tempolemes

## 

```bash
git clone https://github.com/hayatisaeed/tempolemes.git
```

create virtualenv:
```bash
pip install --upgrade virtualenv

cd tempolemes

virtualenv venv  # create venv

source/venv/bin/activate  # activate the venv
```

install packages:
```bash
pip install -r requirements.txt
```

make migrations:
```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

create superuser:
```bash
python3 manage.py createsuperuser
```

run server:
```bash
python3 manage.py runserver
```

then go to: http://127.0.0.1:8000/
