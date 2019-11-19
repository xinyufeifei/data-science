FROM python:3.7-alpine

# Install necessry software
RUN apk add --no-cache --virtual .build-deps gcc g++ python3-dev musl-dev linux-headers freetype-dev

RUN mkdir supergirl
COPY requirements.txt /supergirl
COPY notebooks /supergirl/notebooks
WORKDIR /supergirl

# Install Python dependencies
RUN pip install -r requirements.txt
CMD ["papermill", "notebooks/us_unemployment_rate_map/visualize_unemployment_rate_plotly.ipynb", "notebooks/output/out.ipynb"]
