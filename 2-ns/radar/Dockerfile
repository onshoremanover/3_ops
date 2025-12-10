FROM nginx:alpine
RUN apk add --no-cache curl unzip

WORKDIR /usr/share/nginx/html

# Grab v0.9.2 testing build and put it under /scope
RUN rm -rf ./* \
  && mkdir -p scope \
  && curl -L \
       "https://github.com/dustsignal/adsb-radarscope/archive/refs/tags/v1.zip" \
       -o /tmp/adsb-radarscope.zip \
  && unzip /tmp/adsb-radarscope.zip -d /tmp \
  && mv /tmp/adsb-radarscope-1/testing/v0.9.2.0837110925/* scope/ \
  && rm -rf /tmp/adsb-radarscope*

# 🔧 Set your Veenendaal home position and data paths
RUN set -x \
  && sed -i "s|DEFAULT_TAR1090_URL: .*|DEFAULT_TAR1090_URL: 'https://radar.peluan.com/data/aircraft.json',|" scope/config.js \
  && sed -i "s|DEFAULT_HOME_LAT: .*|DEFAULT_HOME_LAT: 52.0286,|" scope/config.js \
  && sed -i "s|DEFAULT_HOME_LON: .*|DEFAULT_HOME_LON: 5.5589,|" scope/config.js \
  && sed -i "s|DEFAULT_RANGE_NM: .*|DEFAULT_RANGE_NM: 60,|" scope/config.js \
  && sed -i "s|AIRPORTS: .*|AIRPORTS: '/scope/data/airports.csv',|" scope/config.js \
  && sed -i "s|NAVAIDS: .*|NAVAIDS: '/scope/data/navaids.csv',|" scope/config.js \
  && sed -i "s|RUNWAYS: .*|RUNWAYS: '/scope/data/runways.csv',|" scope/config.js
