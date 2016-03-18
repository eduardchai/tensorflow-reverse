FROM salestock/python-tensorflow

COPY data_dir /usr/src/app/data_dir
COPY train_dir /usr/src/app/train_dir

CMD [ "gunicorn", "-c", "gunicorn.py", "application:app" ]

EXPOSE 9012
