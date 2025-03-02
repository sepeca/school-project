from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from mainpage.forms import PublishNewsForm
from mainpage.models import Article


@login_required(login_url='/lk/login/')
def publish_news(request):
    if request.user.role == 'pupil':
        return render(request,'no_info.html', {'message': 'У Вас нет прав для публикации новостей'})
    if request.method == "POST":
        form = PublishNewsForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('news')  # Замените на вашу страницу с новостями
    else:
        form = PublishNewsForm(user=request.user)

    return render(request, 'publish_news.html', {'form': form})

def news(request):
    article = Article.objects.all()
    context = {
        'articles': article
    }
    return render(request, 'news.html', context)


def show_article(request, article_id):
    article = get_object_or_404(Article, id=article_id) #Получаем статью или 404 ошибку
    return render(request, 'article.html', {'article': article})
