from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import random
import json
from werkzeug.utils import secure_filename
import logging

# 로깅 설정
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # CORS 설정

# 이미지 업로드 폴더 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 채팅 API 엔드포인트
@app.route('/api/chat', methods=['POST'])
def chat():
    logger.info("채팅 API 호출됨")
    
    try:
        # 요청 로깅
        logger.debug(f"요청 헤더: {request.headers}")
        
        # 요청에서 메시지와 사용자 정보 추출
        if request.is_json:
            # JSON 형식 요청 처리
            logger.debug("JSON 요청 처리")
            data = request.json
            message = data.get('message', '')
            username = data.get('username', 'user')
            logger.debug(f"JSON 데이터: {data}")
            image_url = None
        else:
            # 폼 데이터 요청 처리
            logger.debug("폼 데이터 요청 처리")
            data = request.form.to_dict()
            message = data.get('message', '')
            username = data.get('username', 'user')
            logger.debug(f"폼 데이터: {data}")
            
            # 이미지 파일이 있는 경우 처리
            image_url = None
            if 'image' in request.files:
                image = request.files['image']
                if image.filename:
                    filename = secure_filename(image.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    image.save(filepath)
                    image_url = f"/uploads/{filename}"
                    logger.debug(f"이미지 저장: {filepath}")
        
        # 고정된 레시피 응답 생성
        response_data = {
            "username": "AI 요리사",
            "message": "여기 김치볶음밥 레시피입니다:",
            "recipeId": 1,  # 레시피 ID 추가
            "recipe": {
                "name": "김치볶음밥",
                "description": "맛있는 한국 전통 김치볶음밥",
                "ingredients": [
                    {"name": "김치", "amount": "1컵", "unit": "컵"},
                    {"name": "밥", "amount": "2", "unit": "공기"},
                    {"name": "햄", "amount": "50", "unit": "g"},
                    {"name": "식용유", "amount": "1", "unit": "큰술"},
                    {"name": "파", "amount": "1", "unit": "뿌리"},
                    {"name": "계란", "amount": "1", "unit": "개"},
                    {"name": "참기름", "amount": "1", "unit": "작은술"},
                    {"name": "깨소금", "amount": "약간", "unit": ""}
                ],
                "instructions": [
                    {"step": 1, "instruction": "김치를 잘게 썬다", "cookingTime": 3},
                    {"step": 2, "instruction": "팬에 식용유를 두르고 김치를 볶는다", "cookingTime": 5},
                    {"step": 3, "instruction": "햄을 넣고 함께 볶는다", "cookingTime": 3},
                    {"step": 4, "instruction": "밥을 넣고 잘 섞어가며 볶는다", "cookingTime": 5},
                    {"step": 5, "instruction": "파를 넣고 참기름, 깨소금을 뿌려 마무리한다", "cookingTime": 2},
                    {"step": 6, "instruction": "계란후라이를 올려 완성한다", "cookingTime": 3}
                ],
                "totalTime": 21,
                "difficulty": "쉬움",
                "servings": 2
            },
            "imageUrl": image_url
        }
        
        logger.debug(f"응답 데이터: {response_data}")
        return jsonify(response_data)
    except Exception as e:
        logger.error(f"채팅 처리 중 오류 발생: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    
# 사용자 정보 저장 엔드포인트
@app.route('/api/user-info', methods=['POST'])
def save_user_info():
    logger.info("사용자 정보 API 호출됨")
    
    try:
        # 요청 데이터 로깅
        if request.is_json:
            data = request.json
            logger.debug(f"받은 사용자 정보: {json.dumps(data, default=str)}")
        else:
            logger.warning("JSON 형식이 아닌 요청이 들어왔습니다")
            data = request.form.to_dict()
            logger.debug(f"폼 데이터: {data}")
        
        # 성공 응답
        return jsonify({"status": "success", "message": "사용자 정보가 성공적으로 저장되었습니다"})
    except Exception as e:
        logger.error(f"사용자 정보 처리 중 오류 발생: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 레시피 정보 제공 엔드포인트
@app.route('/api/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    logger.info(f"레시피 정보 API 호출됨: ID={recipe_id}")
    
    try:
        # 임시 레시피 데이터
        recipes = {
            1: {
                "name": "토마토 파스타",
                "description": "신선한 토마토와 바질로 만든 파스타",
                "ingredients": [
                    {"name": "스파게티 면"},
                    {"name": "토마토"},
                    {"name": "바질"},
                    {"name": "올리브 오일"},
                    {"name": "마늘"},
                    {"name": "소금"}
                ],
                "instructions": [
                    {"instruction": "물을 끓인 후 소금을 넣고 스파게티를 삶는다", "cookingTime": 8},
                    {"instruction": "팬에 올리브 오일을 두르고 마늘을 볶는다", "cookingTime": 2},
                    {"instruction": "토마토를 넣고 소스를 만든다", "cookingTime": 5},
                    {"instruction": "삶은 면을 소스에 넣고 바질을 올린다", "cookingTime": 2}
                ]
            },
            2: {
                "name": "김치찌개",
                "description": "맛있는 한국 전통 김치찌개",
                "ingredients": [
                    {"name": "김치"},
                    {"name": "돼지고기"},
                    {"name": "두부"},
                    {"name": "대파"},
                    {"name": "고춧가루"},
                    {"name": "참기름"}
                ],
                "instructions": [
                    {"instruction": "냄비에 참기름을 두르고 돼지고기를 볶는다", "cookingTime": 5},
                    {"instruction": "김치를 넣고 같이 볶는다", "cookingTime": 3},
                    {"instruction": "물을 넣고 끓인다", "cookingTime": 10},
                    {"instruction": "두부와 대파를 넣고 마무리한다", "cookingTime": 5}
                ]
            }
        }
        
        # 레시피 ID로 데이터 찾기
        recipe = recipes.get(recipe_id)
        if not recipe:
            logger.warning(f"레시피를 찾을 수 없음: ID={recipe_id}")
            return jsonify({"error": "Recipe not found"}), 404
        
        logger.debug(f"레시피 정보 응답: {recipe}")
        return jsonify(recipe)
    except Exception as e:
        logger.error(f"레시피 정보 처리 중 오류 발생: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 영양 정보 제공 엔드포인트
@app.route('/api/nutrition/<int:recipe_id>', methods=['GET'])
def get_nutrition(recipe_id):
    logger.info(f"영양 정보 API 호출됨: ID={recipe_id}")
    
    try:
        # 고정된 김치볶음밥 영양 정보
        if recipe_id == 1:
            nutrition = {
                "calories": 450.5,
                "carbohydrate": 65.3,
                "protein": 15.8,
                "fat": 14.2,
                "sugar": 3.5,
                "sodium": 850.0,
                "saturatedFat": 3.2,
                "transFat": 0.1,
                "cholesterol": 105.0,
                "dietaryFiber": 4.2,
                "potassium": 320.5,
                "vitaminA": 15.0,  # % 일일 권장량
                "vitaminC": 22.0,  # % 일일 권장량
                "calcium": 8.0,    # % 일일 권장량
                "iron": 10.0       # % 일일 권장량
            }
            return jsonify(nutrition)
        else:
            logger.warning(f"요청한 레시피 ID({recipe_id})에 대한 영양 정보가 없습니다.")
            return jsonify({"error": "Nutrition data not found"}), 404
            
    except Exception as e:
        logger.error(f"영양 정보 처리 중 오류 발생: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# 정적 파일 제공 (업로드된 이미지)
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    logger.debug(f"파일 요청: {filename}")
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    logger.info("Flask 서버 시작")
    app.run(host='0.0.0.0', port=5000, debug=True)