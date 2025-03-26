from flask import render_template, request, redirect, url_for, jsonify
from app import app, db
from app.models import TrainingRecord
from app.forms import TrainingInputForm
from datetime import datetime, timedelta
from sqlalchemy import func

@app.route('/')
def home():
    # 利用可能な種目の一覧を取得
    exercises = db.session.query(TrainingRecord.exercise).distinct().all()
    exercise_list = [ex[0] for ex in exercises]
    return render_template('home.html', exercises=exercise_list)

@app.route('/progress')
def progress():
    # 利用可能な種目の一覧を取得
    exercises = db.session.query(TrainingRecord.exercise).distinct().all()
    exercise_list = [ex[0] for ex in exercises]
    return render_template('progress.html', exercises=exercise_list)

@app.route('/training/input', methods=['GET', 'POST'])
def training_input():
    form = TrainingInputForm()
    if form.validate_on_submit():
        record = TrainingRecord(
            date=datetime.now().date(),
            exercise=form.exercise.data,
            weight=form.weight.data,
            reps=form.reps.data,
            sets=form.sets.data
        )
        db.session.add(record)
        db.session.commit()
        return render_template('training_confirm.html', record=record)
    
    # 利用可能な種目の一覧を取得
    exercises = db.session.query(TrainingRecord.exercise).distinct().all()
    exercise_list = [ex[0] for ex in exercises]
    
    return render_template('training_input.html', form=form, exercises=exercise_list)

@app.route('/training/records')
def get_training_records():
    try:
        # トレーニング記録を取得
        records = db.session.query(TrainingRecord).all()
        
        # 日付の重複を除去し、ISO形式の日付文字列のリストを作成
        unique_dates = list(set(record.date.isoformat() for record in records))
        
        # 日付でソート
        unique_dates.sort()
        
        return jsonify(unique_dates)
    except Exception as e:
        print(f"Error in get_training_records: {str(e)}")
        return jsonify([]), 500

@app.route('/training/delete/<int:record_id>', methods=['POST'])
def delete_training_record(record_id):
    try:
        record = TrainingRecord.query.get_or_404(record_id)
        db.session.delete(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'トレーニング記録を削除しました。'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'トレーニング記録の削除に失敗しました。'}), 500

@app.route('/training/details')
def get_training_details():
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify([])
        
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        records = TrainingRecord.query.filter_by(date=date).all()
        
        return jsonify([{
            'id': record.id,
            'exercise': record.exercise,
            'weight': record.weight,
            'reps': record.reps,
            'sets': record.sets
        } for record in records])
    except Exception as e:
        return jsonify([])

@app.route('/training/progress')
def get_training_progress():
    exercise = request.args.get('exercise')
    period = request.args.get('period', '30days')  # デフォルトは30日間
    
    if not exercise:
        return jsonify({'error': '種目が指定されていません'}), 400

    # 期間に応じてデータを取得
    end_date = datetime.now().date()
    if period == '30days':
        start_date = end_date - timedelta(days=30)
    elif period == '1year':
        start_date = end_date - timedelta(days=365)
    else:
        return jsonify({'error': '無効な期間が指定されています'}), 400
    
    records = TrainingRecord.query.filter(
        TrainingRecord.date >= start_date,
        TrainingRecord.date <= end_date,
        TrainingRecord.exercise == exercise
    ).order_by(TrainingRecord.date).all()
    
    # 日付ごとの最大重量を取得
    date_weights = {}
    for record in records:
        date_str = record.date.isoformat()
        if date_str not in date_weights or record.weight > date_weights[date_str]:
            date_weights[date_str] = record.weight
    
    # 日付でソートしたデータを返す
    sorted_dates = sorted(date_weights.keys())
    return jsonify({
        'dates': sorted_dates,
        'weights': [date_weights[date] for date in sorted_dates]
    })