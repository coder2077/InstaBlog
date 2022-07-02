from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Post



class PostDetailsView(DetailView):
	model = Post
	template_name = 'blog/post_details.html'

	def get_object(self):
		return Post.objects.get(pk=self.kwargs.get('pk'))


	def post(self, request, pk):
		post = Post.objects.get(pk=pk)
		
		if request.POST['action'] == 'comment':
			if request.POST['comment'] != '':
				if request.user.is_authenticated:
					post.comments.create(
						author=request.user,
						body=request.POST['comment']
					)
					messages.success(request, 'Comment added successfully')
				else:
					messages.error(request, 'You must be logged in to comment')
			else:
				messages.error(request, 'Comment cannot be empty')

			return redirect('post_details', pk=pk)

		elif request.POST['action'] == 'like':
			if request.user.is_authenticated:
				if request.user in post.likes.all():
					post.likes.remove(request.user)
					messages.success(request, 'Like removed successfully')
				else:
					post.likes.add(request.user)
					messages.success(request, 'Like added successfully')
			else:
				messages.error(request, 'You must be logged in to like')

			return redirect('post_details', pk=pk)

		elif request.POST['action'] == 'save':
			if request.user in post.saved.all():
				post.saved.remove(request.user)
				messages.success(request, 'Post removed from saved posts')
			else:
				if request.user.is_authenticated:
					post.saved.add(request.user)
					messages.success(request, 'Post saved')
				else:
					messages.error(request, 'You must be logged in to save posts')
			
			return redirect('post_details', pk=pk)


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	template_name = 'blog/delete_post.html'
	success_url = reverse_lazy('home')
	login_url = '/auth/signup/'

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	template_name = 'blog/update_post.html'
	fields = ('photo', 'body')
	login_url = '/auth/signup/'

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class CreatePostView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'blog/create_post.html'
	fields = ('photo', 'body')
	login_url = '/auth/signup/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class HomePageView(ListView):
	model = Post
	template_name = 'home.html'

	def post(self, request):
		if request.POST['action'].startswith('comment'):
			pk = request.POST['action'].replace('comment_', '')
			post = Post.objects.get(pk=pk)
			if request.POST['comment'] != '':
				if request.user.is_authenticated:
					post.comments.create(
						author=request.user,
						body=request.POST['comment']
					)
					messages.success(request, 'Comment added successfully')
				else:
					messages.error(request, 'You must be logged in to comment')
			else:
				messages.error(request, 'Comment cannot be empty')

			return redirect('post_details', pk=pk)

		elif request.POST['action'].startswith('like'):
			pk = request.POST['action'].replace('like_', '')
			post = Post.objects.get(pk=pk)

			if request.user.is_authenticated:
				if request.user in post.likes.all():
					post.likes.remove(request.user)
					messages.success(request, 'Like removed successfully')
				else:
					post.likes.add(request.user)
					messages.success(request, 'Like added successfully')
			else:
				messages.error(request, 'You must be logged in to like')

			return redirect('home')

		elif request.POST['action'].startswith('save'):
			pk = request.POST['action'].replace('save_', '')
			post = Post.objects.get(pk=pk)

			if request.user in post.saved.all():
				post.saved.remove(request.user)
				messages.success(request, 'Post removed from saved posts')
			else:
				if request.user.is_authenticated:
					post.saved.add(request.user)
					messages.success(request, 'Post saved')				
				else:
					messages.error(request, 'You must be logged in to save posts')
			
			return redirect('home')


def error_404(request, exception):
	return render(request,'error/404.html')

		
def error_403(request, exception):
	return render(request,'error/403.html')

