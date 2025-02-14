from flask import Blueprint, request, jsonify
from database import db
from models.meal import Meal
from datetime import datetime

meals_bp = Blueprint("meals", __name__)

# Criar uma refeição
@meals_bp.route("/meals", methods=["POST"])
def create_meal():
    data = request.get_json()

    # Obtém os valores do JSON
    name = data.get("name")
    description = data.get("description")
    date_time_str = data.get("date_time")
    in_diet = "sim" if data.get("in_diet") else "não"  # Converte True/False para "sim" ou "não"


    # Verifica se todos os campos estão presentes
    if not all([name, description, date_time_str, in_diet]):
        return jsonify({"error": "Missing required fields"}), 400

    # Valida a data
    try:
        date_time = datetime.fromisoformat(date_time_str)
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)"}), 400

    # Cria e salva no banco
    try:
        new_meal = Meal(name=name, description=description, date_time=date_time, in_diet=in_diet)
        db.session.add(new_meal)
        db.session.commit()
        return jsonify({"message": "Meal added successfully!", "id": new_meal.id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error when saving to the database", "details": str(e)}), 500

        
# Listar todas as refeições
@meals_bp.route("/meals", methods=["GET"])
def get_meals():
    meals = Meal.query.all()
    meals_list = [
        {
            "id": meal.id,
            "name": meal.name,
            "description": meal.description,
            "date_time": meal.date_time.isoformat(),  # Retorna em ISO 8601
            "in_diet": meal.in_diet,
        }
        for meal in meals
    ]
    return jsonify(meals_list)


# Obter uma refeição específica
@meals_bp.route("/meals/<int:meal_id>", methods=["GET"])
def get_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"error": "Refeição não encontrada"}), 404

    return jsonify({
        "id": meal.id,
        "name": meal.name,
        "description": meal.description,
        "date_time": meal.date_time.isoformat(),  # Retorna em ISO 8601
        "in_diet": meal.in_diet,
    })


# Editar uma refeição
@meals_bp.route("/meals/<int:meal_id>", methods=["PUT"])
def update_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"error": "Refeição não encontrada"}), 404

    data = request.get_json()
    
    try:
        meal.name = data["name"]
        meal.description = data["description"]
        meal.date_time = datetime.fromisoformat(data["date_time"])  # Converte ISO 8601
        meal.in_diet = data["in_diet"]

        db.session.commit()
        return jsonify({"message": "Refeição atualizada com sucesso!"})
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)"}), 400


# Apagar uma refeição
@meals_bp.route("/meals/<int:meal_id>", methods=["DELETE"])
def delete_meal(meal_id):
    meal = Meal.query.get(meal_id)
    if not meal:
        return jsonify({"error": "Refeição não encontrada"}), 404

    db.session.delete(meal)
    db.session.commit()
    return jsonify({"message": "Refeição deletada com sucesso!"})
