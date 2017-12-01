from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from moments.settings.base import EthanWarning

User = get_user_model()

class Moment(models.Model):
	author = models.ForeignKey(User, related_name='moments')
	image = models.ImageField(upload_to='uploads')
	caption = models.CharField(max_length=140, null=True)
	creation_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "<Moment by {}: {}>".format(self.author, self.caption)


class Like(models.Model):
	who = models.ForeignKey(User)
	moment = models.ForeignKey(Moment)
	effective = models.BooleanField(default=False)

	def __str__(self):
		return "<{} likes {}>".format(self.who, self.post)

	def like(self):
		self.effective = True
		self.save()

	def unlike(self):
		self.effective = False
		self.save()

	def toggle(self):
		self.effective = not self.effective
		self.save()


class Comment(models.Model):
	author = models.ForeignKey(User, related_name='comments')
	moment = models.ForeignKey(Moment, related_name='comments')
	content = models.CharField(max_length=140)
	creation_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "<Comment for {} by {}: {}>".format(self.moment, self.author, self.content)


@receiver(models.signals.post_save, sender=Like)
def like_on_create(sender, instance, created, *args, **kwargs):
	"""
	Function called when a Like models is created

	Argument explanation
	:param sender: the model class (Like)
	:param instance: the actual instance being saved
	:param created: boolean; True if a new record was created
	:param args, kwargs: Capture the unneeded `raw` and `using` arguments
	"""
	if created:
		instance.effective = True
		instance.save()

@receiver(models.signals.pre_save, sender=Like)
def like_before_create(sender, instance, raw, *args, **kwargs):
	if instance.id is None:
		duplicates = Like.objects.filter(who=instance.who, post=instance.post)
		if len(duplicates):
			raise EthanWarning("Somebody's attempting to like some post more than once!!")


@receiver(models.signals.post_save, sender=User)
def create_token(sender, instance, created, *args, **kwargs):
	if created:
		Token.objects.create(user=instance)