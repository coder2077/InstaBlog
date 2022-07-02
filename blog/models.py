from django.db import models
from django.urls import reverse



class Post(models.Model):
	author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	photo = models.ImageField(upload_to='images/', null=False, blank=False)
	body = models.TextField()
	date_posted = models.DateTimeField(auto_now_add=True)
	likes = models.ManyToManyField('accounts.CustomUser', blank=True, related_name='likes')
	saved = models.ManyToManyField('accounts.CustomUser', blank=True, related_name='saved')
	comments = models.ManyToManyField('blog.Comment', blank=True, related_name='comments')

	def __str__(self):
		if len(self.body) > 50:
			return self.body[:50] + '...'
		
		else:
			return self.body

	def get_absolute_url(self):
		return reverse('post_details', args=[str(self.pk)])


class Comment(models.Model):
	author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	body = models.TextField()
	date_posted = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		if len(self.body) > 50:
			return self.body[:50] + '...'
		
		else:
			return self.body

