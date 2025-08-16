#!/usr/bin/env python3
import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from http import HTTPStatus
import uuid
from datetime import datetime

# Mock recipes data
recipes_data = [
    {
        "id": "1",
        "title": "クラシック・パスタ・カルボナーラ",
        "description": "クリーミーで贅沢なローマの定番パスタ料理。卵、チーズ、パンチェッタで作る本格的なカルボナーラです。",
        "category": "メイン",
        "prepTime": 10,
        "cookTime": 15,
        "servings": 4,
        "difficulty": "Medium",
        "image": "https://images.pexels.com/photos/4518843/pexels-photo-4518843.jpeg?auto=compress&cs=tinysrgb&w=800",
        "ingredients": [
            "スパゲッティ 400g",
            "パンチェッタ 150g",
            "卵黄 4個",
            "パルミジャーノ・レッジャーノ 100g",
            "黒胡椒 適量",
            "塩 適量"
        ],
        "instructions": [
            "パスタを茹でる準備をする。大きな鍋にたっぷりの塩水を沸かす。",
            "パンチェッタを小さく切り、フライパンでカリカリになるまで炒める。",
            "卵黄とチーズ、黒胡椒を混ぜ合わせてソースを作る。",
            "パスタを規定時間より1分短く茹でる。",
            "パスタをフライパンに移し、火を止めてソースを加えて素早く混ぜる。",
            "皿に盛り、追加のチーズと黒胡椒をかけて完成。"
        ],
        "tags": ["イタリアン", "パスタ", "クリーミー"]
    },
    {
        "id": "2",
        "title": "照り焼きチキン",
        "description": "甘辛い照り焼きソースが絡んだジューシーなチキン。ご飯との相性も抜群の定番和食です。",
        "category": "メイン",
        "prepTime": 15,
        "cookTime": 20,
        "servings": 4,
        "difficulty": "Easy",
        "image": "https://images.pexels.com/photos/2338407/pexels-photo-2338407.jpeg?auto=compress&cs=tinysrgb&w=800",
        "ingredients": [
            "鶏もも肉 600g",
            "醤油 大さじ4",
            "みりん 大さじ3",
            "砂糖 大さじ2",
            "酒 大さじ2",
            "生姜 1片",
            "サラダ油 大さじ1"
        ],
        "instructions": [
            "鶏肉を一口大に切り、塩胡椒で下味をつける。",
            "生姜をすりおろし、調味料と混ぜ合わせてタレを作る。",
            "フライパンに油を熱し、鶏肉の皮目から焼く。",
            "両面に焼き色がついたらタレを加える。",
            "タレが煮詰まって照りが出るまで煮絡める。",
            "器に盛り、お好みで胡麻や青ねぎをかけて完成。"
        ],
        "tags": ["和食", "チキン", "照り焼き"]
    },
    {
        "id": "3",
        "title": "チョコレートブラウニー",
        "description": "濃厚でファッジのような食感のチョコレートブラウニー。バニラアイスと一緒に召し上がれ。",
        "category": "デザート",
        "prepTime": 20,
        "cookTime": 35,
        "servings": 12,
        "difficulty": "Easy",
        "image": "https://images.pexels.com/photos/887853/pexels-photo-887853.jpeg?auto=compress&cs=tinysrgb&w=800",
        "ingredients": [
            "ダークチョコレート 200g",
            "バター 150g",
            "砂糖 150g",
            "卵 3個",
            "薄力粉 75g",
            "ココアパウダー 25g",
            "バニラエッセンス 小さじ1",
            "くるみ 100g（お好みで）"
        ],
        "instructions": [
            "オーブンを180℃に予熱し、型にバターを塗って粉をまぶす。",
            "チョコレートとバターを湯煎で溶かす。",
            "砂糖と卵を泡立て器で混ぜ、溶かしたチョコレートを加える。",
            "ふるった粉類を加えて混ぜ、お好みでくるみを加える。",
            "型に流し入れ、35分焼く。",
            "完全に冷ましてから型から出し、お好みの大きさに切る。"
        ],
        "tags": ["デザート", "チョコレート", "ブラウニー"]
    },
    {
        "id": "4",
        "title": "シーザーサラダ",
        "description": "クリスピーなクルトンとパルメザンチーズが決め手の定番サラダ。自家製ドレッシングで本格的な味わい。",
        "category": "前菜",
        "prepTime": 15,
        "cookTime": 5,
        "servings": 4,
        "difficulty": "Easy",
        "image": "https://images.pexels.com/photos/1213710/pexels-photo-1213710.jpeg?auto=compress&cs=tinysrgb&w=800",
        "ingredients": [
            "ロメインレタス 2束",
            "パルメザンチーズ 50g",
            "クルトン 1カップ",
            "マヨネーズ 大さじ3",
            "レモン汁 大さじ2",
            "アンチョビペースト 小さじ1",
            "にんにく 1片",
            "オリーブオイル 大さじ1"
        ],
        "instructions": [
            "レタスをよく洗い、食べやすい大きさにちぎって水気を切る。",
            "にんにくをすりおろし、ドレッシングの材料を混ぜ合わせる。",
            "パンを小さく切り、オリーブオイルで炒めてクルトンを作る。",
            "ボウルにレタスを入れ、ドレッシングをかけて和える。",
            "クルトンとパルメザンチーズをかける。",
            "器に盛り、お好みで追加のチーズをかけて完成。"
        ],
        "tags": ["サラダ", "前菜", "シーザー"]
    },
    {
        "id": "5",
        "title": "味噌ラーメン",
        "description": "濃厚でコクのある味噌スープが自慢のラーメン。もやしとコーンをトッピングした定番の一杯。",
        "category": "メイン",
        "prepTime": 20,
        "cookTime": 25,
        "servings": 2,
        "difficulty": "Hard",
        "image": "https://images.pexels.com/photos/884596/pexels-photo-884596.jpeg?auto=compress&cs=tinysrgb&w=800",
        "ingredients": [
            "ラーメン麺 2玉",
            "豚バラ肉 200g",
            "味噌 大さじ4",
            "鶏がらスープの素 大さじ1",
            "もやし 1袋",
            "コーン 100g",
            "ねぎ 1本",
            "にんにく 2片",
            "生姜 1片",
            "ゆで卵 2個"
        ],
        "instructions": [
            "スープを作る。鍋に水800mlを沸かし、鶏がらスープの素を溶かす。",
            "にんにくと生姜をみじん切りにし、炒めて香りを出す。",
            "味噌を少しずつ加えて溶かし、スープに加える。",
            "豚バラ肉を炒めて火を通す。",
            "麺を茹でて丼に入れる。",
            "スープをかけ、豚肉、もやし、コーン、ねぎ、ゆで卵をトッピングして完成。"
        ],
        "tags": ["ラーメン", "味噌", "和食"]
    },
    {
        "id": "6",
        "title": "フルーツタルト",
        "description": "サクサクのタルト生地にカスタードクリームと季節のフルーツを贅沢に盛った華やかなデザート。",
        "category": "デザート",
        "prepTime": 45,
        "cookTime": 30,
        "servings": 8,
        "difficulty": "Hard",
        "image": "https://images.pexels.com/photos/1126359/pexels-photo-1126359.jpeg?auto=compress&cs=tinysrgb&w=800",
        "ingredients": [
            "薄力粉 150g",
            "バター 75g",
            "砂糖 30g",
            "卵黄 1個",
            "牛乳 200ml",
            "卵 2個",
            "コーンスターチ 大さじ2",
            "バニラエッセンス 小さじ1",
            "お好みのフルーツ 適量",
            "アプリコットジャム 大さじ2"
        ],
        "instructions": [
            "タルト生地を作る。粉とバター、砂糖を混ぜ、卵黄を加えてまとめる。",
            "生地を伸ばして型に敷き、180℃で20分焼く。",
            "カスタードクリームを作る。卵、砂糖、コーンスターチを混ぜ、温めた牛乳を加える。",
            "鍋で加熱しながら混ぜ、とろみがつくまで煮る。",
            "冷ましたタルト生地にカスタードを流し入れる。",
            "フルーツを美しく並べ、温めたジャムを塗って完成。"
        ],
        "tags": ["デザート", "タルト", "フルーツ"]
    }
]

