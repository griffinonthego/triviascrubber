import search_sites
import os

site = 'https://quizlet.com/251802743/astronomy-final-exam-flash-cards/'
q_num = 2
search_sites.load_page(site, q_num)
filename = '641a91d6a3751.html'
print(os.stat(filename))
os.setxattr(filename, 'user.url', site.encode())
print(os.stat(filename))



