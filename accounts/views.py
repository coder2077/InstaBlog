from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from blog.models import Post



def userSavedPostsListView(request):
	posts = Post.objects.filter(saved__username=request.user.username)
	context = {'posts': posts}

	if request.method == "GET":
		if request.user.is_authenticated:
			return render(request, 'account/saved_posts.html', context)
		else:
			return redirect('login')
	
	elif request.method == "POST":
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

			return redirect('saved_posts')

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
			
			return redirect('saved_posts')

	elif request.method == "POST":
		post = Post.objects.get(pk=request.POST['post_id'])

		if request.user in post.saved.all():
			post.saved.remove(request.user)
			messages.success(request, 'Post removed from saved posts')
		else:
			if request.user.is_authenticated:
				post.saved.add(request.user)
				messages.success(request, 'Post saved')
			else:
				messages.error(request, 'You must be logged in to save posts')

		return redirect('saved_posts')

	return redirect('saved_posts')


def userPostsListView(request, username):
	user = get_object_or_404(CustomUser, username=username)
	posts = Post.objects.filter(author=user)
	context = {'posts': posts, 'user_model': user}

	if request.method == "GET":
		return render(request, 'account/user_posts.html', context)

	elif request.method == "POST":
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

			return redirect('user_posts', username=username)

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
			
			return redirect('user_posts', username=username)


@login_required(login_url='/auth/login/')
def userProfileEditView(request):
	if request.method == 'POST':
		form = CustomUserChangeForm(request.POST, instance=request.user, files=request.FILES)
		if form.is_valid():
			form.save()
			return redirect('profile', username=request.user.username)
	else:
		form = CustomUserChangeForm(instance=request.user)

	return render(request, 'account/edit_profile.html', {'form': form, 'user': request.user})


def userProfileView(request, username):
	user = get_object_or_404(CustomUser, username=username)
	posts_count = Post.objects.filter(author=user).count()

	return render(request, 'account/profile.html', {'user_model': user, 'posts_count': posts_count})


class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	template_name = 'registration/signup.html'
	
	def form_valid(self, form):
		form.save()
		username = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password1')
		user = authenticate(username=username, password=password)
		login(self.request, user)
		return redirect('home')

