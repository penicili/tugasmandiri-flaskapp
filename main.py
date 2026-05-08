import logging
import waitress
from app import create_app
# Entry point aplikasi, jalankan WSGI dengan waitress
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # aktifkan request log dari waitress
    logging.getLogger('waitress').setLevel(logging.DEBUG)
    logging.getLogger('waitress.queue').setLevel(logging.DEBUG)
    app = create_app()
    waitress.serve(app, host='0.0.0.0', port=5000)
