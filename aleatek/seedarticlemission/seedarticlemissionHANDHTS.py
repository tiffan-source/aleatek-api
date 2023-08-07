# !/bin/bash/python
# import django.conf as settings
import django

django.setup()
# settings.configure()

from mission.models import Article

with open('seedarticlemissionHANDHTS.txt', 'r') as f:
    lines = f.readlines()
    idsupper = []
    idfirstlevel = []
    idsenconlevel = []
    for i, line in enumerate(lines):
        print(i)
        if line.isupper():
            data = Article(titre=line, article_parent_id=None, commentaire='', mission_id=2)
            data.save()
            idsupper.append(data.id)
        elif line[0] == '\t' and line[1] == '\t' and line[2] == '-':
            data = Article(titre=line.replace('\n', '').replace('\t', '').replace("- ", ""),
                           article_parent_id=idsenconlevel[-1], commentaire='', mission_id=2)
            data.save()
        elif line[0] == '\t' and line[1] == '\t':
            data = Article(titre=line.replace('\n', '').replace('\t', '').replace("- ", ""),
                           article_parent_id=idfirstlevel[-1], commentaire='', mission_id=2)
            data.save()
            idsenconlevel.append(data.id)
        elif line[0] == '\t':
            data = Article(titre=line.replace('\n', '').replace('\t', '').replace("- ", ""),
                           article_parent_id=idsupper[-1], commentaire='', mission_id=2)
            data.save()
            idfirstlevel.append(data.id)
        else:
            print(line)
