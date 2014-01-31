# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Story', fields ['user', 'title']
        db.delete_unique('stories_story', ['user_id', 'title'])

        # Adding model 'StoryGenre'
        db.create_table('stories_storygenre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('setting', self.gf('django.db.models.fields.related.ForeignKey')(related_name='storygenre_story', to=orm['stories.Story'])),
            ('subgenre', self.gf('django.db.models.fields.related.ForeignKey')(related_name='storygenre_subgenre', to=orm['stories.SubGenre'])),
        ))
        db.send_create_signal('stories', ['StoryGenre'])

        # Adding model 'SubGenre'
        db.create_table('stories_subgenre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('genre', self.gf('django.db.models.fields.related.ForeignKey')(related_name='genre_subgenre', to=orm['stories.Genre'])),
        ))
        db.send_create_signal('stories', ['SubGenre'])

        # Adding model 'Versions'
        db.create_table('stories_versions', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='story_version', to=orm['stories.Story'])),
            ('path', self.gf('django.db.models.fields.files.FileField')(default='default', max_length=100)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('stories', ['Versions'])

        # Adding model 'SimilarStory'
        db.create_table('stories_similarstory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_story_1', to=orm['stories.Story'])),
            ('story2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='similar_story_2', to=orm['stories.Story'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=10)),
        ))
        db.send_create_signal('stories', ['SimilarStory'])

        # Adding model 'Language'
        db.create_table('stories_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('stories', ['Language'])

        # Adding model 'Genre'
        db.create_table('stories_genre', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('stories', ['Genre'])

        # Deleting field 'Story.genge'
        db.delete_column('stories_story', 'genge')


        # Renaming column for 'Story.language' to match new field type.
        db.rename_column('stories_story', 'language', 'language_id')
        # Changing field 'Story.language'
        db.alter_column('stories_story', 'language_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['stories.Language']))
        # Adding index on 'Story', fields ['language']
        db.create_index('stories_story', ['language_id'])


    def backwards(self, orm):
        # Removing index on 'Story', fields ['language']
        db.delete_index('stories_story', ['language_id'])

        # Deleting model 'StoryGenre'
        db.delete_table('stories_storygenre')

        # Deleting model 'SubGenre'
        db.delete_table('stories_subgenre')

        # Deleting model 'Versions'
        db.delete_table('stories_versions')

        # Deleting model 'SimilarStory'
        db.delete_table('stories_similarstory')

        # Deleting model 'Language'
        db.delete_table('stories_language')

        # Deleting model 'Genre'
        db.delete_table('stories_genre')

        # Adding field 'Story.genge'
        db.add_column('stories_story', 'genge',
                      self.gf('django.db.models.fields.IntegerField')(default=1, max_length=2),
                      keep_default=False)


        # Renaming column for 'Story.language' to match new field type.
        db.rename_column('stories_story', 'language_id', 'language')
        # Changing field 'Story.language'
        db.alter_column('stories_story', 'language', self.gf('django.db.models.fields.IntegerField')(max_length=2))
        # Adding unique constraint on 'Story', fields ['user', 'title']
        db.create_unique('stories_story', ['user_id', 'title'])


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
            'description': ('django.db.models.fields.TextField', [], {}),
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
        'stories.storygenre': {
            'Meta': {'object_name': 'StoryGenre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'setting': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storygenre_story'", 'to': "orm['stories.Story']"}),
            'subgenre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'storygenre_subgenre'", 'to': "orm['stories.SubGenre']"})
        },
        'stories.subgenre': {
            'Meta': {'object_name': 'SubGenre'},
            'genre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'genre_subgenre'", 'to': "orm['stories.Genre']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'stories.versions': {
            'Meta': {'object_name': 'Versions'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.files.FileField', [], {'default': "'default'", 'max_length': '100'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'story_version'", 'to': "orm['stories.Story']"})
        }
    }

    complete_apps = ['stories']