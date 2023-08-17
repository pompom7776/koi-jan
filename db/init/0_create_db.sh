sudo -i -u postgres psql -l | grep koijan; \
if [ $? -ne 0 ]; then \
  sudo -i -u postgres psql -c "
    CREATE DATABASE koijan
      WITH OWNER postgres"
          ENCODING = 'UTF8'
          LC_COLLATE = 'ja_JP.UTF-8'
          LC_CTYPE = 'ja_JP.UTF-8'
  "; \
fi

for sql_file in ./*.sql; do
  if [ -f "$sql_file" ]; then
    sudo -i -u postgres psql -d koijan -f "$sql_file"
  fi
done
