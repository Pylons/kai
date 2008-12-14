"""Setup the kai application"""
import logging

from couchdb.design import ViewDefinition
import pylons

from kai.config.environment import load_environment
from kai.model import Article, Documentation, Human, Paste, Rating

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup kai here"""
    load_environment(conf.global_conf, conf.local_conf)
    server = pylons.config['kai.server']
    db = pylons.config['kai.db']
    ViewDefinition.sync_many(db, [
        Article.all_months, Article.all_tags, Article.by_month,
        Article.by_tag, Article.by_time, Article.by_slug,
        
        Documentation.by_path, Documentation.ids_for_version,
        Documentation.doc_key,
        
        Human.by_displayname, Human.by_email, Human.by_email_token,
        Human.by_openid, Human.by_password_token,
        
        Rating.all_raters,
    ])
    
    
    # admin = Human(name="Admin")
    # admin.store(db)
    # joe = Human(name="Joe")
    # joe.store(db)
    # fred = Human(name="Fred Smith", username="fsmith")
    # fred.store(db)
    # 
    # sample = Paste(human_id=joe.id, title="Sample 1", code="This is a sample", language="text")
    # sample.store(db)
    # sample2 = Paste(human_id=admin.id, title="Sample 2", code="Another sample", lanugage="text")
    # sample2.store(db)
