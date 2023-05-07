from django.shortcuts import get_object_or_404, render
from django.views import generic, View


from .forms import CommentForm
from .models import Post


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 3


class PostDetailView(View):
    def get(self, request, slug):
        template_name = "post_detail.html"
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True).order_by("-created_on")
        comment_form = CommentForm()
        context = {
            "post": post,
            "comments": comments,
            "comment_form": comment_form,
        }
        return render(request, template_name, context)

    def post(self, request, slug):
        template_name = "post_detail.html"
        post = get_object_or_404(Post, slug=slug)
        comments = post.comments.filter(active=True).order_by("-created_on")
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            context = {
                "post": post,
                "comments": comments,
                "new_comment": new_comment,
                "comment_form": CommentForm(),
            }
        else:
            context = {
                "post": post,
                "comments": comments,
                "comment_form": comment_form,
            }
        return render(request, template_name, context)


