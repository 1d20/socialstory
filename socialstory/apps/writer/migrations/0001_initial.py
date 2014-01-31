# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Writer'
        db.create_table('writer_writer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_writer', to=orm['auth.User'])),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(default='user_pictures/default.jpg', max_length=100)),
            ('status', self.gf('django.db.models.fields.CharField')(default='', max_length=65)),
            ('biography', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('writer', ['Writer'])

        # Adding unique constraint on 'Writer', fields ['user', 'date_add']
        db.create_unique('writer_writer', ['user_id', 'date_add'])

        # Adding model 'WriterVote'
        db.create_table('writer_writervote', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='writer_vote', to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='story_vote', to=orm['stories.Story'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('writer', ['WriterVote'])

        # Adding unique constraint on 'WriterVote', fields ['user', 'story']
        db.create_unique('writer_writervote', ['user_id', 'story_id'])

        # Adding model 'WriterFavorite'
        db.create_table('writer_writerfavorite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='writer_favorite', to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='story_favorite', to=orm['stories.Story'])),
        ))
        db.send_create_signal('writer', ['WriterFavorite'])

        # Adding unique constraint on 'WriterFavorite', fields ['user', 'story']
        db.create_unique('writer_writerfavorite', ['user_id', 'story_id'])

        # Adding model 'WriterRead'
        db.create_table('writer_writerread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='writer_read', to=orm['auth.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='story_read', to=orm['stories.Story'])),
        ))
        db.send_create_signal('writer', ['WriterRead'])

        # Adding unique constraint on 'WriterRead', fields ['user', 'story']
        db.create_unique('writer_writerread', ['user_id', 'story_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'WriterRead', fields ['user', 'story']
        db.delete_unique('writer_writerread', ['user_id', 'story_id'])

        # Removing unique constraint on 'WriterFavorite', fields ['user', 'story']
        db.delete_unique('writer_writerfavorite', ['user_id', 'story_id'])

        # Removing unique constraint on 'WriterVote', fields ['user', 'story']
        db.delete_unique('writer_writervote', ['user_id', 'story_id'])

        # Removing unique constraint on 'Writer', fields ['user', 'date_add']
        db.delete_unique('writer_writer', ['user_id', 'date_add'])

        # Deleting model 'Writer'
        db.delete_table('writer_writer')

        # Deleting model 'WriterVote'
        db.delete_table('writer_writervote')

        # Deleting model 'WriterFavorite'
        db.delete_table('writer_writerfavorite')

        # Deleting model 'WriterRead'
        db.delete_table('writer_writerread')


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
        'stories.story': {
            'Meta': {'unique_together': "(('user', 'title'),)", 'object_name': 'Story'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'genge': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'pages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'default': "'posters/default.jpg'", 'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'story': ('django.db.models.fields.files.FileField', [], {'default': "'stories/default.txt'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_user'", 'to': "orm['auth.User']"}),
            'voteCount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'writer.writer': {
            'Meta': {'unique_together': "(('user', 'date_add'),)", 'object_name': 'Writer'},
            'biography': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'default': "'user_pictures/default.jpg'", 'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '65'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_writer'", 'to': "orm['auth.User']"})
        },
        'writer.writerfavorite': {
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'WriterFavorite'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_favorite'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer_favorite'", 'to': "orm['auth.User']"})
        },
        'writer.writerread': {
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'WriterRead'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_read'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer_read'", 'to': "orm['auth.User']"})
        },
        'writer.writervote': {
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'WriterVote'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_vote'", 'to': "orm['stories.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'writer_vote'", 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['writer']