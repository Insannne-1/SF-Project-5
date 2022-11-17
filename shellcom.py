# 0.
from news.models import *

# 1. Задача - Создать двух пользователей
User.objects.create_user(username='Author_1', password='password_1', email='mail_1@mail.net', first_name='Аркадий', last_name='Аркадьев')
User.objects.create_user(username='Author_2', password='password_2', email='mail_2@mail.net', first_name='Борис', last_name='Борисов')

# 2. Задача - Создать двух авторов (они же - "пользователи", только способные писать статьи)
Author.objects.create(user_id=User.objects.get(username='Author_1').pk)
Author.objects.create(user_id=User.objects.get(username='Author_2').pk)

# 3. Задача - Добавить категории
Category.objects.create(cat_name='Экстренно')
Category.objects.create(cat_name='Политика')
Category.objects.create(cat_name='Спорт')
Category.objects.create(cat_name='Культура')
Category.objects.create(cat_name='Погода')
Category.objects.create(cat_name='Происшествия')

# 4. Задача - Добавить две статьи и одну новость
post_1=Post.objects.create(type=1, header='Заголовок статьи 1', text='Текст статьи 1', author_id=Author.objects.get(user_id=User.objects.get(username='Author_1').pk).pk)
post_2=Post.objects.create(type=1, header='Заголовок статьи 2', text='Текст статьи 2', author_id=Author.objects.get(user_id=User.objects.get(username='Author_2').pk).pk)
post_3=Post.objects.create(type=0, header='Заголовок новости 1', text='Текст новости 1', author_id=Author.objects.get(user_id=User.objects.get(username='Author_2').pk).pk)

# 5. Задача - присвоить созданным статьям/новостям несколько категорий
PostCategory.objects.create(post_id=post_1.id, category_id= Category.objects.get(cat_name='Политика').pk)
PostCategory.objects.create(post_id=post_1.id, category_id= Category.objects.get(cat_name='Спорт').pk)
PostCategory.objects.create(post_id=post_2.id, category_id= Category.objects.get(cat_name='Культура').pk)
PostCategory.objects.create(post_id=post_2.id, category_id= Category.objects.get(cat_name='Политика').pk)
PostCategory.objects.create(post_id=post_3.id, category_id= Category.objects.get(cat_name='Экстренно').pk)
PostCategory.objects.create(post_id=post_3.id, category_id= Category.objects.get(cat_name='Происшествия').pk)

# 6. Задача - Создать комментарии к постам
comm_1=Comment.objects.create(post_id=post_1.id, user_id=User.objects.get(username='Author_2').pk, text='Комментарий 1 от пользователя 2 на пост 1 автора 1')
comm_2=Comment.objects.create(post_id=post_1.id, user_id=User.objects.get(username='Author_2').pk, text='Комментарий 2 от пользователя 2 на пост 1 автора 1')
comm_3=Comment.objects.create(post_id=post_1.id, user_id=User.objects.get(username='Author_2').pk, text='Комментарий 3 от пользователя 2 на пост 1 автора 1')
comm_4=Comment.objects.create(post_id=post_2.id, user_id=User.objects.get(username='Author_1').pk, text='Комментарий 1 от пользователя 1 на пост 2 автора 2')
comm_5=Comment.objects.create(post_id=post_2.id, user_id=User.objects.get(username='Author_1').pk, text='Комментарий 2 от пользователя 1 на пост 2 автора 2')
comm_6=Comment.objects.create(post_id=post_3.id, user_id=User.objects.get(username='Author_1').pk, text='Комментарий 1 от пользователя 1 на пост 3 автора 2')

# 7. Задача - "поставить" лайки и дизлайки
post_1.like()
post_1.like()
post_1.like()
post_1.like()
post_1.like()
post_1.like()
post_1.like()
post_1.like()
post_2.like()
post_2.like()
post_2.like()
post_2.like()
post_3.like()
post_3.like()
comm_1.like()
comm_2.dislike()
comm_2.dislike()
comm_3.dislike()
comm_4.like()
comm_4.like()
comm_5.like()
comm_5.like()
comm_5.like()
comm_6.like()

# 8. Задача - обновить рейтинг пользователей (авторов)
Author.objects.get(user_id=User.objects.get(username='Author_1').pk).update_rating()
Author.objects.get(user_id=User.objects.get(username='Author_2').pk).update_rating()

# 9. Задача - Вычислить лучшего (по рейтингу) пользователя
print(f"Пользователь {User.objects.get(id=Author.objects.order_by('rating').last().user_id).username} имеет лучший рейтинг из всех: {Author.objects.order_by('rating').last().rating} баллов")

# 10. Задача - Найти лучшую статью и вывести данные по ней
bestpost=Post.objects.order_by('rating').last().id
bp_date=Post.objects.get(id=bestpost).m_of_creation.date()
bp_author=User.objects.get(id=Author.objects.get(id=Post.objects.get(id=bestpost).author_id).user_id).username
bp_title=Post.objects.get(id=bestpost).header
bp_body=Post.objects.get(id=bestpost).text
print(f"<<Лучшая статья>>:\nдата: {bp_date}\nАвтор: {bp_author}\nНазвание: {bp_title}\nКраткое содержание (очень):{bp_body[0:10]}")

# 11. Задача - Найти все комментарии к лучшей (по рейтингу) статье
c_bestpost=Comment.objects.filter(post_id=bestpost).order_by('-m_of_comm')
print("Лучшие комментарии:\n")
for i in c_bestpost:
    print(f"Дата: {i.m_of_comm.date()}\nАвтор: {User.objects.get(id=i.user_id).username}\nРейтинг: {i.rating}\nТекст: {i.text}\n")