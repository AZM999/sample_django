from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
# Create your views here.





def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<modelname>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  #<app>/<modelname>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4
    
    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
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


def about(request):
    return render(request, 'blog/about.html', {'title':'about'})


posts = [
    {
        'author': 'azm',
        'title' : 'BGE 14',
        'content' : ' It is perhaps just dawning on five or six minds that natural philosophy is only a world-exposition and world-arrangement (according to us, if I may say so!) and NOT a world-explanation; but in so far as it is based on belief in the senses, it is regarded as more, and for a long time to come must be regarded as more—namely, as an explanation. It has eyes and fingers of its own, it has ocular evidence and palpableness of its own: this operates fascinatingly, persuasively, and CONVINCINGLY upon an age with fundamentally plebeian tastes—in fact, it follows instinctively the canon of truth of eternal popular sensualism. What is clear, what is "explained"? Only that which can be seen and felt—one must pursue every problem thus far. Obversely, however, the charm of the Platonic mode of thought, which was an ARISTOCRATIC mode, consisted precisely in RESISTANCE to obvious sense-evidence—perhaps among men who enjoyed even stronger and more fastidious senses than our contemporaries, but who knew how to find a higher triumph in remaining masters of them: and this by means of pale, cold, grey conceptional networks which they threw over the motley whirl of the senses—the mob of the senses, as Plato said. In this overcoming of the world, and interpreting of the world in the manner of Plato, there was an ENJOYMENT different from that which the physicists of today offer us—and likewise the Darwinists and anti-teleologists among the physiological workers, with their principle of the "smallest possible effort," and the greatest possible blunder. "Where there is nothing more to see or to grasp, there is also nothing more for men to do"—that is certainly an imperative different from the Platonic one, but it may notwithstanding be the right imperative for a hardy, laborious race of machinists and bridge-builders of the future, who have nothing but ROUGH work to perform. ',
        'date_posted' : 'September 9, 2024'
    },
    {
        'author': 'azm999',
        'title' : 'BGE 193',
        'content' : 'Quidquid luce fuit, tenebris agit: but also contrariwise. What we experience in dreams, provided we experience it often, pertains at last just as much to the general belongings of our soul as anything "actually" experienced; by virtue thereof we are richer or poorer, we have a requirement more or less, and finally, in broad daylight, and even in the brightest moments of our waking life, we are ruled to some extent by the nature of our dreams. Supposing that someone has often flown in his dreams, and that at last, as soon as he dreams, he is conscious of the power and art of flying as his privilege and his peculiarly enviable happiness; such a person, who believes that on the slightest impulse, he can actualize all sorts of curves and angles, who knows the sensation of a certain divine levity, an "upwards" without effort or constraint, a "downwards" without descending or lowering—without TROUBLE!—how could the man with such dream-experiences and dream-habits fail to find "happiness" differently coloured and defined, even in his waking hours! How could he fail—to long DIFFERENTLY for happiness? "Flight," such as is described by poets, must, when compared with his own "flying," be far too earthly, muscular, violent, far too "troublesome" for him. ',
        'date_posted' : 'September 11, 2024'
    }]