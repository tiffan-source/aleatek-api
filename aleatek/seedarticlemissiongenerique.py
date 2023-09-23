# !/bin/bash/python
# import django.conf as settings
import django

django.setup()
# settings.configure()

from mission.models import Article, ArticleMission

with open('articlemissionL.txt', 'r') as f:
    lines = f.readlines()
    idsupper = []
    idfirstlevel = []
    idsenconlevel = []
    try:
        for i, line in enumerate(lines):
            print(line)
            
            if line.isupper():
                if Article.objects.filter(titre=line).exists():
                    id = Article.objects.get(titre=line).id
                    ArticleMission(article_id=id, mission_id=1).save()
                    if id not in idsupper:
                        idsupper.append(id)
                else:
                    data = Article(titre=line, article_parent_id=None, commentaire='')
                    data.save()
                    idsupper.append(data.id)
                    ArticleMission(article_id=data.id, mission_id=1).save()
            
            elif line.startswith("\t\t- "):
                if Article.objects.filter(titre=line.replace('\n', '').replace('\t', '')).exists():
                    id = Article.objects.get(titre=line.replace('\n', '').replace('\t', '')).id
                    ArticleMission(article_id=id, mission_id=1).save()
                else:
                    data = Article(titre=line.replace('\n', '').replace('\t', ''), article_parent_id=idsenconlevel[-1],
                                commentaire='')
                    data.save()
                    ArticleMission(article_id=data.id, mission_id=1).save()
            
            elif line.startswith("\t\t"):
                if Article.objects.filter(titre=line.replace('\n', '').replace('\t', '')).exists():
                    id = Article.objects.get(titre=line.replace('\n', '').replace('\t', '')).id
                    ArticleMission(article_id=id, mission_id=1).save()
                    if id not in idsenconlevel:
                        idsenconlevel.append(id)
                else:
                    data = Article(titre=line.replace('\n', '').replace('\t', ''), article_parent_id=idfirstlevel[-1],
                                commentaire='')
                    data.save()
                    idsenconlevel.append(data.id)
                    ArticleMission(article_id=data.id, mission_id=1).save()
            
            elif line.startswith("\t"):
                if Article.objects.filter(titre=line.replace('\n', '').replace('\t', '')).exists():
                    id = Article.objects.get(titre=line.replace('\n', '').replace('\t', '')).id
                    ArticleMission(article_id=id, mission_id=1).save()
                    if id not in idfirstlevel:
                        idfirstlevel.append(id)
                else:
                    data = Article(titre=line.replace('\n', '').replace('\t', ''), article_parent_id=idsupper[-1],
                                commentaire='')
                    data.save()
                    idfirstlevel.append(data.id)
                    ArticleMission(article_id=data.id, mission_id=1).save()
            else:
                print(line)
    except Exception as ex:
        print(ex)
        Article.objects.all().delete()
        