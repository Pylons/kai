"""Setup the kai application"""
import logging

import pylons

from kai.config.environment import load_environment
from kai.model import Human, Paste

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup kai here"""
    load_environment(conf.global_conf, conf.local_conf)
    server = pylons.config['kai.server']
    db = pylons.config['kai.db']
    admin = Human(name="Admin")
    admin.store(db)
    joe = Human(name="Joe")
    joe.store(db)
    fred = Human(name="Fred Smith", username="fsmith")
    fred.store(db)
    
    sample = Paste(human_id=joe.id, title="Sample 1", code="This is a sample", language="text")
    sample.store(db)
    sample2 = Paste(human_id=admin.id, title="Sample 2", code="Another sample", lanugage="text")
    sample2.store(db)
