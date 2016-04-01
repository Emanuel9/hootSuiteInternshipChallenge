# hootSuiteInternshipChallenge
Stiu ca initial problema imi spune sa stochez toate datele in baza de date si apoi sa fac doar queri-uri mongo. Eu m-am gandit la o alta solutie pe care am argumentat-o mai jos.
Daca nu se accepta aceasta solutie, o sa fac cum mi s-a cerut.

Ideea mea este urmatoarea:

M-am gandit sa nu stochez totul de la inceput, poate nu intereseaza pe nimeni ce 
s-a intamplat intr-o anumita zi.

Se face urmatorul request http://127.0.0.1:5000/?year=2005&day=November_3&category=births sau orice request care respecta acest format.

Verific daca am ceva in baza mea de date mongo pentru acest request.

In cazul in care am, intorc userului un raspuns in json cu ce am gasit in baza de date pentru acea interogare.

In cazul in care nu am, folosesc api-ul de wikipedia pentru a-mi aduce in baza de date informatiile cerute de utilizator, apoi ii voi da json-ul din baza mea mongo.

Instructiuni de utilizare a scriptului
#########################################

Baza mea de date se numeste hootsuite:

use hootsuite

Folosesc o colectie pages in care stochez datele aduse atunci cand se face request-ul.
db.createCollection("pages")

Voi porni aplicatia asa : python fetch_wikipedia_data.py

Folosesc flask

Pasi
#######################################################################################################################

1. Iau din request year, day and category
2. Ma conectez la baza de date mongo
3. In cazul in care am date in baza de data care sa satisfaca requestul userului, ii intorc datele in forma json. In cazul in care nu am date, folosesc api-ul de wikipedia sa imi aduc
datele local, creez un document in JSON cu ele, il inserez in baza de date mongo apoi ii intorc userului ce a cerut.
4. Ma deconectez de la baza de date mongo

Early release
######################################################




