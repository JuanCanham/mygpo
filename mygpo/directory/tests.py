import unittest
from unittest import mock
import uuid
from datetime import datetime

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.test import TestCase
from mygpo.data.feeddownloader import NoEpisodesException

from mygpo.podcasts.models import Podcast
from mygpo.directory.views import MissingPodcast, ToplistView


class ToplistTests(unittest.TestCase):
    """Test podcast and episode toplists"""

    def test_toplist_languages(self):
        """Test the all_languages method of the toplists"""
        languages = ["de", "de_AT", "en"]
        for lang in languages:
            Podcast.objects.create(
                id=uuid.uuid1(), created=datetime.utcnow(), language=lang
            )

        view = ToplistView()
        all_langs = view.all_languages()
        self.assertEqual(all_langs, {"de": "Deutsch", "en": "English"})

class MissingPodcastTests(TestCase):
    """Test adding Missing podcasts"""

    def request_podcast(self, url):
        """Generate a request and call MissingPodcasts.get"""
        factory = RequestFactory()
        request = factory.get(url)
        request.user = get_user_model()
        response = MissingPodcast().get(request)
        return response

    def test_cant_add_empty_url(self):
        """Test empty url is not addable"""

        response = self.request_podcast(None)

        self.assertNotContains(response, "Add Podcast")

    @mock.patch("mygpo.podcasts.models.PodcastManager.get")
    def test_cant_add_valid_podcast(self, mock_podcast_manager_get):
        """Test valid podcast is not addable"""
        mock_podcast_manager_get.return_value = Podcast.objects.create(
            id=uuid.uuid1(), created=datetime.utcnow(), link='https://mypodcast.com'
        )

        response = self.request_podcast('https://gpodder.net/missing?q=https://mypodcast.com')

        self.assertNotContains(response, "Add Podcast")

    @mock.patch("mygpo.data.feeddownloader.PodcastUpdater")
    @mock.patch("mygpo.podcasts.models.PodcastManager.get")
    def test_can_add_podcast_without_link(self, mock_podcast_manager_get, mock_podcast_updater):
        """Test valid podcast without a link is addable"""
        mock_podcast_manager_get.return_value = Podcast.objects.create(
            id=uuid.uuid1(), created=datetime.utcnow()
        )

        response = self.request_podcast('https://gpodder.net/missing?q=https://mypodcast.com')

        self.assertContains(response, "Add Podcast")
        mock_podcast_updater.assert_called_once()

    @mock.patch("mygpo.data.feeddownloader.PodcastUpdater")
    @mock.patch("mygpo.podcasts.models.PodcastManager.get")
    def test_can_add_non_existent_podcast(self, mock_podcast_manager_get, mock_podcast_updater):
        """Test non existent podcast is addable"""
        mock_podcast_manager_get.side_effect=Podcast.DoesNotExist

        response = self.request_podcast('https://gpodder.net/missing?q=https://mypodcast.com')

        self.assertContains(response, "Add Podcast")
        mock_podcast_updater.assert_called_once()

    @mock.patch("django.contrib.messages.error")
    @mock.patch("mygpo.data.feeddownloader.PodcastUpdater")
    @mock.patch("mygpo.podcasts.models.PodcastManager.get")
    def test_cant_add_invalid_podcast(self, mock_podcast_manager_get, mock_podcast_updater, _mock_messages):
        """Test invalid podcast is not addable"""
        mock_podcast_manager_get.return_value = Podcast.objects.create(
            id=uuid.uuid1(), created=datetime.utcnow(), link='https://mypodcast.com'
        )
        mock_podcast_updater.side_effect=NoEpisodesException

        response = self.request_podcast('https://gpodder.net/missing?q=https://mypodcast.com')

        self.assertNotContains(response, "Add Podcast")
