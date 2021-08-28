# agriness_library
Agriness Developer Backend Challenge

### Usual commands
python manage.py runserver 8000

django-admin startapp nameapp

python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

### Challenge

Digamos que você trabalha para uma Livraria Online, onde é possível verificar todos dados
dos livros que você está emprestado ou livros que gostaria de realizar uma reserva. Nosso
tempo de reserva do livro é 3 dias.
Operações esperadas no nosso backend:
Listagem de livros emprestados:
- /client/{id_client}/books
- Lista de livros emprestados

Ao retornar os livros emprestados, verificar de acordo com a regra sobre dias de atraso:
Dias em atraso Multa Juros ao Dia
Sem atraso 0% 0%
Até 3 dias 3% 0.2%
Acima 3 dias 5% 0.4%
Acima 5 dias 7% 0.6%

Reserva de livro:
- /books/{id}/reserve
- Reserva de livro

Reserva de livro passando o id do livro que gostaria de fazer a reserva.
Listagem de livros:
- /books
- Retornar todos livros

Deve retornar todos livros cadastrados e também o seu status, o livro pode estar “disponível”,
“emprestado”.
Informações devem ser persistidas em um banco de dados da sua preferência.