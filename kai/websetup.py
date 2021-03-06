"""Setup the kai application"""
import logging

from couchdb.design import ViewDefinition
import pylons
import pylons.test

from kai.config.environment import load_environment
from kai.model import Article, Comment, Documentation, Human, Paste, Rating, Snippet, Traceback
from kai.model.generics import all_doc_tags

log = logging.getLogger(__name__)

def sync_db(db):
    ViewDefinition.sync_many(db, [
        all_doc_tags,
        
        Article.all_months, Article.all_tags, Article.by_month,
        Article.by_tag, Article.by_time, Article.by_slug,
        
        Comment.by_time, Comment.comment_count, Comment.by_anytime,
        
        Documentation.by_path, Documentation.ids_for_version,
        Documentation.doc_key,
        
        Human.by_displayname, Human.by_email, Human.by_email_token,
        Human.by_openid, Human.by_password_token,
        
        Paste.by_author, Paste.by_tag, Paste.all_tags, Paste.by_time,
        Paste.by_old_id, Paste.by_tag_time, Paste.by_session_id,
        
        Rating.all_raters,
        
        Snippet.by_date, Snippet.by_author, Snippet.by_slug, Snippet.by_title,
        Snippet.by_author_id, Snippet.by_tag, Snippet.all_tags,
        Snippet.author_totals,
        
        Traceback.by_uuid, Traceback.by_time, Traceback.by_session_id,
    ])

def setup_app(command, conf, vars):
    """Place any commands to setup kai here"""
    # Don't reload the app if it was loaded under the testing environment
    if not pylons.test.pylonsapp:
        load_environment(conf.global_conf, conf.local_conf)
    
    server = pylons.config['kai.server']
    db = pylons.config['kai.db']
    sync_db(db)
