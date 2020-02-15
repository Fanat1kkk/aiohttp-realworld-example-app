from tortoise.contrib import test
from authentication.models import User
from profiles.models import Profile


class TestModels(test.TestCase):
    async def setUp(self):
        self.user = await User.create(username='username', email='email', password='password')

    async def test_user_and_profile(self):
        assert await User.all().count() == 1

        profile = await Profile(user=self.user)
        await profile.save()

        assert profile.user == self.user
        assert await Profile.all().count() == 1
