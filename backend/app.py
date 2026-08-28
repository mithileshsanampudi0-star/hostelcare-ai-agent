import os
from flask import Flask
from flask_cors import CORS
from config import FLASK_PORT
from routes.complaint_routes import complaint_bp
from routes.ticket_routes import ticket_bp
from routes.admin_routes import admin_bp
from agent.scheduler import start_scheduler

app = Flask(__name__)
CORS(app)

app.register_blueprint(complaint_bp)
app.register_blueprint(ticket_bp)
app.register_blueprint(admin_bp)


@app.route("/")
def health():
    return {"status": "HostelCare AI backend running"}


# Flask's debug reloader spawns a second process; only start the scheduler in the
# actual running process, not the reloader's parent watcher.
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
    start_scheduler()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=FLASK_PORT,
        debug=True
    )
