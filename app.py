from app import app
from app.models import Member


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Member': Member}