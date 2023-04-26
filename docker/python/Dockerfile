FROM python:3.9
#
# Packages by module
#
RUN python -m pip install termcolor mysql-connector-python bs4 python-dotenv requests lru_cache
WORKDIR /tmp
# 
# Persistance
#
ADD shell.sh /usr/local/bin/shell.sh
RUN chmod 777 /usr/local/bin/shell.sh
CMD /usr/local/bin/shell.sh