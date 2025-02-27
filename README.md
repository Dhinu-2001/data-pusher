# Data Pusher

A Django project deployed on AWS with PostgreSQL, Gunicorn, and Nginx.

## **Prerequisites**
- AWS EC2 instance (Ubuntu 22.04 recommended)
- SSH access to the instance
- PostgreSQL database setup
- Domain name (optional, for HTTPS)

## **1. Clone the Project**
```bash
cd ~  # Move to home directory
git clone https://github.com/YOUR_GITHUB_USERNAME/data-pusher.git
cd data-pusher
```

## **2. Set Up a Virtual Environment**
```bash
sudo apt update && sudo apt install python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
```

## **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

## **4. Configure Environment Variables**
Create a `.env` file in the project root:
```bash
nano .env
```
Add the following environment variables (update with your values):
```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com,ec2-your-ip.compute.amazonaws.com
CSRF_TRUSTED_ORIGINS=your-domain.com,ec2-your-ip.compute.amazonaws.com
DATABASE_NAME=data_pusher
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your-db-host
DATABASE_PORT=5432
```
Save and exit (`CTRL + X`, then `Y`, then `ENTER`).

## **5. Configure PostgreSQL**
Ensure PostgreSQL is installed and create a database:
```bash
sudo -u postgres psql
```
In the PostgreSQL shell, run:
```sql
CREATE DATABASE data_pusher;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
ALTER ROLE your_db_user SET client_encoding TO 'utf8';
ALTER ROLE your_db_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE your_db_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE data_pusher TO your_db_user;
\q  # Exit PostgreSQL
```

## **6. Apply Migrations & Collect Static Files**
```bash
python manage.py makemigrations
python manage.py migrate
```

## **7. Set Up Gunicorn**
Create a Gunicorn systemd service file:
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Add:
```ini
[Unit]
Description=Gunicorn daemon for Django project
After=network.target

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/data-pusher
ExecStart=/home/ubuntu/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/data-pusher/gunicorn.sock data_pusher.wsgi:application

[Install]
WantedBy=multi-user.target
```
Save and exit.

Reload systemd and start Gunicorn:
```bash
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
Check status:
```bash
sudo systemctl status gunicorn
```

## **8. Set Up Nginx**
```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/data-pusher
```
Add the following:
```nginx
server {
    listen 80;
    server_name data-pusher.dhinu.site;

    location / {
        proxy_pass http://unix:/home/ubuntu/data-pusher/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```
Save and exit.

Enable the configuration:
```bash
sudo ln -s /etc/nginx/sites-available/data-pusher /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## **9. Secure with SSL (Let's Encrypt)**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d data-pusher.dhinu.site
```
Choose **redirect HTTP to HTTPS** when prompted.

## **10. Restart Services After Changes**
After updating `.env`, restart services:
```bash
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

## **11. Access the Application**
Visit: [https://data-pusher.dhinu.site](https://data-pusher.dhinu.site)

## **12. Logs & Debugging**
- Check Gunicorn logs:
  ```bash
  sudo journalctl -u gunicorn --no-pager --lines=50
  ```
- Check Nginx logs:
  ```bash
  sudo tail -f /var/log/nginx/error.log
  ```

---
### **Done! 🎉 Your Django project is now live on AWS.**
Let me know if you have any issues! 🚀

