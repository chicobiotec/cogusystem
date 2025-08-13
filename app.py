from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from PIL import Image
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cogumelos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Criar pasta de uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo para múltiplas imagens por coleta
class ImagemColeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coleta_id = db.Column(db.Integer, db.ForeignKey('coleta.id'), nullable=False)
    nome_arquivo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(500))
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com Coleta
    coleta = db.relationship('Coleta', back_populates='imagens')

class Coleta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome_cientifico = db.Column(db.String(200))
    nome_popular = db.Column(db.String(200))
    data_coleta = db.Column(db.Date, nullable=False)
    local_coleta = db.Column(db.String(500))
    coordenadas = db.Column(db.String(100))
    substrato = db.Column(db.String(200))
    coletor = db.Column(db.String(200))
    observacoes = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    isolados = db.relationship('Isolado', backref='coleta', lazy=True, cascade='all, delete-orphan')
    experimentos = db.relationship('Experimento', backref='coleta', lazy=True, cascade='all, delete-orphan')
    imagens = db.relationship('ImagemColeta', back_populates='coleta', lazy=True, cascade='all, delete-orphan')

class Isolado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    coleta_id = db.Column(db.Integer, db.ForeignKey('coleta.id'), nullable=False)
    data_isolamento = db.Column(db.Date, nullable=False)
    meio_cultura = db.Column(db.String(100))
    temperatura_incubacao = db.Column(db.Float)
    observacoes = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    repiques = db.relationship('Repique', backref='isolado', lazy=True, cascade='all, delete-orphan')
    experimentos = db.relationship('Experimento', backref='isolado', lazy=True, cascade='all, delete-orphan')

class Repique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isolado_id = db.Column(db.Integer, db.ForeignKey('isolado.id'), nullable=False)
    data_repique = db.Column(db.Date, nullable=False)
    numero_placas = db.Column(db.Integer, default=1)
    meio_cultura = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

class Experimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    coleta_id = db.Column(db.Integer, db.ForeignKey('coleta.id'))
    isolado_id = db.Column(db.Integer, db.ForeignKey('isolado.id'))
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)
    objetivo = db.Column(db.Text)
    materiais_metodos = db.Column(db.Text)
    resultados = db.Column(db.Text)
    discussao = db.Column(db.Text)
    conclusoes = db.Column(db.Text)
    status = db.Column(db.String(50), default='Em andamento')
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

# Rotas principais
@app.route('/')
def index():
    total_coletas = Coleta.query.count()
    total_isolados = Isolado.query.count()
    total_experimentos = Experimento.query.count()
    
    coletas_recentes = Coleta.query.order_by(Coleta.data_cadastro.desc()).limit(5).all()
    isolados_recentes = Isolado.query.order_by(Isolado.data_cadastro.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_coletas=total_coletas,
                         total_isolados=total_isolados,
                         total_experimentos=total_experimentos,
                         coletas_recentes=coletas_recentes,
                         isolados_recentes=isolados_recentes)

