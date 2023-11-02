#!/usr/bin/bash
# setup the aws server and install some missing programs/dependencies to accommodate qalchemy_v1

# install missing python3 modules 
pip3 install lxml
pip3 install beautifulsoup4
sudo pip3 install gunicorn

# config nginx to manage static request and reverse proxy dynamic request to gunicorn flask app on :8000
config=$(cat <<EOF
server {
	listen 80 default_server;
	listen [::] default_server;
	add_header X-Served-By 212691-web-01;

	root /var/www/html;
	index index.html;
	server_name qalchemy.plexusdev.tech;

	location / {
		alias /home/ubuntu/qalchemy_v1/search/templates/;
		index.html;
	}

	location /static {
		alias /home/ubuntu/qalchemy_v1/search/static/
	}

	location /search {
		proxy_pass https://127.0.0.1:8000;
		proxy_set_header Host $host;
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header Content-Length $content_length;
		proxy_set_header Content-Type $content_type;
		proxy_set_header X-Request-Body $request_body;
	}

	error_page 404 /error.html;
}
EOF
)

# copy the content of default nginx file before being replace.
if [ ! -e /etc/nginx/sites-enabled/default.copy ]; then
	sudo cp /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default.copy
fi

echo "$config" | sudo tee /etc/nginx/sites-enabled/default >dev/null


# set up supervisor - I would have used systemd but i prefer to allocate it to supervisor since qalchemy is currently lightweighted.

sudo apt install -y supervisor

config_supervisor=$(cat <<EOF
[program:qalchemy]
directory=/home/ubuntu/qalchemy_v1/
command=gunicorn -w 3 search.app:qalchemy
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stdout_logfile=/var/log/qalchemy/access.log
stderr_logfile=/var/log/qalchemy/error.log
EOF
)


# i need to make qalchemy directory and touch access and error files 

sudo mkdir -p /var/log/qalchemy
sudo touch /var/log/qalchemy/{access.log,error.log}

sudo touch /etc/supervisor/conf.d/qalchemy.conf 

sudo echo "$config_supervisor" | sudo tee /etc/supervsior/conf.d/qalchemy.conf

# now restart and reload

sudo service nginx restart
sudo supervisorctl reload
