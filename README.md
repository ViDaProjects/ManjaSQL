# ManjaSQL

This project is a database manager system developed in python with it's own language and the ability to load databases from csv files as well as by connecting to mysql workbench. Many SQL like style commands work on this project, such as select for up to two tables, order by asc and desc, update, insert and delete. 

## Syntax

While the commands mentioned before are implemented in our system, they are not under the "default" name provided by sql so we made a small syntax guide to help users who may want to give it a try. The main principle for the choice of words was words that exist in Portuguese and Spanish

or: ou
set: transformar
inner join: juntar interno
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

agarrar, de, donde, distinto e organizar por