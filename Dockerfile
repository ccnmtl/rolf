FROM ccnmtl/django.base
RUN apt-get update && apt-get install -y git-core
RUN  echo "    IdentityFile ~/.ssh/id_rsa" >> /etc/ssh/ssh_config
RUN groupadd -r pusher && useradd -r -g pusher pusher \
		&& chown pusher:pusher /var \
		&& chown -R pusher:pusher /ve \
		&& mkdir /home/pusher \
		&& chown -R pusher:pusher /home/pusher
USER pusher
ADD wheelhouse /wheelhouse
RUN /ve/bin/pip install --no-index -f /wheelhouse -r /wheelhouse/requirements.txt
WORKDIR /app
COPY . /app/
RUN mkdir -p /var/www/rolf/rolf
RUN mkdir -p /var/tmp/rolf/checkouts
RUN mkdir -p /var/tmp/rolf/scripts
RUN /ve/bin/flake8 /app/rolf/ --max-complexity=10
RUN /ve/bin/python manage.py test
EXPOSE 8000
ADD docker-run.sh /run.sh
CMD ["/run.sh"]
