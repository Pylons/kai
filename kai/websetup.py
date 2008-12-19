"""Setup the kai application"""
import logging

from couchdb.design import ViewDefinition
import pylons

from kai.config.environment import load_environment
from kai.model import Article, Comment, Documentation, Human, Paste, Rating, Snippet, Traceback

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup kai here"""
    load_environment(conf.global_conf, conf.local_conf)
    server = pylons.config['kai.server']
    db = pylons.config['kai.db']
    ViewDefinition.sync_many(db, [
        Article.all_months, Article.all_tags, Article.by_month,
        Article.by_tag, Article.by_time, Article.by_slug,
        
        Comment.by_time, Comment.comment_count,
        
        Documentation.by_path, Documentation.ids_for_version,
        Documentation.doc_key,
        
        Human.by_displayname, Human.by_email, Human.by_email_token,
        Human.by_openid, Human.by_password_token,
        
        Paste.by_author, Paste.by_tag, Paste.all_tags, Paste.by_time,
        
        Rating.all_raters,
        
        Snippet.by_date, Snippet.by_author, Snippet.by_slug, Snippet.by_title,
        Snippet.by_author_id, Snippet.by_tag, Snippet.all_tags,
        Snippet.author_totals,
        
        Traceback.by_uuid, Traceback.by_time, Traceback.by_session_id,
    ])
