document.addEventListener('DOMContentLoaded', function() {
    // カレンダーイベント処理
    function initializeCalendar() {
        const calendarEl = document.getElementById('calendar');
        if (calendarEl) {
            const calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                locale: 'ja',
                height: 'auto',
                dateClick: function(info) {
                    window.location.href = `/training/input?date=${info.dateStr}`;
                },
                events: function(fetchInfo, successCallback, failureCallback) {
                    fetch('/training/records')
                        .then(response => response.json())
                        .then(records => {
                            const events = records.map(record => ({
                                title: '筋トレ',
                                start: record.date,
                                backgroundColor: 'green',
                                borderColor: 'green'
                            }));
                            successCallback(events);
                        })
                        .catch(failureCallback);
                }
            });
            calendar.render();
        }
    }

    // 進捗グラフ初期化
    function initializeProgressChart() {
        const progressChartEl = document.getElementById('progressChart');
        if (progressChartEl) {
            fetch('/training/progress')
                .then(response => response.json())
                .then(data => {
                    const ctx = progressChartEl.getContext('2d');
                    new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: data.labels,
                            datasets: [{
                                label: '総トレーニング量',
                                data: data.values,
                                borderColor: 'rgb(75, 192, 192)',
                                tension: 0.1
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                title: {
                                    display: true,
                                    text: 'トレーニング進捗'
                                }
                            }
                        }
                    });
                });
        }
    }

    // 最近のトレーニング履歴表示
    function displayRecentTrainings() {
        const recentTrainingsEl = document.getElementById('recent-trainings');
        if (recentTrainingsEl) {
            fetch('/training/records')
                .then(response => response.json())
                .then(records => {
                    recentTrainingsEl.innerHTML = records.slice(0, 5).map(record => 
                        `<li class="list-group-item">
                            ${record.date}: ${record.exercise} - ${record.weight}kg x ${record.sets}セット
                        </li>`
                    ).join('');
                });
        }
    }

    // トレーニング入力フォームのリアルタイムバリデーション
    function setupTrainingInputValidation() {
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', function(event) {
                const exercise = form.querySelector('#exercise');
                const weight = form.querySelector('#weight');
                const reps = form.querySelector('#reps');
                const sets = form.querySelector('#sets');

                let isValid = true;

                // バリデーションロジック
                if (!exercise.value.trim()) {
                    exercise.classList.add('is-invalid');
                    isValid = false;
                } else {
                    exercise.classList.remove('is-invalid');
                }

                if (weight.value <= 0) {
                    weight.classList.add('is-invalid');
                    isValid = false;
                } else {
                    weight.classList.remove('is-invalid');
                }

                if (reps.value <= 0) {
                    reps.classList.add('is-invalid');
                    isValid = false;
                } else {
                    reps.classList.remove('is-invalid');
                }

                if (sets.value <= 0) {
                    sets.classList.add('is-invalid');
                    isValid = false;
                } else {
                    sets.classList.remove('is-invalid');
                }

                if (!isValid) {
                    event.preventDefault();
                }
            });
        }
    }

    // ページごとの初期化
    initializeCalendar();
    initializeProgressChart();
    displayRecentTrainings();
    setupTrainingInputValidation();
});