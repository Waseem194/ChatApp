# Chat App
This project is a high-performance, containerized chat application built with FastAPI, Socket.IO, and Redis. 
It provides a real-time messaging experience with a modern UI and persistent message logging.

## 🚀 How to Run This Project

1. Make sure you have atleast `Python 3.14.3` installed.
2. Create virtual envirement through this command:

```bash
python -m venv <environment_name>
```

3. Activate your newly created virtual environment by this command

```bash
source <env_name>/bin/activate  -- MACOS
source <env_name>/Scripts/activate -- Windows
```

4. After creating virtual envirement, then install requirements.txt through this command:

```bash
pip install -r requirements.txt
```

5. After this to Navigate main.py file then run this command:

```bash
uvicorn main:socket_app --reload
```


6. Run docker commands

#### Build and start docker container

```bash
docker-compose up --build
```

#### Kill and stop running docker container

```bash
docker compose down
```



