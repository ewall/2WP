# WordPress 3.0 database model
#   for SQLAlchemy w/ Elixir
# reference http://codex.wordpress.org/Database_Description

from elixir import *
from sqlalchemy.dialects.mysql import *

metadata.bind = "sqlite:///:memory:"
metadata.bind.echo = True

class User(Entity):
    using_options(tablename='wp_users')

    ID =                    Field(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)
    user_login =            Field(VARCHAR(60))
    user_pass =             Field(VARCHAR(64))
    user_nicename =         Field(VARCHAR(50))
    user_email =            Field(VARCHAR(100))
    user_url =              Field(VARCHAR(100))
    user_registered =       Field(DATETIME)
    user_activation_key =   Field(VARCHAR(60))
    user_status =           Field(INT(11))
    display_name =          Field(VARCHAR(250))

    posts = OneToMany('Post')

    def __repr__(self):
        return "<User '%s'| '%s' | '%s'>" % (self.user_login, self.user_nicename, self.user_email)

class Post(Entity):
    using_options(tablename='wp_posts')

    ID =                    Field(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)
    post_author =           ManyToOne('User')
    post_date =             Field(DATETIME)
    post_date_gmt =         Field(DATETIME)
    post_content =          Field(LONGTEXT)
    post_title =            Field(TEXT)
    post_excerpt =          Field(TEXT)
    post_status =           Field(VARCHAR(20), default="publish")
    comment_status =        Field(VARCHAR(20), default="open")
    ping_status =           Field(VARCHAR(20), default="open")
    post_password =         Field(VARCHAR(20))
    post_name =             Field(VARCHAR(200))
    to_ping =               Field(TEXT)
    pinged =                Field(TEXT)
    post_modified =         Field(DATETIME)
    post_modified_gmt =     Field(DATETIME)
    post_content_filtered = Field(TEXT)
    post_parent =           ManyToOne('Post') #???
    guid =                  Field(VARCHAR(255))
    menu_order =            Field(INT(11), default=0)
    post_type =             Field(VARCHAR(20), default="post")
    post_mime_type =        Field(VARCHAR(100))
    comment_count =         Field(BIGINT(20, unsigned=True), default=0)

    def __repr__(self):
        return "<Post '%s'>" % self.post_title

class Comment(Entity):
    using_options(tablename='wp_comments')

    comment_ID =            Field(BIGINT(20, unsigned=True), primary_key=True, autoincrement=True)
    comment_post_ID =       OneToMany('Post')
    comment_author =        Field(TINYTEXT)
    comment_author_email =  Field(VARCHAR(100))
    comment_author_url =    Field(VARCHAR(200))
    comment_author_IP =     Field(VARCHAR(100))
    comment_date =          Field(DATETIME)
    comment_date_gmt =      Field(DATETIME)
    
