from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from mainpage.forms import PublishNewsForm
from mainpage.models import Article


@login_required(login_url='/lk/login/')
def publish_news(request):
    if request.user.role == 'pupil':
        return render(request, 'no_info.html', {'message': 'У Вас нет прав для публикации новостей'})

    form = PublishNewsForm(request.POST or None, request.FILES or None, user=request.user)

    if request.method == "POST":
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            return redirect('news')  # После публикации переходим к списку новостей

    return render(request, 'articles/publish_news.html', {'form': form})

def news(request):
    article = Article.objects.all()
    context = {
        'articles': article
    }
    return render(request, 'articles/news.html', context)


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id) #Получаем статью или 404 ошибку
    return render(request, 'articles/article.html', {'article': article})
