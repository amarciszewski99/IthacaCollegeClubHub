from application import application
from application.models import Member


@application.shell_context_processor
def make_shell_context():
    return {'db': db, 'Member': Member}