# Rotas para Coletas
@app.route('/coletas')
def coletas():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    substrato = request.args.get('substrato', '')
    coletor = request.args.get('coletor', '')
    
    query = Coleta.query
    
    if search:
        query = query.filter(
            db.or_(
                Coleta.codigo.contains(search),
                Coleta.nome_cientifico.contains(search),
                Coleta.nome_popular.contains(search),
                Coleta.local_coleta.contains(search)
            )
        )
    
    if substrato:
        query = query.filter(Coleta.substrato == substrato)
    
    if coletor:
        query = query.filter(Coleta.coletor.contains(coletor))
    
    coletas = query.order_by(Coleta.data_cadastro.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('coletas.html', coletas=coletas)

@app.route('/coleta/<int:id>')
def coleta_detalhe(id):
    coleta = Coleta.query.get_or_404(id)
    return render_template('coleta_detalhe.html', coleta=coleta)

@app.route('/coleta/<int:id>/excluir', methods=['POST'])
def excluir_coleta(id):
    coleta = Coleta.query.get_or_404(id)
    try:
        # Excluir a coleta (cascade delete das imagens, isolados e experimentos)
        db.session.delete(coleta)
        db.session.commit()
        flash('Coleta excluída com sucesso!', 'success')
        return redirect(url_for('coletas'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir coleta: {str(e)}', 'error')
        return redirect(url_for('coleta_detalhe', id=id))

@app.route('/coleta/<int:id>/editar', methods=['GET', 'POST'])
def editar_coleta(id):
    coleta = Coleta.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Atualizar dados básicos da coleta
            coleta.codigo = request.form['codigo']
            coleta.nome_cientifico = request.form['nome_cientifico']
            coleta.nome_popular = request.form['nome_popular']
            coleta.data_coleta = datetime.strptime(request.form['data_coleta'], '%Y-%m-%d').date()
            coleta.local_coleta = request.form['local_coleta']
            coleta.coordenadas = request.form['coordenadas']
            coleta.substrato = request.form['substrato']
            coleta.coletor = request.form['coletor']
            coleta.observacoes = request.form['observacoes']
            
            # Processar novas imagens se fornecidas
            if 'imagens' in request.files:
                files = request.files.getlist('imagens')
                for file in files:
                    if file and file.filename != '':
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        # Criar registro da nova imagem
                        imagem = ImagemColeta(
                            coleta_id=coleta.id,
                            nome_arquivo=filename,
                            descricao=request.form.get('descricao_imagem', '')
                        )
                        db.session.add(imagem)
            
            db.session.commit()
            flash('Coleta atualizada com sucesso!', 'success')
            return redirect(url_for('coleta_detalhe', id=coleta.id))
            
        except Exception as e:
            flash(f'Erro ao atualizar coleta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('editar_coleta.html', coleta=coleta)

@app.route('/coleta/nova', methods=['GET', 'POST'])
def nova_coleta():
    if request.method == 'POST':
        try:
            # Criar nova coleta
            coleta = Coleta(
                codigo=request.form['codigo'],
                nome_cientifico=request.form['nome_cientifico'],
                nome_popular=request.form['nome_popular'],
                data_coleta=datetime.strptime(request.form['data_coleta'], '%Y-%m-%d').date(),
                local_coleta=request.form['local_coleta'],
                coordenadas=request.form['coordenadas'],
                substrato=request.form['substrato'],
                coletor=request.form['coletor'],
                observacoes=request.form['observacoes']
            )
            
            db.session.add(coleta)
            db.session.flush()  # Para obter o ID da coleta
            
            # Processar múltiplas imagens
            if 'imagens' in request.files:
                files = request.files.getlist('imagens')
                for file in files:
                    if file and file.filename != '':
                        filename = secure_filename(file.filename)
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                        filename = f"{timestamp}_{filename}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(filepath)
                        
                        # Criar registro da imagem
                        imagem = ImagemColeta(
                            coleta_id=coleta.id,
                            nome_arquivo=filename,
                            descricao=request.form.get('descricao_imagem', '')
                        )
                        db.session.add(imagem)
            
            db.session.commit()
            flash('Coleta cadastrada com sucesso!', 'success')
            return redirect(url_for('coleta_detalhe', id=coleta.id))
            
        except Exception as e:
            flash(f'Erro ao cadastrar coleta: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('nova_coleta.html')

# Rotas para Isolados
@app.route('/isolados')
def isolados():
    page = request.args.get('page', 1, type=int)
    isolados = Isolado.query.order_by(Isolado.data_cadastro.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('isolados.html', isolados=isolados)

@app.route('/isolado/<int:id>')
def isolado_detalhe(id):
    isolado = Isolado.query.get_or_404(id)
    return render_template('isolado_detalhe.html', isolado=isolado)

@app.route('/isolado/novo', methods=['GET', 'POST'])
def novo_isolado():
    if request.method == 'POST':
        try:
            isolado = Isolado(
                codigo=request.form['codigo'],
                coleta_id=request.form['coleta_id'],
                data_isolamento=datetime.strptime(request.form['data_isolamento'], '%Y-%m-%d').date(),
                meio_cultura=request.form['meio_cultura'],
                temperatura_incubacao=float(request.form['temperatura_incubacao']) if request.form['temperatura_incubacao'] else None,
                observacoes=request.form['observacoes']
            )
            
            db.session.add(isolado)
            db.session.commit()
            flash('Isolado cadastrado com sucesso!', 'success')
            return redirect(url_for('isolados'))
            
        except Exception as e:
            flash(f'Erro ao cadastrar isolado: {str(e)}', 'error')
            db.session.rollback()
    
    coletas = Coleta.query.all()
    return render_template('novo_isolado.html', coletas=coletas)

# Rotas para Repiques
@app.route('/repique/novo/<int:isolado_id>', methods=['GET', 'POST'])
def novo_repique(isolado_id):
    isolado = Isolado.query.get_or_404(isolado_id)
    
    if request.method == 'POST':
        try:
            repique = Repique(
                isolado_id=isolado_id,
                data_repique=datetime.strptime(request.form['data_repique'], '%Y-%m-%d').date(),
                numero_placas=int(request.form['numero_placas']),
                meio_cultura=request.form['meio_cultura'],
                observacoes=request.form['observacoes']
            )
            
            db.session.add(repique)
            db.session.commit()
            flash('Repique cadastrado com sucesso!', 'success')
            return redirect(url_for('isolado_detalhe', id=isolado_id))
            
        except Exception as e:
            flash(f'Erro ao cadastrar repique: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('novo_repique.html', isolado=isolado)

@app.route('/repique/<int:id>/excluir', methods=['POST'])
def excluir_repique(id):
    repique = Repique.query.get_or_404(id)
    isolado_id = repique.isolado_id
    try:
        db.session.delete(repique)
        db.session.commit()
        flash('Repique excluído com sucesso!', 'success')
        return redirect(url_for('isolado_detalhe', id=isolado_id))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir repique: {str(e)}', 'error')
        return redirect(url_for('isolado_detalhe', id=isolado_id))

# Rotas para Experimentos
@app.route('/experimentos')
def experimentos():
    page = request.args.get('page', 1, type=int)
    experimentos = Experimento.query.order_by(Experimento.data_cadastro.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('experimentos.html', experimentos=experimentos)

@app.route('/experimento/<int:id>')
def experimento_detalhe(id):
    experimento = Experimento.query.get_or_404(id)
    return render_template('experimento_detalhe.html', experimento=experimento)

@app.route('/experimento/<int:id>/excluir', methods=['POST'])
def excluir_experimento(id):
    experimento = Experimento.query.get_or_404(id)
    try:
        db.session.delete(experimento)
        db.session.commit()
        flash('Experimento excluído com sucesso!', 'success')
        return redirect(url_for('experimentos'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir experimento: {str(e)}', 'error')
        return redirect(url_for('experimento_detalhe', id=id))

@app.route('/experimento/novo', methods=['GET', 'POST'])
def novo_experimento():
    if request.method == 'POST':
        try:
            experimento = Experimento(
                titulo=request.form['titulo'],
                coleta_id=request.form['coleta_id'] if request.form['coleta_id'] else None,
                isolado_id=request.form['isolado_id'] if request.form['isolado_id'] else None,
                data_inicio=datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date() if request.form['data_inicio'] else None,
                data_fim=datetime.strptime(request.form['data_fim'], '%Y-%m-%d').date() if request.form['data_fim'] else None,
                objetivo=request.form['objetivo'],
                materiais_metodos=request.form['materiais_metodos'],
                resultados=request.form['resultados'],
                discussao=request.form['discussao'],
                conclusoes=request.form['conclusoes'],
                status=request.form['status']
            )
            
            db.session.add(experimento)
            db.session.commit()
            flash('Experimento cadastrado com sucesso!', 'success')
            return redirect(url_for('experimentos'))
            
        except Exception as e:
            flash(f'Erro ao cadastrar experimento: {str(e)}', 'error')
            db.session.rollback()
    
    coletas = Coleta.query.all()
    isolados = Isolado.query.all()
    return render_template('novo_experimento.html', coletas=coletas, isolados=isolados)

# Rotas para exclusão de isolados
@app.route('/isolado/<int:id>/excluir', methods=['POST'])
def excluir_isolado(id):
    isolado = Isolado.query.get_or_404(id)
    try:
        # Excluir o isolado (cascade delete dos repiques e experimentos relacionados)
        db.session.delete(isolado)
        db.session.commit()
        flash('Isolado excluído com sucesso!', 'success')
        return redirect(url_for('isolados'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir isolado: {str(e)}', 'error')
        return redirect(url_for('isolado_detalhe', id=id))

@app.route('/isolado/<int:id>/editar', methods=['GET', 'POST'])
def editar_isolado(id):
    isolado = Isolado.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Atualizar dados do isolado
            isolado.codigo = request.form['codigo']
            isolado.data_isolamento = datetime.strptime(request.form['data_isolamento'], '%Y-%m-%d').date()
            isolado.meio_cultura = request.form['meio_cultura']
            isolado.temperatura_incubacao = request.form.get('temperatura_incubacao') or None
            isolado.observacoes = request.form.get('observacoes', '')
            
            # Se meio_cultura for 'outros', usar o valor do campo outros_meios
            if isolado.meio_cultura == 'outros':
                isolado.meio_cultura = request.form.get('outros_meios', '')
            
            db.session.commit()
            flash('Isolado atualizado com sucesso!', 'success')
            return redirect(url_for('isolado_detalhe', id=isolado.id))
            
        except Exception as e:
            flash(f'Erro ao atualizar isolado: {str(e)}', 'error')
            db.session.rollback()
    
    # Buscar todas as coletas para o select
    coletas = Coleta.query.all()
    return render_template('editar_isolado.html', isolado=isolado, coletas=coletas)

@app.route('/repique/<int:id>/editar', methods=['GET', 'POST'])
def editar_repique(id):
    repique = Repique.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Atualizar dados do repique
            repique.data_repique = datetime.strptime(request.form['data_repique'], '%Y-%m-%d').date()
            repique.numero_placas = int(request.form['numero_placas'])
            repique.meio_cultura = request.form['meio_cultura']
            repique.observacoes = request.form.get('observacoes', '')
            
            # Se meio_cultura for 'outros', usar o valor do campo outros_meios
            if repique.meio_cultura == 'outros':
                repique.meio_cultura = request.form.get('outros_meios', '')
            
            db.session.commit()
            flash('Repique atualizado com sucesso!', 'success')
            return redirect(url_for('isolado_detalhe', id=repique.isolado_id))
            
        except Exception as e:
            flash(f'Erro ao atualizar repique: {str(e)}', 'error')
            db.session.rollback()
    
    return render_template('editar_repique.html', repique=repique)

@app.route('/experimento/<int:id>/editar', methods=['GET', 'POST'])
def editar_experimento(id):
    experimento = Experimento.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Atualizar dados do experimento
            experimento.titulo = request.form['titulo']
            experimento.data_inicio = datetime.strptime(request.form['data_inicio'], '%Y-%m-%d').date() if request.form.get('data_inicio') else None
            experimento.data_fim = datetime.strptime(request.form['data_fim'], '%Y-%m-%d').date() if request.form.get('data_fim') else None
            experimento.status = request.form['status']
            experimento.objetivo = request.form.get('objetivo', '')
            experimento.materiais_metodos = request.form.get('materiais_metodos', '')
            experimento.resultados = request.form.get('resultados', '')
            experimento.discussao = request.form.get('discussao', '')
            experimento.conclusoes = request.form.get('conclusoes', '')
            
            db.session.commit()
            flash('Experimento atualizado com sucesso!', 'success')
            return redirect(url_for('experimento_detalhe', id=experimento.id))
            
        except Exception as e:
            flash(f'Erro ao atualizar experimento: {str(e)}', 'error')
            db.session.rollback()
    
    # Buscar todas as coletas e isolados para os selects
    coletas = Coleta.query.all()
    isolados = Isolado.query.all()
    return render_template('editar_experimento.html', experimento=experimento, coletas=coletas, isolados=isolados)

# Sistema de busca
@app.route('/busca')
def busca():
    query = request.args.get('q', '')
    tipo = request.args.get('tipo', 'todos')
    
    resultados = {}
    
    if query:
        if tipo in ['todos', 'coletas']:
            coletas = Coleta.query.filter(
                db.or_(
                    Coleta.codigo.contains(query),
                    Coleta.nome_cientifico.contains(query),
                    Coleta.nome_popular.contains(query),
                    Coleta.local_coleta.contains(query)
                )
            ).all()
            resultados['coletas'] = coletas
        
        if tipo in ['todos', 'isolados']:
            isolados = Isolado.query.filter(
                db.or_(
                    Isolado.codigo.contains(query),
                    Isolado.meio_cultura.contains(query)
                )
            ).all()
            resultados['isolados'] = isolados
        
        if tipo in ['todos', 'experimentos']:
            experimentos = Experimento.query.filter(
                db.or_(
                    Experimento.titulo.contains(query),
                    Experimento.objetivo.contains(query)
                )
            ).all()
            resultados['experimentos'] = experimentos
    
    return render_template('busca.html', resultados=resultados, query=query, tipo=tipo)

# Rota para servir imagens
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# API para dados em JSON
@app.route('/api/coletas')
def api_coletas():
    coletas = Coleta.query.all()
    return jsonify([{
        'id': c.id,
        'codigo': c.codigo,
        'nome_cientifico': c.nome_cientifico,
        'nome_popular': c.nome_popular,
        'data_coleta': c.data_coleta.strftime('%Y-%m-%d') if c.data_coleta else None,
        'local_coleta': c.local_coleta
    } for c in coletas])

@app.route('/api/isolados')
def api_isolados():
    isolados = Isolado.query.all()
    return jsonify([{
        'id': i.id,
        'codigo': i.codigo,
        'coleta_codigo': i.coleta.codigo if i.coleta else None,
        'data_isolamento': i.data_isolamento.strftime('%Y-%m-%d') if i.data_isolamento else None,
        'meio_cultura': i.meio_cultura
    } for i in isolados])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
