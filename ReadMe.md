
# Running an Application with Docker Compose  
This tutorial will help you run an application on your local machine using Docker Compose.  
## Prerequisites  
1. **Docker**. Make sure Docker is installed on your machine. You can download it from the official [website](https://www.docker.com/get-started/).  
2. **Docker Compose**. Docker Compose is usually bundled with Docker. Make sure it is installed by running the command:  
   ```bash  
   docker-compose --version
   ```
3. `.env` **File**. Make sure you have a .env file with the necessary environment variables. 
File `.env.sample` contains the necessary template to work. Example content:  
    ```  
    POSTGRES_DB=your_db_name  
    POSTGRES_USER=your_db_user
    POSTGRES_PASSWORD=your_db_password
    POSTGRES_HOST=db 
    POSTGRES_PORT=5432 
    TG_TOKEN=your_telegram_bot_token 
	```
## Launching the application  
1. **Clone the repository** (if you haven't already):  
   ```bash  
   git clone https://github.com/goqwertys/habit-tracker.git  
   cd habit-tracker  
   ```
2. Build and run containers:  
   ```bash  
   docker-compose -f docker-compose.dev.yml up --build
   ```
   This command:  
   - Builds the images described in the Dockerfile.  
   - Runs the containers described in docker-compose.dev.yml.  
3. **Create a superuser**:  
   ```  
   create_superuser  
   ```
4. **Access to the application**:  
    - Your application will be available at: http://localhost:8000
    - If you are using PostgreSQL, it will be available on port 5432.
    - Redis will be available on port 6379.
## Stopping the application
To stop containers, run:
   ```bash
	docker-compose -f docker-compose.dev.yml down
   ```
If you want to remove volumes (eg PostgreSQL data), use:
   ```bash
	docker-compose -f docker-compose.dev.yml down -v
   ```
## Logs
To view logs for a specific service, use the command:
   ```bash
	docker-compose -f docker-compose.dev.yml logs <service_name>
   ```
For example:
   ```bash
	docker-compose -f docker-compose.dev.yml logs web
   ```
## Useful commands
- View running containers:
	```bash
	docker-compose -f docker-compose.dev.yml ps
	```
- Stopping all containers::
	```bash
	docker-compose -f docker-compose.dev.yml down
	```
- Cleaning Docker (removing unused data):
	```bash
	docker system prune -f
	```
