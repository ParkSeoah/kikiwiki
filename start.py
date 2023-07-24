import os
import sqlite3
from flask import Flask, request, g, render_template

app = Flask(__name__)
app.config['DATABASE'] = 'wiki.db'
app.config['SECRET_KEY'] = 'your_secret_key'  # 비밀 키를 실제로는 더 복잡하게 설정해야 합니다.

# 데이터베이스 연결 함수
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

# 데이터베이스 생성 함수
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# 앱 시작 시 데이터베이스 연결
@app.before_request
def before_request():
    g.db = get_db()

# 앱 종료 시 데이터베이스 연결 해제
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

# 위키 페이지 보기
@app.route('/<page_name>')
def view_page(page_name):
    cur = g.db.execute('SELECT * FROM pages WHERE name = ?', [page_name])
    page = cur.fetchone()
    if page is None:
        return '페이지를 찾을 수 없습니다.', 404
    return render_template('view_page.html', page=page)

# 새로운 위키 페이지 만들기
@app.route('/create', methods=['GET', 'POST'])
def create_page():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        g.db.execute('INSERT INTO pages (name, content) VALUES (?, ?)', [name, content])
        g.db.commit()
        return f'<a href="/{name}">여기</a>에서 새로운 페이지 "{name}"을(를) 확인하세요.'
    return render_template('create_page.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    app.run(debug=True)
