# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BranchRequests'
        db.create_table('stories_branchrequests', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branchrequest_branch', to=orm['stories.Story'])),
            ('request_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='branchrequest_user', to=orm['auth.User'])),
            ('comment_message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('stories', ['BranchRequests'])

        # Deleting field 'Story.description'
        db.delete_column('stories_story', 'description')

        # Deleting field 'Story.poster'
        db.delete_column('stories_story', 'poster')

        # Deleting field 'Story.language'
        db.delete_column('stories_story', 'language_id')

        # Deleting field 'Story.title'
        db.delete_column('stories_story', 'title')

        # Deleting field 'Story.pages'
        db.delete_column('stories_story', 'pages')

        # Adding field 'Branch.language'
        db.add_column('stories_branch', 'language',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='branch_language', to=orm['stories.Language']),
                      keep_default=False)

        # Adding field 'Branch.poster'
        db.add_column('stories_branch', 'poster',
                      self.gf('django.db.models.fields.files.ImageField')(default='posters/default.jpg', max_length=100),
                      keep_default=False)

        # Adding field 'Branch.description'
        db.add_column('stories_branch', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'BranchRequests'
        db.delete_table('stories_branchrequests')

        # Adding field 'Story.description'
        db.add_column('stories_story', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Story.poster'
        db.add_column('stories_story', 'poster',
                      self.gf('django.db.models.fields.files.ImageField')(default='posters/default.jpg', max_length=100),
                      keep_default=False)

        # Adding field 'Story.language'
        db.add_column('stories_story', 'language',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='story_language', to=orm['stories.Language']),
                      keep_default=False)

        # Adding field 'Story.title'
        db.add_column('stories_story', 'title',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Adding field 'Story.pages'
        db.add_column('stories_story', 'pages',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Deleting field 'Branch.language'
        db.delete_column('stories_branch', 'language_id')

        # Deleting field 'Branch.poster'
        db.delete_column('stories_branch', 'poster')

        # Deleting field 'Branch.description'
        db.delete_column('stories_branch', 'description')


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
        'stories.branch': {
            'Meta': {'object_name': 'Branch'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branch_language'", 'to': "orm['stories.Language']"}),
            'poster': ('django.db.models.fields.files.ImageField', [], {'default': "'posters/default.jpg'", 'max_length': '100'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_version'", 'to': "orm['stories.Story']"}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_version'", 'to': "orm['auth.User']"})
        },
        'stories.branchrequests': {
            'Meta': {'object_name': 'BranchRequests'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchrequest_branch'", 'to': "orm['stories.Story']"}),
            'comment_message': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'branchrequest_user'", 'to': "orm['auth.User']"})
        },
        'stories.commit': {
            'Meta': {'object_name': 'Commit'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commit_branch'", 'to': "orm['stories.Branch']"}),
            'code': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'}),
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
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
        'stories.similarstory': {
            'Meta': {'object_name': 'SimilarStory'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'story1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_story_1'", 'to': "orm['stories.Story']"}),
            'story2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'similar_story_2'", 'to': "orm['stories.Story']"})
        },
        'stories.story': {
            'Meta': {'object_name': 'Story'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'genres': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'story_subgenre'", 'symmetrical': 'False', 'to': "orm['stories.SubGenre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_user'", 'to': "orm['auth.User']"}),
            'voteCount': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'stories.subgenre': {
            'Meta': {'object_name': 'SubGenre'},
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'genre_subgenre'", 'to': "orm['stories.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['stories']