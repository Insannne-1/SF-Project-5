from django.db import models
from datetime import datetime

from django.contrib.auth.models import User;        # импортируем встроенную будущую таблицу, чтобы хранить в ней данные пользователей

class Author(models.Model):                                             # Таблица с авторами (нет) -
    user = models.OneToOneField(User, on_delete=models.CASCADE);        # - только логин, изначально созданный в таблице User
    rating = models.IntegerField(default=0);                            # Рейтинг автора
    def update_rating(self):                                            # Посчитаем рейтинг
        rt=0;
        r_p=Post.objects.filter(author_id=self.id).values('rating');    # Возьмем набор из Post принадлежащий автору, только поле рейтинг
        for i in range(0,len(r_p)):                                     # .. и проходя циклом
            rt+=r_p[i]['rating'];                                       # .. сложим все значения в словарях из набора
        rt*=3;                                                          # .. и умножим на три.
        r_c=Comment.objects.filter(user_id=Author.objects.get(id=self.id).user_id).values('rating');
        for i in range(0,len(r_c)):                                     # То же проделаем с написанными им (Автором) комментариями
            rt+=r_c[i]['rating'];                                       # (но на три уже не умножаем)
        r_s=Post.objects.filter(author_id=self.id).values('id');        # Теперь посчитаем рейтинг комментариев на все статьи за авторством Автора
        for i in range(0, len(r_s)):                                    # - сперва получим ID всех статей автора и прогоним через цикл..
            n_s=Comment.objects.filter(post_id=r_s[i]['id']).values('rating');  #..где выберем рейтинг комментов на эту статью
            for p in range(0, len(n_s)):                                # прогоним набор через цикл и просто сложим все рейтинги
                rt += n_s[p]['rating'];
        self.rating=rt;                                                 # присвоим новый рейтинг автору
        self.save();                                                    # сохраним
        return self.rating;                                             # и вернем ответ запрашивающему сценарию (пока его нет, но будет)

class Category(models.Model):                                   # Таблица с категориями новостей
    cat_name = models.CharField(max_length=50, unique=True);    # Имя категории (название темы новости) - чтобы без дубликатов

class Post(models.Model):                                                   # Таблица с новостями (сам пост)
    header = models.CharField(max_length=255);                              # Заголовок
    text = models.TextField();                                              # Тело новости
    rating = models.IntegerField(default=0);                                # рейтинг новости
    type = models.IntegerField(default=0);                                  # Тип: новость или статья. По умолчанию - новость (0)
    m_of_creation = models.DateTimeField(auto_now_add=True);                # Дата и время создания (авто - в момент внесения в базу данных)
    author = models.ForeignKey(Author, on_delete=models.CASCADE);           # Автор. Сотрут автора - все новости под его пером тоже удалятся
    category = models.ManyToManyField(Category, through="PostCategory");    # Категория. Cсылается на Category через PostCategory
    def like(self):                                                         # Лайк / дизлайк
        self.rating = self.rating + 1;                                      # Если лайк - лайк +1
        self.save();                                                        # Сохраним его
        return self.rating;                                                 # И сразу вернем новый рейтинг (вдруг в будущем пригодится)
    def dislike(self):                                                      # А если дизлайк -
        self.rating = self.rating - 1;                                      # то вычтем 1. Рейтинг может быть и отрицательным
        self.save();
        return self.rating;                                                 # И тоже покажем обновленный рейтинг

class PostCategory(models.Model):                                           # Помежуточная таблица:
    post = models.ForeignKey(Post, on_delete=models.CASCADE);               # Сотрут пост - и запись из этой таблицы исчезнет
    category = models.ForeignKey(Category, on_delete=models.CASCADE);       # Сотрут тему - исчезнет и здесь и в постах

class Comment(models.Model):                                        # Таблица с комментариями к статье
    post = models.ForeignKey(Post, on_delete=models.CASCADE);       # Ссылка на статью - если последняя удалится, то и коммент тоже
    user = models.ForeignKey(User, on_delete=models.CASCADE);       # Автор коммента. Комментатора сотрут - коммент сотрется сам
    text = models.TextField();                                      # Текст комментария
    m_of_comm = models.DateTimeField(auto_now_add=True);            # Авто-дата и время публикации комментария
    rating = models.IntegerField(default=0);                        # рейтинг комментария
    def like(self):                                                 # Лайк / Дизлайк
        self.rating = self.rating + 1;
        self.save();
        return self.rating;
    def dislike(self):
        self.rating = self.rating - 1;
        self.save();
        return self.rating;