categories = ["すべて", "メイン", "前菜", "デザート", "サラダ", "スープ"]

# Curated food images from Pexels
food_images = [
    "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/376464/pexels-photo-376464.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1092730/pexels-photo-1092730.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1410235/pexels-photo-1410235.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1099680/pexels-photo-1099680.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1438672/pexels-photo-1438672.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640772/pexels-photo-1640772.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1199957/pexels-photo-1199957.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1435904/pexels-photo-1435904.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640774/pexels-photo-1640774.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640773/pexels-photo-1640773.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640775/pexels-photo-1640775.jpeg?auto=compress&cs=tinysrgb&w=800",
    "https://images.pexels.com/photos/1640776/pexels-photo-1640776.jpeg?auto=compress&cs=tinysrgb&w=800"
]

import random

class RecipeAPIHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)
        
        # Set CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if path == '/api/recipes':
            # Get all recipes with optional filtering
            filtered_recipes = recipes_data.copy()
            
            # Filter by search term
            if 'search' in query_params:
                search_term = query_params['search'][0].lower()
                filtered_recipes = [
                    recipe for recipe in filtered_recipes
                    if (search_term in recipe['title'].lower() or 
                        search_term in recipe['description'].lower() or
                        any(search_term in tag.lower() for tag in recipe['tags']))
                ]
            
            # Filter by category
            if 'category' in query_params:
                category = query_params['category'][0]
                if category != 'すべて':
                    filtered_recipes = [
                        recipe for recipe in filtered_recipes
                        if recipe['category'] == category
                    ]
            
            response = {
                'recipes': filtered_recipes,
                'total': len(filtered_recipes)
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif path == '/api/categories':
            # Get all categories
            response = {'categories': categories}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif path == '/api/images/random':
            # Get random food image
            random_image = random.choice(food_images)
            response = {'image_url': random_image}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif path == '/api/images':
            # Get all available food images
            response = {'images': food_images}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        elif path.startswith('/api/recipes/'):
            # Get specific recipe by ID
            recipe_id = path.split('/')[-1]
            recipe = next((r for r in recipes_data if r['id'] == recipe_id), None)
            
            if recipe:
                self.wfile.write(json.dumps(recipe, ensure_ascii=False).encode('utf-8'))
            else:
                self.send_error(404, 'Recipe not found')
        else:
            self.send_error(404, 'Endpoint not found')

    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/recipes':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                recipe_data = json.loads(post_data.decode('utf-8'))
                
                # Generate new ID and add recipe
                new_recipe = {
                    'id': str(uuid.uuid4()),
                    **recipe_data,
                    'image': recipe_data.get('image', random.choice(food_images))
                }
                
                recipes_data.insert(0, new_recipe)
                
                self.send_response(201)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                self.wfile.write(json.dumps(new_recipe, ensure_ascii=False).encode('utf-8'))
                
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
        else:
            self.send_error(404, 'Endpoint not found')

    def log_message(self, format, *args):
        """Override to reduce log noise"""
        return

def run_server(port=8080):
    """Run the API server"""
    with socketserver.TCPServer(("", port), RecipeAPIHandler) as httpd:
        print(f"Recipe API server running on http://localhost:{port}")
        print("Available endpoints:")
        print("  GET  /api/recipes - Get all recipes (supports ?search= and ?category= params)")
        print("  GET  /api/recipes/{id} - Get specific recipe")
        print("  GET  /api/categories - Get all categories")
        print("  GET  /api/images - Get all available food images")
        print("  GET  /api/images/random - Get random food image")
        print("  POST /api/recipes - Create new recipe")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run_server()