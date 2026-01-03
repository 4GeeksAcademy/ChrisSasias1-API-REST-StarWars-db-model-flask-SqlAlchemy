
# [GET] /people                                 Listar todos los registros de people(characters) en la base de datos.
# [GET] /people/<int:people_id>                 Muestra la información de un solo personaje según su id.
# [GET] /planets                                Listar todos los registros de planets en la base de datos.
# [GET] /planets/<int:planet_id>                Muestra la información de un solo planeta según su id.


# Adicionalmente, necesitamos crear los siguientes endpoints para que podamos tener usuarios y favoritos en nuestro blog:

# [GET] /users                                                   Listar todos los usuarios del blog.
# [GET] /users/<int:user_id>/favorites                           Listar todos los favoritos que pertenecen al usuario actual.
# [POST] /favorite/planet/<int:planet_id>/user/<int:user_id>     Añade un nuevo planet favorito al usuario actual con el id = planet_id.
# [POST] /favorite/people/<int:people_id>/user/<int:user_id>     Añade un nuevo people favorito al usuario actual con el id = people_id.
# [DELETE] /favorite/planet/<int:planet_id>/user/<int:user_id>   Elimina un planet favorito con el id = planet_id.
# [DELETE] /favorite/people/<int:people_id>/user/<int:user_id>   Elimina un people favorito con el id = people_id.

# ***** Opcionales(
#     Hacer lo mismo con Starships
#     Crear endpoint POST para agregar usuarios, planetas, starships y characters
#     Métodos PUT para actualizar información de planetas, starships, characters y usuarios
# )
 