from flask import Flask, request, Response
from curl_cffi import requests # Import ini, bukan requests biasa

app = Flask(__name__)

@app.route('/bypass')
def bypass():
    image_url = request.args.get('url')
    if not image_url:
        return "URL required", 400

    try:
        # 'impersonate' akan membuat request terlihat 100% seperti Chrome asli
        resp = requests.get(
            image_url,
            impersonate="chrome124", 
            headers={
                "referer": "https://animein.net",
                "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            },
            cookies={"cf_clearance": "4SwZkWEjpM09frsx2Fz8BHzL5lyvrEclBxyvclIb_yg-1778463116-1.2.1.1-k_rkwkEIJe4bn1xVV7iZpRORX1sdif7TYwtVp8pl8IgoZJxj20liPGIaiWxWH4GgtHRAGi7cunbvW8H35wAXLT7nYSJ6sxB8pSBujAc7edcSVhCo0spJZcgkkv9K7NpRJQzV3lZopysuADJW0n636edLgTiRUaHrSadhrerwZUEUObTdkwIZssZPWP_uGpeNalZHIIIhexCS8xvaHC6CWChQpbJZVEzupaCjpNbLb0J1JqTjMCYRtdOuYtMNOqjHcZIGWiOLiYzbStl7mG08l7L6RpI2gUtbbU4RI_EgVd5HLttgPqx.WZPUMwnZo2oN9teGfo0OKf7skgbOYhLvvAyour_cf_clearance_cookie_value_here"}
        )

        # Cek apakah isinya benar-benar gambar atau malah HTML blokir
        if "text/html" in resp.headers.get("Content-Type", ""):
            return "Masih kena blokir Cloudflare (HTML received)", 403

        return Response(resp.content, mimetype=resp.headers.get("Content-Type"))
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(port=6060)
