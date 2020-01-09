server {
    listen 80;
    listen [::]:80;

    server_name *.mybobalist.com mybobalist.com;

    location / {
        proxy_pass http://127.0.0.1:3034;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}