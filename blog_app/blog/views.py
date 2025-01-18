from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post,Vote 
from blog_app.forms import ContactForm
from django.contrib import messages
from users.models import Complaint
from django.utils import timezone
from django.db.models import Q,Exists, OuterRef


# Create your views here.

def home(request):
    context = {
        'posts' : Post.objects.all(),
        'title' : 'home',
    }
    return render(request,'blog/home.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                user_upvoted=Exists(
                    Vote.objects.filter(
                        post=OuterRef('pk'),
                        user=self.request.user,
                        vote_type='upvote'
                    )
                ),
                user_downvoted=Exists(
                    Vote.objects.filter(
                        post=OuterRef('pk'),
                        user=self.request.user,
                        vote_type='downvote'
                    )
                )
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        posts = context['posts']

        # Add user voting data to each post
        if user.is_authenticated:
            for post in posts:
                post.user_upvoted = post.voters.filter(
                    vote__vote_type='upvote', id=user.id
                ).exists()
                post.user_downvoted = post.voters.filter(
                    vote__vote_type='downvote', id=user.id
                ).exists()
        else:
            for post in posts:
                post.user_upvoted = False
                post.user_downvoted = False

        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        profile = request.user.profile  # Access the authenticated user's profile

        if not profile.viewed_posts.filter(pk=post.pk).exists():
            post.view_count += 1
            post.save(update_fields=['view_count'])
            profile.viewed_posts.add(post)  # Mark the post as viewed by this user

        return super().get(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

def about(request):
    context = {

        'title': 'About',  # Set the title dynamically

        # Add other context variables as needed

    }
    return render(request,'blog/about.html',context)

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                Complaint.objects.create(
                    name=name,
                    email=from_email,
                    subject=subject,
                    message=message
                )
                send_mail(subject,message,from_email,['suchirpandula@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid Header Found')
            messages.success(request, f'Your request has been sent successfully!')
            return redirect('blog-contact')
    return render(request,'blog/contact.html',{'form' : form,'title' : 'contact'})


class SearchView(ListView):
    model = Post
    template_name = 'blog/searchbar.html'  # Your template for search results
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        # Get the search query and date range from the request
        search_query = self.request.GET.get('search', '')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')

        # Start with all posts
        queryset = Post.objects.all()

        # Filter by search query if provided
        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        # Filter by date range if both dates are provided
        if start_date and end_date:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d') + timezone.timedelta(days=1)  # Include the end date
            queryset = queryset.filter(date_posted__range=(start_date, end_date))

        return queryset.order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        posts = context['posts']

        # Add user voting data to each post
        if user.is_authenticated:
            for post in posts:
                post.user_upvoted = post.voters.filter(vote__vote_type='upvote', id=user.id).exists()
                post.user_downvoted = post.voters.filter(vote__vote_type='downvote', id=user.id).exists()
        else:
            for post in posts:
                post.user_upvoted = False
                post.user_downvoted = False

        return context
    
    
def toggle_vote(request, post_id, vote_type):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to vote.'}, status=403)

    post = get_object_or_404(Post, id=post_id)
    existing_vote = Vote.objects.filter(user=request.user, post=post).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove the vote if it's already of the same type
            if vote_type == 'upvote':
                post.upvotes -= 1
            else:
                post.downvotes -= 1
            existing_vote.delete()
        else:
            # Change the vote type
            if vote_type == 'upvote':
                post.upvotes += 1
                post.downvotes -= 1
            else:
                post.downvotes += 1
                post.upvotes -= 1
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        # Create a new vote
        if vote_type == 'upvote':
            post.upvotes += 1
        else:
            post.downvotes += 1
        Vote.objects.create(user=request.user, post=post, vote_type=vote_type)

    post.save()
    return JsonResponse({'upvotes': post.upvotes, 'downvotes': post.downvotes})
