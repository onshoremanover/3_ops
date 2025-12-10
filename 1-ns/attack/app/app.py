from flask import Flask, render_template, send_file
from datetime import datetime, timedelta
import re
import os
import io
import imgkit
import base64
from collections import Counter
import geoip2.database

app = Flask(__name__)
GEOIP_DB = "/app/GeoLite2-Country.mmdb"
LOG_FILE = "/fail2ban-logs/fail2ban.log"
FLAGS_FOLDER = "static/flags"

@app.route('/')
def index():
    stats = get_fail2ban_stats()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    return render_template('index.html', stats=stats, updated=timestamp)

@app.route('/screenshot.png')
def screenshot():
    html = render_template('index.html', stats=get_fail2ban_stats(), updated=datetime.now().strftime('%Y-%m-%d %H:%M'))

    options = {
        'format': 'png',
        'width': 540,
        'height': 960,
        'encoding': "UTF-8",
        'quiet': ''
    }

    img = imgkit.from_string(html, False, options=options)

    return send_file(
        io.BytesIO(img),
        mimetype='image/png',
        as_attachment=False,
        download_name='fail2ban-latest.png'
    )

def get_fail2ban_stats():
    now = datetime.now()
    cutoff = now - timedelta(days=1)
    ip_list = []

    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+.*Ban ([\d\.]+)', line)
                if match:
                    timestamp = datetime.strptime(match.group(1), '%Y-%m-%d %H:%M:%S')
                    if timestamp > cutoff:
                        ip_list.append(match.group(2))
    except Exception as e:
        return {"total_attempts": 0, "by_country": [("Error", str(e))]}

    ip_counter = Counter(ip_list)
    country_counter = {}

    reader = geoip2.database.Reader(GEOIP_DB)
    for ip in ip_counter:
        try:
            country_info = reader.country(ip)
            country_name = country_info.country.name
            country_code = country_info.country.iso_code.lower()

            # Load and encode flag as base64
            flag_path = os.path.join(FLAGS_FOLDER, f"{country_code}.png")
            if os.path.exists(flag_path):
                with open(flag_path, "rb") as f:
                    flag_base64 = base64.b64encode(f.read()).decode('utf-8')
                flag_data = f"data:image/png;base64,{flag_base64}"
            else:
                flag_data = None

        except Exception:
            country_name = "Unknown"
            flag_data = None

        country_counter[country_name] = (flag_data, ip_counter[ip])

    return {
        "total_attempts": sum(ip_counter.values()),
        "by_country": sorted(country_counter.items(), key=lambda x: x[1][1], reverse=True)
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
