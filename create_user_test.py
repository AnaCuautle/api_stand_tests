import sender_stand_request
import data


# Esta función cambia el valor del parámetro "firstName"
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


# Función para pruebas positivas
def positive_assert(first_name):
    user_body = get_user_body(first_name)

    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


# Función para pruebas negativas con firstName inválido
def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)

    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400

    assert response.json()["message"] == "Has introducido un nombre de usuario no válido. " \
                                         "El nombre solo puede contener letras del alfabeto latino, " \
                                         "la longitud debe ser de 2 a 15 caracteres."


# Función para pruebas negativas sin firstName válido
def negative_assert_no_firstname(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400
    assert response.json()["code"] == 400
    assert response.json()["message"] == "No se han aprobado todos los parámetros requeridos"


# PRUEBA 1
# firstName contiene 2 caracteres → válido
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# PRUEBA 2
# firstName contiene 15 caracteres → válido
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aaaaaaaaaaaaaaa")


# PRUEBA 3
# firstName contiene 1 carácter → inválido
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")


# PRUEBA 4
# firstName contiene 16 caracteres → inválido
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Aaaaaaaaaaaaaaaa")


# PRUEBA 5
# firstName contiene espacios → según la checklist debería ser inválido
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("A Aaa")


# PRUEBA 6
# firstName contiene caracteres especiales
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("\"№%@\",")


# PRUEBA 7
# firstName contiene números
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


# PRUEBA 8
# La solicitud no contiene firstName
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")

    negative_assert_no_firstname(user_body)

# PRUEBA 9
# firstName contiene un string vacío
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")

    negative_assert_no_firstname(user_body)

# Prueba 10. Error
# El tipo del parámetro "firstName" es un número
def test_create_user_number_type_first_name_get_error_response():
    # El cuerpo de la solicitud actualizada se guarda en la variable user_body
    user_body = get_user_body(12)
    # El resultado de la solicitud para crear un nuevo usuario o usuaria se guarda en la variable response
    response = sender_stand_request.post_new_user(user_body)

    # Comprobar el código de estado de la respuesta
    assert response.status_code == 400
