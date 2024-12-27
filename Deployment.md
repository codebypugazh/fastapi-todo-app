Deploying a **FastAPI** app on a VPS (Virtual Private Server) involves several steps, including setting up the server, installing necessary software, deploying the application, and configuring a web server like Nginx for reverse proxy. Here's a step-by-step guide:

---

### **1. Set Up Your VPS**
1. **Access Your VPS**: Use SSH to connect to your VPS.
   ```bash
   ssh username@your_vps_ip
   ```
2. **Update Your Server**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

---

### **2. Install Required Software**
1. **Install Python**:
   ```bash
   sudo apt install python3 python3-pip python3-venv -y
   ```
2. **Install Uvicorn (ASGI server)**:
   ```bash
   pip install uvicorn fastapi
   ```

---

### **3. Prepare Your FastAPI App**
1. **Transfer Your App**:
   - Use `scp` or Git to copy your app files to the server.
   ```bash
   scp -r /path/to/your/app username@your_vps_ip:/path/on/server
   ```

2. **Set Up Virtual Environment**:
   ```bash
   cd /path/on/server
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Test the App Locally**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   Replace `main:app` with your FastAPI app's entry point.

---

### **4. Set Up Systemd Service**
To ensure your app runs in the background and restarts on failure:
1. **Create a Systemd Service File**:
   ```bash
   sudo nano /etc/systemd/system/fastapi.service
   ```

2. **Add the Following Content**:
   ```ini
   [Unit]
   Description=FastAPI app
   After=network.target

   [Service]
   User=username
   Group=groupname
   WorkingDirectory=/path/on/server
   Environment="PATH=/path/on/server/venv/bin"
   ExecStart=/path/on/server/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

3. **Reload Systemd and Start the Service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start fastapi
   sudo systemctl enable fastapi
   ```

---

### **5. Install and Configure Nginx**
1. **Install Nginx**:
   ```bash
   sudo apt install nginx -y
   ```

2. **Configure Nginx**:
   ```bash
   sudo nano /etc/nginx/sites-available/fastapi
   ```

3. **Add the Following Configuration**:
   ```nginx
   server {
       listen 80;
       server_name your_domain_or_ip;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

4. **Enable the Configuration**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   ```

---

### **6. Secure the Server with SSL**
1. **Install Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   ```

2. **Get an SSL Certificate**:
   ```bash
   sudo certbot --nginx -d your_domain
   ```

3. **Renew Certificates Automatically**:
   ```bash
   sudo crontab -e
   ```
   Add:
   ```bash
   0 0 * * * certbot renew --quiet
   ```

---

### **7. Verify the Deployment**
- Access your app at `http://your_domain_or_ip` or `https://your_domain` if SSL is enabled.
- Check logs for issues:
  ```bash
  sudo journalctl -u fastapi
  ```

That's it! Your FastAPI app should now be running on your VPS. Let me know if you hit any issues!