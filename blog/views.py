from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Post, Profile
from .forms import CommentForm, UpdateUserForm, UpdateProfileForm, PostForm


""" Listview """
class PostList(ListView):
    model = Post()
    queryset = Post.objects.filter(status=1).order_by('likes')
    template_name = 'index.html'
    paginate_by = 6


""" Listview (drafts) """
class DraftList(ListView):
    model = Post()
    queryset = Post.objects.filter(status=0).order_by('created_on')
    template_name = 'post_draft.html'
    context_object_name = 'object_list'
    paginate_by = 6


""" Createview """
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


""" Updateview """
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = '_update_form'
    


""" Deleteview """
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')


@login_required
def delete_post(request, slug):
    """ Delete a blog post """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only blog admins can do that.')
        return redirect(reverse('home'))

    post = get_object_or_404(Post, slug=slug)
    post.delete()
    messages.success(request, 'Post deleted!')
    return redirect(reverse('home'))


""" Detailview """
class PostDetail(DetailView):

    template_name = 'post.html'

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        disliked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if post.likes.filter(id=self.request.user.id).exists():
            disliked = True

        return render (
            request, 'post.html', 
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'disliked': disliked,
                'comment_form': CommentForm(),
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        disliked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if post.dislikes.filter(id=self.request.user.id).exists():
            disliked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else: 
            comment_form = CommentForm()

        return render (
            request, 'post.html', 
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'comment_form': CommentForm(),
            },
        )


class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        # if post.dislikes.filter(id=request.user.id).exists():
        #     post.dislikes.remove(request.user)
        # else:
        #     post.dislikes.add(request.user)

        return HttpResponseRedirect(reverse('post', args=[slug]))

class PostDisike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        # if post.likes.filter(id=request.user.id).exists():
        #     post.likes.remove(request.user)
        # else:
        #     post.likes.add(request.user)

        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)

        return HttpResponseRedirect(reverse('post', args=[slug]))


@login_required
def profile(request):

    user_profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)


    context = {
        'user_profile': user_profile,
        'user_form': user_form, 
        'profile_form': profile_form
    }

    return render(request, 'profile.html', context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')
