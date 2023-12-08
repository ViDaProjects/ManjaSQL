# ManjaSQL

This project is a database manager system developed in python with it's own language and the ability to load databases from csv files as well as by connecting to mysql workbench. Many SQL like style commands work on this project, such as select for up to two tables, order by asc and desc, update, insert and delete. 

## Syntax

While the commands mentioned before are implemented in our system, they are not under the "default" name provided by sql so we made a small syntax guide to help users who may want to give it a try. The main principle for the choice of words was words that exist in Portuguese and Spanish

or: ou
set: transformar
inner join on: juntar interno em
insert into: inserir
and: e
order by: organizar por
where: donde
insert into: inserir
update: modificar
delete from: apagar
select: agarrar
values: valores
from: de
distinct: distinto
asc: asc
desc: desc

## Order

This language is, unfortunately, not as modular as real sql, so, during "select" commands it is important that present fields get filled in the correct order, that is:

agarrar, distinto, de, juntar interno em, donde e organizar por

Commands on sql will still run 

## Examples

select emp_no, dept_no, dept_name from dept_emp, departments inner join ON dept_no
agarrar emp_no, dept_no, dept_name de dept_emp, departments juntar interno em dept_no

select livro_id, titulo, genero_id, descricao from livros, generos inner join ON genero_id where livro_id > 5
agarrar livro_id, titulo, genero_id, descricao de livros, generos inner join on genero_id donde livro_id > 5 

select titulo from livros, generos inner join
agarrar titulo de livros, generos juntar interno

select livro_id, titulo, autor order by livro_id desc
agarrar livro_id, titulo, autor organizar por livro_id desc

update livros set preco = 600
modificar livros transformar preco = 600

update livros set preco = 120 where livro_id < 10
modificar livros transformar preco = 120 donde livro_id < 10

delete from livros where livro_id = 4
apagar livros donde livro_id = 4

insert into livros values 23, 'David Segalle, Viviane Ruotolo' 1, UTFPR, 3, 'One of the books of all time', 150, 1000, 0
inserir livros valores 23, 'David Segalle, Viviane Ruotolo' 1, UTFPR, 3, 'One of the books of all time', 150, 1000, 0

insert into livros preco, estoque, reserva, livro_id, titulo, autor, edicao, ano, editora, genero_id, descricao values 150, 1000, 0, 23, 'David Segalle, Viviane Ruotolo' 1, UTFPR, 3, 'One of the books of all time'

inserir livros preco, estoque, reserva, livro_id, titulo, autor, edicao, ano, editora, genero_id, descricao valores 150, 1000, 0, 23, 'David Segalle, Viviane Ruotolo' 1, UTFPR, 3, 'One of the books of all time'
