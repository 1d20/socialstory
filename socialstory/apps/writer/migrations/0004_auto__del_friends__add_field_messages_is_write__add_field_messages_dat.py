# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Friends'
        db.delete_table('writer_friends')

        # Adding field 'Messages.is_write'
        db.add_column('writer_messages', 'is_write',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Messages.date_add'
        db.add_column('writer_messages', 'date_add',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 2, 8, 0, 0), blank=True),
                      keep_default=False)

        # Deleting field 'Comments.lenght'
        db.delete_column('writer_comments', 'lenght')

        # Adding field 'Comments.length'
        db.add_column('writer_comments', 'length',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Friends'
        db.create_table('writer_friends', (
            ('user2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_friend_2', to=orm['auth.User'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_friend_1', to=orm['auth.User'])),
        ))
        db.send_create_signal('writer', ['Friends'])

        # Deleting field 'Messages.is_write'
        db.delete_column('writer_messages', 'is_write')

        # Deleting field 'Messages.date_add'
        db.delete_column('writer_messages', 'date_add')

        # Adding field 'Comments.lenght'
        db.add_column('writer_comments', 'lenght',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10),
                      keep_default=False)

        # Deleting field 'Comments.length'
        db.delete_column('writer_comments', 'length')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'stories.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'stories.language': {
            'Meta': {'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'stories.story': {
            'Meta': {'object_name': 'Story'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'story_subgenre'", 'symmetrical': 'False', 'to': "orm['stories.SubGenre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_language'", 'to': "orm['stories.Language']"}),
            'pages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'default': "'posters/default.jpg'", 'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'story': ('django.db.models.fields.files.FileField', [], {'default': "'stories/default.txt'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_user'", 'to': "orm['auth.User']"}),
            'voteCount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'stories.subgenre': {
            'Meta': {'object_name': 'SubGenre'},
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'genre_subgenre'", 'to': "orm['stories.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'writer.comments': {
            'Meta': {'object_name': 'Comments'},
            'color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_char': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'like_writer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paragraph_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_comment'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_comment'", 'to': "orm['auth.User']"})
        },
        'writer.messages': {
            'Meta': {'object_name': 'Messages'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_write': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_message_from'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_message_to'", 'to': "orm['auth.User']"})
        },
        'writer.setting': {
            'Meta': {'object_name': 'Setting'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'writer.settingvalue': {
            'Meta': {'object_name': 'SettingValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'setting_settingvalue'", 'to': "orm['writer.Setting']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'writer.usersettings': {
            'Meta': {'object_name': 'UserSettings'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'settingvalue_usersetting'", 'to': "orm['writer.SettingValue']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_usersetting'", 'to': "orm['auth.User']"})
        },
        'writer.writer': {
            'Meta': {'object_name': 'Writer'},
            'biography': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'default': "'user_pictures/default.jpg'", 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '65'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'writer.writerfavorite': {
            'Meta': {'object_name': 'WriterFavorite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_favorite'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer_favorite'", 'to': "orm['auth.User']"})
        },
        'writer.writerread': {
            'Meta': {'object_name': 'WriterRead'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_read'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer_read'", 'to': "orm['auth.User']"})
        },
        'writer.writervote': {
            'Meta': {'object_name': 'WriterVote'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_vote'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer_vote'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['writer']