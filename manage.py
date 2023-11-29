from app import app, db
from app.model.models import IntrusionEvent

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'IntrusionEvent': IntrusionEvent}

if __name__ == '__main__':
    app.run(debug=True)
